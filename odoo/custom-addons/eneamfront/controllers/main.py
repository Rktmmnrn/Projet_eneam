from odoo import http, fields
from odoo.http import request

class Eneamfront (http.Controller):
    
    @http.route('/pointage', auth='user', website=True)
    def pointage(self, **kw):
        user = request.env.user
        # Trouver l'employé associé à cet utilisateur
        employee = request.env['hr.employee'].search([
            ('user_id', '=', user.id)
        ], limit=1)
        
        if not employee:
            return request.render('eneamfront.error_template', {
                'error': 'Aucun employé associé à votre compte. Contactez l\'administrateur.'
            })
        # Vérifier que l'employé a un matricule (lié à Django)
        if not employee.matricule:
            return request.render('eneamfront.error_template', {
                'error': 'Votre compte employé n\'a pas de matricule. Contactez l\'administrateur.'
            })

        if user.has_group('eneamfront.group_eneam_responsable'):
            return self._page_dg()
        else:
            return self._page_employe(employee)


    def _page_dg(self):
        # base_url = "http://127.0.0.1:8000/api"          # back Django
        base_url = "http://192.168.88.5:8000/api"
        today = fields.Date.today()
        return request.render('eneamfront.page_dg', {
            'api_url': base_url + '/pointage/',
            'today': today,
        })


    def _page_employe(self, employee):
        """Page employé avec données de l'employé connecté"""
        return request.render('eneamfront.page_employe', {
            'employee': employee,
            'matricule': employee.matricule,
            'api_personnel_url': 'http://192.168.88.5:8000/api/personnel/',
            # 'api_personnel_url': 'http://127.0.0.1:8000/api/personnel/',
            'api_pointage_url': 'http://192.168.88.5:8000/api/pointage/',
            # 'api_pointage_url': 'http://127.0.0.1:8000/api/pointage/',
        })


    # controllers/main.py - AJOUTER
    @http.route('/pointage/arrivee', auth='user', website=True)
    def pointer_arrivee(self, **kw):
        """Pointage arrivée pour l'employé connecté"""
        return self._pointer_type('arrivee')


    @http.route('/pointage/depart', auth='user', website=True)  
    def pointer_depart(self, **kw):
        """Pointage départ pour l'employé connecté"""
        return self._pointer_type('depart')

    def _pointer_type(self, type_pointage):
        """Pointage pour l'utilisateur connecté"""
        user = request.env.user
        employee = request.env['hr.employee'].search([
            ('user_id', '=', user.id)
        ], limit=1)
        
        if not employee or not employee.matricule:
            return request.render('eneamfront.error_template', {
                'error': 'Employé non configuré pour le pointage.'
            })

        # Synchroniser avec Django et verification de l'existance d'une pointage de même type
        try:
            today = fields.Date.today()
            existing_pointage = request.env['eneam.pointage'].sudo().search([
                ('personnel_id', '=', employee.id),
                ('type_pointage', '=', type_pointage),
                ('date_pointage', '=', today)
            ], limit=1)
            
            if existing_pointage:
                # Demander confirmation de mise à jour
                ancienne_heure = existing_pointage.datetime_str or "précédemment"
                return request.render('eneamfront.confirm_update_template', {
                    'existing_pointage': existing_pointage,
                    'type_pointage': type_pointage,
                    'employee': employee,
                    'matricule': employee.matricule,
                    'ancienne_heure': ancienne_heure,
                })

            # nouveau pointage
            pointage = request.env['eneam.pointage'].sudo().create({
                'personnel_id': employee.id,
                'type_pointage': type_pointage,
                'date_pointage': today,
                'notes': f'Pointage {type_pointage} depuis interface web'
            })
            
            # Synchroniser avec Django
            pointage._push_django(type_pointage)
            success = True
            message = f'✅ Pointage {type_pointage} enregistré avec succès!'
        
            return request.render('eneamfront.pointage_result', {
                'success': success,
                'message': message,
                'type_pointage': type_pointage,
                'employee': employee,
                'matricule': employee.matricule,
            })

        except Exception as e:
            success = False
            message = f'❌ Erreur: {str(e)}'
            return request.render('eneamfront.pointage_result', {
                'success': success,
                'message': message,
                'type_pointage': type_pointage,
                'employee': employee,
                'matricule': getattr(employee, 'matricule', None),
            })

    # Route pour la confirmation maj
    @http.route('/pointage/update/<int:pointage_id>', auth='user', website=True)
    def confirm_update_pointage(self, pointage_id, **kw):
        """Confirmation de mise à jour d'un pointage existant"""
        pointage = request.env['eneam.pointage'].browse(pointage_id)
        
        if not pointage.exists():
            return request.render('eneamfront.error_template', {
                'error': 'Pointage non trouvé.'
            })
        
        # Mettre à jour le pointage existant
        try:
            pointage._push_django(pointage.type_pointage)
            
            return request.render('eneamfront.pointage_result', {
                'success': True,
                'message': f'Pointage {pointage.type_pointage} mis à jour avec succès!',
                'type_pointage': pointage.type_pointage,
                'employee': pointage.personnel_id,
                'matricule': pointage.personnel_id.matricule,
            })
        
        except Exception as e:
            return request.render('eneamfront.pointage_result', {
                'success': False,
                'message': f'Erreur lors de la mise à jour: {str(e)}',
                'type_pointage': pointage.type_pointage,
                'employee': pointage.personnel_id,
                'matricule': pointage.personnel_id.matricule,
            })