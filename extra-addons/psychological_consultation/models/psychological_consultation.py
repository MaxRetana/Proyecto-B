# -*- coding: utf-8 -*-
import logging
from datetime import datetime

import pytz

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
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmada'),
        ('done', 'Realizada'),
        ('cancelled', 'Cancelada')
    ], string='Estado', default='draft', tracking=True)
    clinic_id = fields.Many2one('psychological.clinic', string='Clínica', tracking=True)
    
    def get_consultation_date_mexico_tz(self):
        """Retorna la fecha de consulta en zona horaria de México (America/Mexico_City)."""
        if not self.date_consultation:
            return None
        # date_consultation está en UTC, convertir a México
        mexico_tz = pytz.timezone('America/Mexico_City')
        # El datetime de Odoo viene sin timezone info (UTC), lo hacemos aware y luego convertimos
        utc_dt = pytz.UTC.localize(self.date_consultation)
        mexico_dt = utc_dt.astimezone(mexico_tz)
        return mexico_dt
    
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'
            rec.message_post(body=_('Consulta confirmada.'))
            rec._send_confirmation_emails()

    def _send_confirmation_emails(self):
        template_patient = self.env.ref(
            'psychological_consultation.mail_template_consultation_confirmed_patient',
            raise_if_not_found=False,
        )
        template_psychologist = self.env.ref(
            'psychological_consultation.mail_template_consultation_confirmed_psychologist',
            raise_if_not_found=False,
        )

        recipient_values = [
            (template_patient, self.pacient_id.name or 'Paciente', self.email_pacient),
            (template_psychologist, self.psycologist_id.name or 'Psicologo', self.email_psycologist),
        ]

        for template, recipient_name, email_to in recipient_values:
            if not template:
                _logger.warning('No se encontro la plantilla de confirmacion para: %s', recipient_name)
                continue
            if not email_to:
                _logger.info('No hay correo configurado para el destinatario: %s', recipient_name)
                continue
            try:
                mail_id = template.send_mail(
                    self.id,
                    force_send=True,
                    email_values={'email_to': email_to},
                )
                if mail_id:
                    _logger.info('Correo de confirmacion enviado a %s (%s)', recipient_name, email_to)
            except Exception as e:
                _logger.exception(
                    'Error enviando correo de confirmacion de consulta %s a %s: %s',
                    self.name,
                    email_to,
                    str(e)
                )
            
            
    def cancelation_wizard(self):
        if self.state in ['done', 'cancelled']:
            raise UserError(_('No se puede cancelar una consulta que ya está realizada o cancelada.'))
        return {
            'name': _('Cancelar Consulta Psicológica'),
            'type': 'ir.actions.act_window',
            'res_model': 'psychological.consultation.cancelation',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }
    
    def action_cancel(self, reason):
        for rec in self:
            rec.state = 'cancelled'
            rec.message_post(body=_('Consulta cancelada. Razón: %s', reason or 'Sin especificar'))
            rec._send_rejection_emails(reason)

    def _send_rejection_emails(self, reason):
        template_rejection_patient = self.env.ref(
            'psychological_consultation.mail_template_consultation_rejected_patient',
            raise_if_not_found=False,
        )
        template_rejection_psychologist = self.env.ref(
            'psychological_consultation.mail_template_consultation_rejected_psychologist',
            raise_if_not_found=False,
        )

        recipient_values = [
            (
                template_rejection_patient,
                self.pacient_id.name or 'Paciente',
                self.email_pacient,
            ),
            (
                template_rejection_psychologist,
                self.psycologist_id.name or 'Psicologo',
                self.email_psycologist,
            ),
        ]

        for template, recipient_name, email_to in recipient_values:
            if not template:
                _logger.warning('No se encontro la plantilla de rechazo para: %s', recipient_name)
                continue
            if not email_to:
                _logger.info('No hay correo configurado para el destinatario: %s', recipient_name)
                continue
            try:
                mail_id = template.with_context(rejection_reason=reason or 'Sin especificar').send_mail(
                    self.id,
                    force_send=True,
                    email_values={'email_to': email_to},
                )
                if mail_id:
                    _logger.info('Correo de rechazo enviado a %s (%s)', recipient_name, email_to)
            except Exception as e:
                _logger.exception(
                    'Error enviando correo de rechazo de consulta %s a %s: %s',
                    self.name,
                    email_to,
                    str(e)
                )
            
            
    
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