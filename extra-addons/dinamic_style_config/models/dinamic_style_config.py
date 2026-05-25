import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DinamicStyleConfig(models.Model):
    _name = 'dinamic.style.config'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Colores Dinamicos para estilos de odoo backend'
    _order = 'priority desc, id desc'

    name = fields.Char(string='Nombre de la configuración', default='Estilo predeterminado', tracking=True)
    is_active = fields.Boolean(string='Activa', default=False, tracking=True)
    priority = fields.Integer(string='Prioridad', default=10, tracking=True)

    theme_mode = fields.Selection([
        ('light', 'Claro'),
        ('dark', 'Oscuro'),
        ('auto', 'Automático'),
    ], string='Modo del tema', default='light', tracking=True)

    primary_color = fields.Char(string='Color primario', default='#000000', tracking=True)
    secondary_color = fields.Char(string='Color secundario', default='#FFFFFF', tracking=True)
    accent_color = fields.Char(string='Color de acento', default='#1f6feb', tracking=True)
    background_color = fields.Char(string='Color de fondo', default='#FFFFFF', tracking=True)
    card_bg_color = fields.Char(string='Color de tarjetas', default='#FFFFFF', tracking=True)
    sidebar_bg_color = fields.Char(string='Color de barra lateral', default='#F6F8FA', tracking=True)
    navbar_bg_color = fields.Char(string='Color de barra superior', default='#FFFFFF', tracking=True)
    text_color = fields.Char(string='Color del texto', default='#111827', tracking=True)
    muted_text_color = fields.Char(string='Color de texto secundario', default='#6B7280', tracking=True)
    border_color = fields.Char(string='Color del borde', default='#D1D5DB', tracking=True)
    success_color = fields.Char(string='Color de éxito', default='#16A34A', tracking=True)
    warning_color = fields.Char(string='Color de advertencia', default='#F59E0B', tracking=True)
    danger_color = fields.Char(string='Color de error', default='#DC2626', tracking=True)
    info_color = fields.Char(string='Color informativo', default='#0EA5E9', tracking=True)
    link_color = fields.Char(string='Color de enlaces', default='#2563EB', tracking=True)
    link_hover_color = fields.Char(string='Color hover de enlaces', default='#1D4ED8', tracking=True)
    button_text_color = fields.Char(string='Texto de botón primario', default='#FFFFFF', tracking=True)
    button_secondary_text_color = fields.Char(string='Texto de botón secundario', default='#111827', tracking=True)
    navbar_text_color = fields.Char(string='Texto de barra superior', default='#111827', tracking=True)
    navbar_hover_bg_color = fields.Char(string='Hover de barra superior', default='#DBEAFE', tracking=True)
    navbar_hover_text_color = fields.Char(string='Texto hover de barra superior', default='#111827', tracking=True)
    navbar_icon_color = fields.Char(
        string='Iconos barra superior',
        default='#6B7280',
        tracking=True,
        help='Afecta: .o_main_navbar .fa, .o_main_navbar .oi, .o_main_navbar i'
    )
    navbar_icon_hover_color = fields.Char(
        string='Iconos hover barra superior',
        default='#111827',
        tracking=True,
        help='Afecta hover: .o_main_navbar .fa:hover, .o_main_navbar .oi:hover, .o_main_navbar i:hover'
    )
    menu_text_color = fields.Char(string='Texto de menú lateral', default='#111827', tracking=True)
    menu_hover_bg_color = fields.Char(string='Hover de menú lateral', default='#E5E7EB', tracking=True)
    menu_hover_text_color = fields.Char(string='Texto hover de menú lateral', default='#111827', tracking=True)
    menu_active_text_color = fields.Char(
        string='Texto activo menú lateral',
        default='#111827',
        tracking=True,
        help='Afecta: .o_menu_sections .o_menu_entry_lvl_1.active > a'
    )
    dropdown_bg_color = fields.Char(
        string='Fondo dropdowns',
        default='#FFFFFF',
        tracking=True,
        help='Afecta: .dropdown-menu, .o-dropdown--menu'
    )
    dropdown_text_color = fields.Char(
        string='Texto dropdowns',
        default='#111827',
        tracking=True,
        help='Afecta: .dropdown-menu .dropdown-item, .o-dropdown--menu .dropdown-item'
    )
    dropdown_hover_bg_color = fields.Char(
        string='Hover dropdowns',
        default='#F3F4F6',
        tracking=True,
        help='Afecta hover: .dropdown-menu .dropdown-item:hover, .o-dropdown--menu .dropdown-item:hover'
    )
    input_bg_color = fields.Char(
        string='Fondo de campos',
        default='#FFFFFF',
        tracking=True,
        help='Afecta: .form-control, .o_input, input, select, textarea'
    )
    input_text_color = fields.Char(
        string='Texto de campos',
        default='#111827',
        tracking=True,
        help='Afecta: .form-control, .o_input, input, select, textarea'
    )
    input_placeholder_color = fields.Char(
        string='Placeholder de campos',
        default='#9CA3AF',
        tracking=True,
        help='Afecta: .form-control::placeholder, input::placeholder, textarea::placeholder'
    )
    table_header_bg_color = fields.Char(
        string='Fondo cabecera de tabla',
        default='#F9FAFB',
        tracking=True,
        help='Afecta: .o_list_view thead th'
    )
    table_header_text_color = fields.Char(
        string='Texto cabecera de tabla',
        default='#374151',
        tracking=True,
        help='Afecta: .o_list_view thead th'
    )
    table_row_hover_bg_color = fields.Char(
        string='Hover fila de tabla',
        default='#F3F4F6',
        tracking=True,
        help='Afecta hover: .o_list_view .o_data_row:hover'
    )
    icon_color = fields.Char(string='Color de iconos', default='#6B7280', tracking=True)
    icon_hover_color = fields.Char(string='Hover de iconos', default='#1F6FEB', tracking=True)
    hover_color = fields.Char(string='Color hover general', default='#E5E7EB', tracking=True)
    active_color = fields.Char(string='Color activo', default='#DBEAFE', tracking=True)

    @api.model
    def _get_effective_config_for_user(self, user):
        configs = self.search([
            ('is_active', '=', True),
        ], order='priority desc, id desc')
        if not configs:
            return self.browse()
        return configs[:1]

    @api.model
    def _get_backend_css_for_user(self, user):
        config = self._get_effective_config_for_user(user)
        if not config:
            return ''

        vars_map = {
            '--dsc-primary': config.primary_color,
            '--dsc-secondary': config.secondary_color,
            '--dsc-accent': config.accent_color,
            '--dsc-bg': config.background_color,
            '--dsc-card-bg': config.card_bg_color,
            '--dsc-sidebar-bg': config.sidebar_bg_color,
            '--dsc-navbar-bg': config.navbar_bg_color,
            '--dsc-text': config.text_color,
            '--dsc-text-muted': config.muted_text_color,
            '--dsc-border': config.border_color,
            '--dsc-success': config.success_color,
            '--dsc-warning': config.warning_color,
            '--dsc-danger': config.danger_color,
            '--dsc-info': config.info_color,
            '--dsc-link': config.link_color,
            '--dsc-link-hover': config.link_hover_color,
            '--dsc-btn-text': config.button_text_color,
            '--dsc-btn-secondary-text': config.button_secondary_text_color,
            '--dsc-navbar-text': config.navbar_text_color,
            '--dsc-navbar-hover-bg': config.navbar_hover_bg_color,
            '--dsc-navbar-hover-text': config.navbar_hover_text_color,
            '--dsc-navbar-icon': config.navbar_icon_color,
            '--dsc-navbar-icon-hover': config.navbar_icon_hover_color,
            '--dsc-menu-text': config.menu_text_color,
            '--dsc-menu-hover-bg': config.menu_hover_bg_color,
            '--dsc-menu-hover-text': config.menu_hover_text_color,
            '--dsc-menu-active-text': config.menu_active_text_color,
            '--dsc-dropdown-bg': config.dropdown_bg_color,
            '--dsc-dropdown-text': config.dropdown_text_color,
            '--dsc-dropdown-hover-bg': config.dropdown_hover_bg_color,
            '--dsc-input-bg': config.input_bg_color,
            '--dsc-input-text': config.input_text_color,
            '--dsc-input-placeholder': config.input_placeholder_color,
            '--dsc-table-head-bg': config.table_header_bg_color,
            '--dsc-table-head-text': config.table_header_text_color,
            '--dsc-table-row-hover-bg': config.table_row_hover_bg_color,
            '--dsc-icon': config.icon_color,
            '--dsc-icon-hover': config.icon_hover_color,
            '--dsc-hover': config.hover_color,
            '--dsc-active': config.active_color,
        }

        css_lines = [':root {']
        for var_name, value in vars_map.items():
            if value:
                css_lines.append(f'  {var_name}: {value};')
        css_lines.append('}')

        css_lines.extend([
            '/* Fondos y estructura base */',
            '.o_web_client {',
            '  background-color: var(--dsc-bg);',
            '  color: var(--dsc-text);',
            '}',
            '.o_action_manager {',
            '  background-color: var(--dsc-bg);',
            '}',
            '',
            '/* Barra de navegación */',
            '.o_main_navbar {',
            '  background-color: var(--dsc-navbar-bg) !important;',
            '  border-bottom: 1px solid var(--dsc-border) !important;',
            '}',
            '.o_main_navbar .navbar-brand, .o_main_navbar .nav-link {',
            '  color: var(--dsc-navbar-text) !important;',
            '}',
            '.o_main_navbar .nav-link:hover, .o_main_navbar .dropdown-toggle:hover {',
            '  background-color: var(--dsc-navbar-hover-bg) !important;',
            '  color: var(--dsc-navbar-hover-text) !important;',
            '}',
            '.o_main_navbar .fa, .o_main_navbar .oi, .o_main_navbar i {',
            '  color: var(--dsc-navbar-icon) !important;',
            '}',
            '.o_main_navbar .fa:hover, .o_main_navbar .oi:hover, .o_main_navbar i:hover {',
            '  color: var(--dsc-navbar-icon-hover) !important;',
            '}',
            '.dropdown-menu, .o-dropdown--menu {',
            '  background-color: var(--dsc-dropdown-bg) !important;',
            '}',
            '.dropdown-menu .dropdown-item, .o-dropdown--menu .dropdown-item {',
            '  color: var(--dsc-dropdown-text) !important;',
            '}',
            '.dropdown-menu .dropdown-item:hover, .o-dropdown--menu .dropdown-item:hover {',
            '  background-color: var(--dsc-dropdown-hover-bg) !important;',
            '}',
            '',
            '/* Menú lateral */',
            '.o_menu_sections, .o-app {',
            '  background-color: var(--dsc-sidebar-bg) !important;',
            '}',
            '.o_menu_sections .o_menu_entry_lvl_1 > a {',
            '  color: var(--dsc-menu-text) !important;',
            '}',
            '.o_menu_sections .o_menu_entry_lvl_1 > a:hover, .o_menu_sections .o_menu_entry_lvl_2 > a:hover {',
            '  background-color: var(--dsc-menu-hover-bg) !important;',
            '  color: var(--dsc-menu-hover-text) !important;',
            '}',
            '.o_menu_sections .o_menu_entry_lvl_1.active > a {',
            '  background-color: var(--dsc-active) !important;',
            '  color: var(--dsc-menu-active-text) !important;',
            '}',
            '.o_menu_sections .o_menu_entry_lvl_2 > a {',
            '  color: var(--dsc-text-muted) !important;',
            '}',
            '',
            '/* Tarjetas y vistas */',
            '.o_form_view, .o_list_view, .o_kanban_view {',
            '  background-color: var(--dsc-card-bg);',
            '}',
            '.o_kanban_record {',
            '  background-color: var(--dsc-card-bg);',
            '  border-color: var(--dsc-border);',
            '}',
            '.o_form_sheet {',
            '  background-color: var(--dsc-card-bg);',
            '}',
            '',
            '/* Botones primarios */',
            '.btn-primary, .btn-primary:hover, .btn-primary:active {',
            '  background-color: var(--dsc-primary) !important;',
            '  border-color: var(--dsc-primary) !important;',
            '  color: var(--dsc-btn-text) !important;',
            '}',
            '',
            '/* Botones secundarios */',
            '.btn-secondary {',
            '  background-color: var(--dsc-secondary) !important;',
            '  border-color: var(--dsc-secondary) !important;',
            '  color: var(--dsc-btn-secondary-text) !important;',
            '}',
            '',
            '/* Estados de éxito */',
            '.alert-success, .badge-success, .text-success {',
            '  background-color: var(--dsc-success) !important;',
            '  color: white !important;',
            '  border-color: var(--dsc-success) !important;',
            '}',
            '',
            '/* Estados de advertencia */',
            '.alert-warning, .badge-warning, .text-warning {',
            '  background-color: var(--dsc-warning) !important;',
            '  color: white !important;',
            '  border-color: var(--dsc-warning) !important;',
            '}',
            '',
            '/* Estados de peligro */',
            '.alert-danger, .badge-danger, .text-danger {',
            '  background-color: var(--dsc-danger) !important;',
            '  color: white !important;',
            '  border-color: var(--dsc-danger) !important;',
            '}',
            '',
            '/* Estados informativos */',
            '.alert-info, .badge-info, .text-info {',
            '  background-color: var(--dsc-info) !important;',
            '  color: white !important;',
            '  border-color: var(--dsc-info) !important;',
            '}',
            '',
            '/* Enlaces */',
            'a:not(.btn):not(.nav-link):not(.breadcrumb-item) {',
            '  color: var(--dsc-link) !important;',
            '}',
            'a:not(.btn):not(.nav-link):not(.breadcrumb-item):hover {',
            '  color: var(--dsc-link-hover) !important;',
            '  text-decoration: underline;',
            '}',
            '',
            '/* Campos de formulario */',
            '.form-control, .o_input, input:not([type=hidden]):not([type=submit]):not([type=button]), select, textarea {',
            '  border-color: var(--dsc-border) !important;',
            '  color: var(--dsc-input-text) !important;',
            '  background-color: var(--dsc-input-bg) !important;',
            '}',
            '.form-control::placeholder, input::placeholder, textarea::placeholder {',
            '  color: var(--dsc-input-placeholder) !important;',
            '}',
            '.form-control:focus, .o_input:focus {',
            '  border-color: var(--dsc-accent) !important;',
            '  box-shadow: 0 0 0 0.2rem var(--dsc-accent) !important;',
            '}',
            '',
            '/* Etiquetas y textos */',
            '.o_form_label {',
            '  color: var(--dsc-text) !important;',
            '}',
            '.text-muted {',
            '  color: var(--dsc-text-muted) !important;',
            '}',
            '.fa, .oi, .o_icon, .o_field_widget .btn .fa {',
            '  color: var(--dsc-icon) !important;',
            '}',
            '.fa:hover, .oi:hover, .o_icon:hover, .o_field_widget .btn:hover .fa {',
            '  color: var(--dsc-icon-hover) !important;',
            '}',
            '.o_required_modifier .o_form_label::after {',
            '  color: var(--dsc-danger);',
            '}',
            '',
            '/* Bordes */',
            '.o_list_view .o_data_row, .o_list_view thead {',
            '  border-color: var(--dsc-border) !important;',
            '}',
            '.o_list_view thead th {',
            '  background-color: var(--dsc-table-head-bg) !important;',
            '  color: var(--dsc-table-head-text) !important;',
            '}',
            '.o_list_view .o_data_row:hover {',
            '  background-color: var(--dsc-table-row-hover-bg) !important;',
            '}',
            'hr {',
            '  border-color: var(--dsc-border) !important;',
            '}',
            '',
            '/* Focus visible */',
            '*:focus-visible {',
            '  outline: 2px solid var(--dsc-accent) !important;',
            '  outline-offset: 2px;',
            '}',
            '',
            '/* Accent color para elementos highlight */',
            '.badge-primary, .o_tag {',
            '  background-color: var(--dsc-accent) !important;',
            '  color: white !important;',
            '}',
        ])

        if config.theme_mode == 'dark':
            css_lines.extend([
                ':root {',
                '  color-scheme: dark;',
                '}',
            ])

        return '\n'.join(css_lines)

    @api.constrains(
        'primary_color', 'secondary_color', 'accent_color', 'background_color',
        'card_bg_color', 'sidebar_bg_color', 'navbar_bg_color', 'text_color',
        'muted_text_color', 'border_color', 'success_color', 'warning_color',
        'danger_color', 'info_color', 'link_color', 'link_hover_color',
        'button_text_color', 'button_secondary_text_color', 'navbar_text_color',
        'navbar_hover_bg_color', 'navbar_hover_text_color', 'navbar_icon_color',
        'navbar_icon_hover_color', 'menu_text_color', 'menu_hover_bg_color',
        'menu_hover_text_color', 'menu_active_text_color', 'dropdown_bg_color',
        'dropdown_text_color', 'dropdown_hover_bg_color', 'input_bg_color',
        'input_text_color', 'input_placeholder_color', 'table_header_bg_color',
        'table_header_text_color', 'table_row_hover_bg_color', 'icon_color',
        'icon_hover_color', 'hover_color', 'active_color'
    )
    def _check_hex_colors(self):
        hex_pattern = re.compile(r'^#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$')
        color_fields = [
            'primary_color', 'secondary_color', 'accent_color', 'background_color',
            'card_bg_color', 'sidebar_bg_color', 'navbar_bg_color', 'text_color',
            'muted_text_color', 'border_color', 'success_color', 'warning_color',
            'danger_color', 'info_color', 'link_color', 'link_hover_color',
            'button_text_color', 'button_secondary_text_color', 'navbar_text_color',
            'navbar_hover_bg_color', 'navbar_hover_text_color', 'navbar_icon_color',
            'navbar_icon_hover_color', 'menu_text_color', 'menu_hover_bg_color',
            'menu_hover_text_color', 'menu_active_text_color', 'dropdown_bg_color',
            'dropdown_text_color', 'dropdown_hover_bg_color', 'input_bg_color',
            'input_text_color', 'input_placeholder_color', 'table_header_bg_color',
            'table_header_text_color', 'table_row_hover_bg_color', 'icon_color',
            'icon_hover_color', 'hover_color', 'active_color'
        ]
        for record in self:
            for field_name in color_fields:
                value = record[field_name]
                if value and not hex_pattern.match(value):
                    raise ValidationError(
                        f'El valor "{value}" en "{record._fields[field_name].string}" no es un color hexadecimal válido.'
                    )

    def action_set_active(self):
        self.ensure_one()
        self.search([('id', '!=', self.id), ('is_active', '=', True)]).write({'is_active': False})
        self.is_active = True
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def action_deactivate_all(self):
        self.search([('is_active', '=', True)]).write({'is_active': False})
        return {'type': 'ir.actions.client', 'tag': 'reload'}
