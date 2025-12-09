from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests
import json
from datetime import datetime

class EneamPointage(models.Model):
    _name = 'eneam.pointage'
    _description = 'Pointage ENEAM (sync Django)'
    _rec_name = 'personnel_id'
    _sql_constraints = [
        ('uniq_day_type', 'unique(personnel_id, date_pointage, type_pointage)',
         'Un seul pointage de ce type par jour.')
    ]

    personnel_id   = fields.Many2one('hr.employee', string='Personnel', required=True, ondelete='cascade')
    date_pointage  = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    type_pointage  = fields.Selection([('arrivee','Arrivée'),('depart','Départ'),('pause_debut','Début Pause'),('pause_fin','Fin Pause')], string='Type', required=True)
    datetime_str   = fields.Char(string='Date-heure Django')  # ISO string reçue / envoyée
    notes          = fields.Text(string='Notes')
    synced         = fields.Boolean(string='Synchronisé avec Django', default=False)

    # DJANGO_URL = "http://127.0.0.1:8000/api"
    DJANGO_URL = "http://django:8000/api"

    # -----------------
    # Bouton ARRIVÉE
    # -----------------
    def action_pointer_arrivee(self):
        self.ensure_one()
        self._push_django('arrivee')

    # -----------------
    # Bouton DÉPART
    # -----------------
    def action_pointer_depart(self):
        self.ensure_one()
        self._push_django('depart')

    # -----------------
    # PUSH vers Django
    # -----------------
    def _push_django(self, type_):
        dt_iso = datetime.now().isoformat(timespec='seconds')
        data = {
            'personnel': self.personnel_id.matricule,
            'type_pointage': type_,
            'datetime_pointage': dt_iso,
            'notes': self.notes or f'Pointage {type_} depuis Odoo',
            'appareil_id': 'odoo_front',
        }

        resp = requests.post(f"{self.DJANGO_URL}/pointage/", json=data, headers={'Content-Type': 'application/json'})

        if resp.status_code not in (201, 200):
            raise UserError(_("Erreur Django : %s") % resp.text)

        self.synced = True # Marquer comme synchronisé
        self.type_pointage = type_
        self.datetime_str = dt_iso