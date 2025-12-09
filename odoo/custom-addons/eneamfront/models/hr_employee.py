from odoo.exceptions import UserError
from odoo import models, fields, api, _
import requests

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Ajouter le champ matricule s'il n'existe pas
    matricule = fields.Char(string='Matricule', required=True)
    user_id = fields.Many2one('res.users', string='Compte Odoo')
    django_id = fields.Integer(string='ID Django')

    # crée un compte Odoo lié à l'employé
    def action_create_user(self):
        self.ensure_one()
        
        # VÉRIFICATION 1: Données obligatoires
        if self.user_id:
            raise UserError(_('Cet employé a déjà un compte Odoo.'))
        if not self.work_email:
            raise UserError(_('Renseignez un email professionnel.'))
        if not self.matricule:
            raise UserError(_('Renseignez un matricule.'))

        # VÉRIFICATION 2: L'employé existe-t-il dans Django ?
        try:
            api_url = "http://django:8000/api/personnel/"
            # api_url = "http://127.0.0.1:8000/api/personnel/"
            params = {'matricule': self.matricule}  # ← Recherche par MATRICULE maintenant
            
            response = requests.get(api_url, params=params, timeout=10)
            
            if response.status_code != 200:
                raise UserError(_('Erreur API Django: %s') % response.status_code)
                
            personnel_data = response.json()
            
            if not personnel_data:
                raise UserError(
                    _('Matricule "%s" non trouvé dans Django. Créez d\'abord le personnel dans Django.') % self.matricule
                )
                
            # ✅ Employé trouvé dans Django - on peut créer le compte
            django_personnel = personnel_data[0]
            
        except requests.exceptions.RequestException as e:
            raise UserError(_('Erreur connexion Django: %s') % str(e))

        # CRÉATION du compte Odoo
        try:
            group_user = self.env.ref('base.group_user')
            user = self.env['res.users'].sudo().create({
                'name': self.name,
                'login': self.work_email, 
                'email': self.work_email,
                'groups_id': [(4, group_user.id)],
            })

            # ASSOCIATION compte Odoo → employé
            self.user_id = user.id
            
            # STOCKER l'ID Django pour référence
            self.django_id = django_personnel.get('id')
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Succès'),
                    'message': _('Compte Odoo créé pour %s (Matricule: %s)') % (self.name, self.matricule),
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except Exception as e:
            raise UserError(_('Erreur création compte: %s') % str(e))