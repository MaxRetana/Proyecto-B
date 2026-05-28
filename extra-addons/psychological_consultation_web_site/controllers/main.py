from datetime import datetime, timedelta

import pytz

from odoo import fields, http
from odoo.http import request


class PsychologicalConsultationWebsiteController(http.Controller):

    def _get_user_tz(self):
        return pytz.timezone('America/Mexico_City')

    def _get_available_time_slots(self, request_date):
        try:
            date_obj = datetime.strptime(request_date, '%Y-%m-%d').date()
        except (TypeError, ValueError):
            return []

        user_tz = self._get_user_tz()

        weekday = str(date_obj.weekday())
        schedule_lines = request.env['time.work.consultation.line'].sudo().search([
            ('day_of_week', '=', weekday),
        ])

        candidate_slots = set()
        for line in schedule_lines:
            start_minutes = int(round((line.start_time or 0.0) * 60))
            end_minutes = int(round((line.end_time or 0.0) * 60))
            if end_minutes <= start_minutes:
                continue

            # Se generan inicios de cita de 1 hora dentro de cada tramo.
            current = start_minutes
            while current + 60 <= end_minutes:
                hour = current // 60
                minute = current % 60
                candidate_slots.add(f'{hour:02d}:{minute:02d}')
                current += 60

        local_day_start = user_tz.localize(datetime.combine(date_obj, datetime.min.time()))
        local_day_end = local_day_start + timedelta(days=1)
        utc_day_start = local_day_start.astimezone(pytz.UTC).replace(tzinfo=None)
        utc_day_end = local_day_end.astimezone(pytz.UTC).replace(tzinfo=None)

        existing_consultations = request.env['psychological.consultation'].sudo().search([
            ('date_consultation', '>=', fields.Datetime.to_string(utc_day_start)),
            ('date_consultation', '<', fields.Datetime.to_string(utc_day_end)),
            ('state', '!=', 'cancelled'),
        ])

        occupied_slots = {
            fields.Datetime.context_timestamp(request.env.user, consultation.date_consultation).strftime('%H:%M')
            for consultation in existing_consultations
            if consultation.date_consultation
        }

        return sorted([slot for slot in candidate_slots if slot not in occupied_slots])

    @http.route(
        '/',
        type='http',
        auth='public',
        website=True,
        methods=['GET', 'POST'],
    )
    def consultations_home_page(self, **post):
        user = request.env.user
        employee = request.env['hr.employee'].sudo().search(['|', ('user_id', '=', user.id), ('user_portal_id', '=', user.id)], limit=1)
        is_capturista = user.has_group('psychological_consultation_web_site.group_psychological_consultation_capturista')
        show_patient_selector = is_capturista
        patients = request.env['hr.employee'].sudo().search([
            ('type_of_psychologist_consultation', '=', 'patient'),
            ('user_portal_id', '!=', False),
        ], order='name') if is_capturista else request.env['hr.employee']
        is_portal = user.has_group('base.group_portal')
        is_admin = user.has_group('base.group_system')
        is_public = user.has_group('base.group_public')

        values = {
            'is_public': is_public,
            'is_portal': is_portal,
            'is_admin': is_admin,
            'is_capturista': is_capturista,
            'error_message': False,
            'success_message': False,
            'show_patient_selector': show_patient_selector,
            'patients': patients,
            'form_data': {
                'request_date': post.get('request_date', ''),
                'request_time': post.get('request_time', ''),
                'notes': post.get('notes', ''),
                'pacient_id': post.get('pacient_id', '') if show_patient_selector else (employee.id if employee else ''),
            },
        }

        if request.httprequest.method == 'POST':
            if not is_portal and not is_admin and not is_capturista:
                if is_public:
                    return request.redirect('/web/login?redirect=/')
                values['error_message'] = 'Solo usuarios portal autenticados pueden solicitar consultas.'
                return request.render('psychological_consultation_web_site.consultations_home_page', values)

            request_date = (post.get('request_date') or '').strip()
            request_time = (post.get('request_time') or '').strip()
            notes = (post.get('notes') or '').strip()
            pacient_id = (post.get('pacient_id') or '').strip()

            if not request_date or not request_time:
                values['error_message'] = 'Debes indicar fecha y una hora disponible para la consulta.'
                return request.render('psychological_consultation_web_site.consultations_home_page', values)

            if show_patient_selector and not pacient_id:
                values['error_message'] = 'Debes seleccionar un paciente para crear la consulta.'
                return request.render('psychological_consultation_web_site.consultations_home_page', values)

            pacient_employee = employee
            if show_patient_selector:
                try:
                    pacient_employee = request.env['hr.employee'].sudo().browse(int(pacient_id)).exists()
                except (TypeError, ValueError):
                    pacient_employee = request.env['hr.employee']

                if not pacient_employee or pacient_employee.type_of_psychologist_consultation != 'patient':
                    values['error_message'] = 'El paciente seleccionado no es valido.'
                    return request.render('psychological_consultation_web_site.consultations_home_page', values)

            if not pacient_employee and not show_patient_selector:
                values['error_message'] = 'Tu usuario no tiene un empleado vinculado. Contacta al administrador.'
                return request.render('psychological_consultation_web_site.consultations_home_page', values)

            available_slots = self._get_available_time_slots(request_date)
            if request_time not in available_slots:
                values['error_message'] = 'La hora seleccionada ya no esta disponible. Elige otra opcion.'
                return request.render('psychological_consultation_web_site.consultations_home_page', values)

            try:
                user_tz = self._get_user_tz()
                local_datetime = user_tz.localize(datetime.strptime(f'{request_date} {request_time}:00', '%Y-%m-%d %H:%M:%S'))
                utc_datetime = local_datetime.astimezone(pytz.UTC).replace(tzinfo=None)
            except (TypeError, ValueError):
                values['error_message'] = 'La fecha ingresada no es valida.'
                return request.render('psychological_consultation_web_site.consultations_home_page', values)

            request.env['psychological.consultation'].sudo().create({
                'pacient_id': pacient_employee.id,
                'date_consultation': fields.Datetime.to_string(utc_datetime),
                'notes': notes,
                'state': 'draft',
            })

            values['success_message'] = 'Solicitud enviada en estado borrador. Te contactaremos para confirmar.'
            values['form_data'] = {
                'request_date': '',
                'request_time': '',
                'notes': '',
                'pacient_id': pacient_employee.id,
            }

        return request.render('psychological_consultation_web_site.consultations_home_page', values)

    @http.route(
        '/psychological/consultations/calendar',
        type='http',
        auth='user',
        website=True,
    )
    def consultations_calendar_page(self, **kwargs):
        return request.render('psychological_consultation_web_site.consultations_calendar_page')

    @http.route(
        '/psychological/consultations/calendar/events',
        type='http',
        auth='user',
        methods=['GET'],
        website=True,
    )
    def consultations_calendar_events(self, **kwargs):
        consultations = request.env['psychological.consultation'].sudo().search(
            [
                ('state', 'in', ['confirmed', 'done']),
                ('date_consultation', '!=', False),
                ('pacient_id.user_portal_id', '=', request.env.user.id) if request.env.user.has_group('base.group_portal') else ('psycologist_id.user_id', '=', request.env.user.id),
            ],
            order='date_consultation asc',
        )

        state_labels = dict(request.env['psychological.consultation']._fields['state'].selection)
        mexico_tz = self._get_user_tz()
        events = []
        for consultation in consultations:
            patient_name = consultation.pacient_id.name or 'Paciente sin nombre'
            psychologist_name = consultation.psycologist_id.name or 'Psicologo sin asignar'
            
            # Convertir la fecha de UTC a zona horaria de México
            utc_dt = pytz.UTC.localize(consultation.date_consultation)
            mexico_dt = utc_dt.astimezone(mexico_tz)
            
            # Formato ISO 8601 con zona horaria para que JavaScript lo interprete correctamente
            iso_format = mexico_dt.isoformat()
            
            events.append({
                'id': consultation.id,
                'name': consultation.name,
                'title': f"{patient_name} con {psychologist_name}",
                'state': consultation.state,
                'state_label': state_labels.get(consultation.state, consultation.state),
                'patient_name': patient_name,
                'psychologist_name': psychologist_name,
                'notes': consultation.notes or '',
                'date_label': mexico_dt.strftime('%d/%m/%Y %H:%M'),
                'date_consultation': iso_format,
            })

        return request.make_json_response({'events': events})

    @http.route(
        '/psychological/consultations/available-hours',
        type='http',
        auth='user',
        methods=['GET'],
        website=True,
    )
    def consultations_available_hours(self, **kwargs):
        request_date = (kwargs.get('date') or '').strip()
        slots = self._get_available_time_slots(request_date)
        return request.make_json_response({'slots': slots})
