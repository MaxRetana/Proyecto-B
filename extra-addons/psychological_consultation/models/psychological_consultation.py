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
    pacient_id = fields.Many2one('res.partner', string='Paciente', tracking=True)
    email_pacient = fields.Char('Email del Paciente', related='pacient_id.email', store=True, tracking=True)
    number_pacient = fields.Char('Número de Teléfono del Paciente', related='pacient_id.phone', store=True, tracking=True)
    psycologist_id = fields.Many2one('res.partner', string='Psicólogo', tracking=True)
    email_psycologist = fields.Char('Email del Psicólogo', related='psycologist_id.email', store=True, tracking=True)
    number_psycologist = fields.Char('Número de Teléfono del Psicólogo', related='psycologist_id.phone', store=True, tracking=True)
    date_consultation = fields.Datetime('Fecha de Consulta', tracking=True)
    notes = fields.Text('Notas', tracking=True)
    state = fields.Selection([
        ('confirmed', 'Confirmada'),
        ('done', 'Realizada'),
        ('cancelled', 'Cancelada')
    ], string='Estado', default='confirmed', tracking=True)
    