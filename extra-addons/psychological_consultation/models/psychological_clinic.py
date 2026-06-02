from urllib.parse import quote_plus

from odoo import models, fields, api

class PsychologicalClinic(models.Model):
    _name = 'psychological.clinic'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Clínica Psicológica'

    name = fields.Char('Nombre de la Clínica', tracking=True)
    address = fields.Char('Dirección de la Clínica', tracking=True)
    active = fields.Boolean('Activo', default=True, tracking=True)
    city = fields.Char('Ciudad de la Clínica', tracking=True)
    state = fields.Char('Estado de la Clínica', tracking=True)
    country = fields.Char('País de la Clínica', tracking=True)
    zip_code = fields.Char('Código Postal de la Clínica', tracking=True)
    phone = fields.Char('Teléfono de la Clínica', tracking=True)
    email = fields.Char('Email de la Clínica', tracking=True)
    latitude = fields.Float('Latitud', tracking=True)
    longitude = fields.Float('Longitud', tracking=True)
    maps_url = fields.Char('URL de Maps', compute='_compute_maps_url', tracking=True)

    def _build_full_address(self):
        self.ensure_one()
        parts = [self.address, self.city, self.state, self.zip_code, self.country]
        return ", ".join(part for part in parts if part)

    @api.depends('address', 'city', 'state', 'zip_code', 'country')
    def _compute_maps_url(self):
        for record in self:
            full_address = record._build_full_address() if record else ''
            record.maps_url = f"https://www.google.com/maps/search/?api=1&query={quote_plus(full_address)}" if full_address else False