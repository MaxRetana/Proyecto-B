from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    
    is_psychologist_consultation = fields.Boolean(string='Es Usuario de Consulta Psicológica', tracking=True)
    type_of_psychologist_consultation = fields.Selection([
        ('patient', 'Paciente'),
        ('psychologist', 'Psicologo')
    ], string='Tipo de Consulta Psicológica', tracking=True)
    
    
    @api.model_create_multi
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        default_is_psychologist_consultation = self.env.context.get('default_is_psychologist_consultation', False)
        default_type_of_psychologist_consultation = self.env.context.get('default_type_of_psychologist_consultation', False)
        if default_is_psychologist_consultation:
            for vals in vals_list:
                if 'is_psychologist_consultation' not in vals:
                    vals['is_psychologist_consultation'] = default_is_psychologist_consultation
                if 'type_of_psychologist_consultation' not in vals:
                    vals['type_of_psychologist_consultation'] = default_type_of_psychologist_consultation

        return super(HrEmployee, self).create(vals_list)