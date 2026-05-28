(function () {
    'use strict';

    const MONTH_LABEL = document.getElementById('pc-current-month');
    const GRID = document.getElementById('pc-calendar-grid');
    const REQUEST_DATE_INPUT = document.getElementById('request_date');
    const REQUEST_TIME_SELECT = document.getElementById('request_time');
    const REQUEST_TIME_HELP = document.getElementById('request_time_help');

    const WEEK_DAYS = ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom'];
    const eventsByDay = new Map();
    let visibleMonth = new Date();
    visibleMonth.setDate(1);

    const toDateKey = (dateObj) => {
        const year = dateObj.getFullYear();
        const month = String(dateObj.getMonth() + 1).padStart(2, '0');
        const day = String(dateObj.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    const parseConsultationDate = (rawDate) => {
        if (!rawDate) {
            return null;
        }
        // Para formato ISO 8601, extraer la fecha sin conversión de zona horaria
        const dateMatch = rawDate.match(/(\d{4})-(\d{2})-(\d{2})/);
        if (!dateMatch) {
            return null;
        }
        // Crear una fecha local (no UTC) usando los componentes de la fecha
        const year = parseInt(dateMatch[1], 10);
        const month = parseInt(dateMatch[2], 10) - 1; // Los meses de JavaScript son 0-indexados
        const day = parseInt(dateMatch[3], 10);
        return new Date(year, month, day);
    };

    const buildHeader = () => {
        const headerFragment = document.createDocumentFragment();
        WEEK_DAYS.forEach((dayName) => {
            const dayCell = document.createElement('div');
            dayCell.className = 'pc-week-day';
            dayCell.textContent = dayName;
            headerFragment.appendChild(dayCell);
        });
        if (GRID) {
            GRID.appendChild(headerFragment);
        }
    };

    const createEventBadge = (eventData) => {
        const badge = document.createElement('div');
        badge.className = `pc-event pc-state-${eventData.state}`;

        // Extraer la hora directamente del formato ISO 8601 sin conversión de zona horaria
        let timeLabel = '--:--';
        if (eventData.date_consultation) {
            const isoMatch = eventData.date_consultation.match(/(\d{2}):(\d{2}):/);
            if (isoMatch) {
                timeLabel = `${isoMatch[1]}:${isoMatch[2]}`;
            }
        }

        badge.title = `${eventData.state_label} - ${eventData.title}`;
        badge.textContent = `${timeLabel} - ${eventData.title}`;
        return badge;
    };

    const createDayCell = (dateObj, isMuted) => {
        const dayCell = document.createElement('div');
        dayCell.className = `pc-day ${isMuted ? 'pc-day-muted' : ''}`;

        const dayNumber = document.createElement('div');
        dayNumber.className = 'pc-day-number';
        dayNumber.textContent = String(dateObj.getDate());
        dayCell.appendChild(dayNumber);

        const eventsKey = toDateKey(dateObj);
        const dayEvents = eventsByDay.get(eventsKey) || [];

        if (dayEvents.length) {
            const eventsContainer = document.createElement('div');
            eventsContainer.className = 'pc-day-events';
            dayEvents.forEach((eventData) => {
                eventsContainer.appendChild(createEventBadge(eventData));
            });
            dayCell.appendChild(eventsContainer);
        }

        return dayCell;
    };

    const renderMonth = () => {
        if (!GRID || !MONTH_LABEL) {
            return;
        }

        GRID.innerHTML = '';

        const monthTitle = visibleMonth.toLocaleDateString('es-CR', {
            month: 'long',
            year: 'numeric',
        });
        MONTH_LABEL.textContent = monthTitle.charAt(0).toUpperCase() + monthTitle.slice(1);

        buildHeader();

        const firstDay = new Date(visibleMonth.getFullYear(), visibleMonth.getMonth(), 1);
        const startWeekday = (firstDay.getDay() + 6) % 7;
        const gridStart = new Date(firstDay);
        gridStart.setDate(firstDay.getDate() - startWeekday);

        for (let index = 0; index < 42; index += 1) {
            const currentDate = new Date(gridStart);
            currentDate.setDate(gridStart.getDate() + index);

            const isMuted = currentDate.getMonth() !== visibleMonth.getMonth();
            GRID.appendChild(createDayCell(currentDate, isMuted));
        }
    };

    const storeEvents = (events) => {
        eventsByDay.clear();

        events.forEach((eventData) => {
            const dateValue = parseConsultationDate(eventData.date_consultation);
            if (!dateValue) {
                return;
            }
            const key = toDateKey(dateValue);
            const existing = eventsByDay.get(key) || [];
            existing.push(eventData);
            existing.sort((left, right) => {
                return String(left.date_consultation).localeCompare(String(right.date_consultation));
            });
            eventsByDay.set(key, existing);
        });
    };

    const setupToolbar = () => {
        if (!GRID) {
            return;
        }
        document.querySelectorAll('.pc-nav-btn').forEach((button) => {
            button.addEventListener('click', () => {
                const action = button.dataset.action;
                const monthOffset = action === 'next' ? 1 : -1;
                visibleMonth.setMonth(visibleMonth.getMonth() + monthOffset);
                renderMonth();
            });
        });
    };

    const loadEvents = async () => {
        if (!GRID || !MONTH_LABEL) {
            return;
        }
        try {
            const response = await fetch('/psychological/consultations/calendar/events', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            });
            const payload = await response.json();
            storeEvents(payload.events || []);
            renderMonth();
        } catch (error) {
            MONTH_LABEL.textContent = 'No fue posible cargar las consultas';
            GRID.innerHTML = '<div class="pc-calendar-error">Intenta de nuevo en unos segundos.</div>';
        }
    };

    const fillTimeOptions = (slots, selectedValue) => {
        if (!REQUEST_TIME_SELECT) {
            return;
        }

        REQUEST_TIME_SELECT.innerHTML = '';

        const emptyOption = document.createElement('option');
        emptyOption.value = '';
        emptyOption.textContent = slots.length
            ? 'Selecciona una hora'
            : 'No hay horas disponibles para esta fecha';
        REQUEST_TIME_SELECT.appendChild(emptyOption);

        slots.forEach((slot) => {
            const option = document.createElement('option');
            option.value = slot;
            option.textContent = slot;
            if (selectedValue && selectedValue === slot) {
                option.selected = true;
            }
            REQUEST_TIME_SELECT.appendChild(option);
        });
    };

    const loadAvailableHours = async (selectedValue) => {
        if (!REQUEST_DATE_INPUT || !REQUEST_TIME_SELECT) {
            return;
        }

        const selectedDate = REQUEST_DATE_INPUT.value;
        if (!selectedDate) {
            fillTimeOptions([], '');
            if (REQUEST_TIME_HELP) {
                REQUEST_TIME_HELP.textContent = 'Selecciona una fecha para ver horas disponibles.';
            }
            return;
        }

        try {
            const response = await fetch(`/psychological/consultations/available-hours?date=${encodeURIComponent(selectedDate)}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            });
            const payload = await response.json();
            const slots = payload.slots || [];
            fillTimeOptions(slots, selectedValue);
            if (REQUEST_TIME_HELP) {
                REQUEST_TIME_HELP.textContent = slots.length
                    ? 'Selecciona una hora dentro del horario de trabajo configurado.'
                    : 'No hay horas disponibles para esta fecha.';
            }
        } catch (error) {
            fillTimeOptions([], '');
            if (REQUEST_TIME_HELP) {
                REQUEST_TIME_HELP.textContent = 'No se pudieron cargar las horas disponibles.';
            }
        }
    };

    const setupRequestForm = () => {
        if (!REQUEST_DATE_INPUT || !REQUEST_TIME_SELECT) {
            return;
        }

        const preselected = REQUEST_TIME_SELECT.dataset.selected || '';
        REQUEST_DATE_INPUT.addEventListener('change', () => {
            loadAvailableHours('');
        });

        loadAvailableHours(preselected);
    };

    setupToolbar();
    loadEvents();
    setupRequestForm();
})();
