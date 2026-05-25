from odoo import models, fields, api
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    
    is_psychologist_consultation = fields.Boolean(string='Es Usuario de Consulta Psicológica', tracking=True)
    type_of_psychologist_consultation = fields.Selection([
        ('patient', 'Paciente'),
        ('psychologist', 'Psicologo')
    ], string='Tipo de Consulta Psicológica', tracking=True)
    
    
    @api.model
    def create(self, vals):
        default_is_psychologist_consultation = self.env.context.get('default_is_psychologist_consultation', False)
        default_type_of_psychologist_consultation = self.env.context.get('default_type_of_psychologist_consultation', False)
        if default_is_psychologist_consultation:
            if 'is_psychologist_consultation' not in vals:
                vals['is_psychologist_consultation'] = default_is_psychologist_consultation
            if 'type_of_psychologist_consultation' not in vals:
                vals['type_of_psychologist_consultation'] = default_type_of_psychologist_consultation
        return super(ResPartner, self).create(vals)