from odoo import models, fields, api

class TimeWorkConsultation(models.Model):
    
    _name = 'time.work.consultation'
    _description = 'Horario de Trabajo para Consultas Psicológicas'

    name = fields.Char('Nombre del Horario', required=True)
    time_lines = fields.One2many('time.work.consultation.line', 'consultation_id', string='Líneas de Horario')
    

class TimeWorkConsultationLine(models.Model):
    
    _name = 'time.work.consultation.line'
    _description = 'Línea de Horario de Trabajo para Consultas Psicológicas'

    consultation_id = fields.Many2one('time.work.consultation', string='Horario de Consulta', required=True, ondelete='cascade')
    day_of_week = fields.Selection([
        ('0', 'Lunes'),
        ('1', 'Martes'),
        ('2', 'Miércoles'),
        ('3', 'Jueves'),
        ('4', 'Viernes'),
        ('5', 'Sábado'),
        ('6', 'Domingo')
    ], string='Día de la Semana', required=True)
    start_time = fields.Float('Hora de Inicio', required=True)
    end_time = fields.Float('Hora de Fin', required=True)