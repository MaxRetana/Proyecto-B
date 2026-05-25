from odoo import http
from odoo.http import request


class DinamicStyleConfigController(http.Controller):
    @http.route('/dinamic_style_config/theme.css', type='http', auth='public', methods=['GET'], csrf=False)
    def dynamic_theme_css(self):
        user = request.env.user
        if not user or user._is_public():
            css = ''
        else:
            css = request.env['dinamic.style.config'].sudo()._get_backend_css_for_user(user)
        headers = [
            ('Content-Type', 'text/css; charset=utf-8'),
            ('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0'),
            ('Pragma', 'no-cache'),
            ('X-Content-Type-Options', 'nosniff'),
        ]
        return request.make_response(css or '', headers=headers)
