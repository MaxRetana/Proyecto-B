# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class PsychologicalConsultation(models.Model):
    _name = 'psychological.consultation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Consulta Psicológica'

    name = fields.Char('Referencia', default='Nuevo', tracking=True)
    pacient_id = fields.Many2one('hr.employee', string='Paciente', tracking=True)
    email_pacient = fields.Char('Email del Paciente', related='pacient_id.work_email', store=True, tracking=True)
    number_pacient = fields.Char('Número de Teléfono del Paciente', related='pacient_id.work_phone', store=True, tracking=True)
    psycologist_id = fields.Many2one('hr.employee', string='Psicólogo', tracking=True)
    email_psycologist = fields.Char('Email del Psicólogo', related='psycologist_id.work_email', store=True, tracking=True)
    number_psycologist = fields.Char('Número de Teléfono del Psicólogo', related='psycologist_id.work_phone', store=True, tracking=True)
    date_consultation = fields.Datetime('Fecha de Consulta', tracking=True)
    notes = fields.Text('Notas', tracking=True)
    state = fields.Selection([
        ('confirmed', 'Confirmada'),
        ('done', 'Realizada'),
        ('cancelled', 'Cancelada')
    ], string='Estado', default='confirmed', tracking=True)
    
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals.get('name') == 'Nuevo':
                # Buscar si existe la secuencia, si no existe la crea
                sequence = self.env['ir.sequence'].search([('code', '=', 'psychological.consultation')], limit=1)
                if not sequence:
                    sequence = self.env['ir.sequence'].create({
                        'name': 'Psychological Consultation Sequence',
                        'code': 'psychological.consultation',
                        'prefix': 'PC',
                        'padding': 4,
                        'number_next': 1,
                        'number_increment': 1,
                    })
                
                # Generar el siguiente número
                next_number = self.env['ir.sequence'].next_by_code('psychological.consultation') or '0001'
                vals['name'] = f"{next_number}"
        return super().create(vals_list)