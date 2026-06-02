from odoo import models, fields, api, _

class PsychologicalConsultationCancelation(models.TransientModel):
    _name = 'psychological.consultation.cancelation'
    _description = 'Cancelación de Consulta Psicológica'

    reason = fields.Text('Razón de Cancelación')
    consultation_id = fields.Many2one('psychological.consultation', string='Consulta a Cancelar')

    def action_cancel_consultation(self):
        #context
        consultation = self._context.get('active_id')
        if consultation:
            self.consultation_id = self.env['psychological.consultation'].browse(consultation)
            self.consultation_id.action_cancel(self.reason)
            
        else:
            raise ValueError(_('No se ha proporcionado una consulta para cancelar.'))