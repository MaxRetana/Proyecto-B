{
    "name": "Sitio Web Consultas Psicológicas",
    "summary": "Módulo para gestionar consultas psicológicas a través de un sitio web",
    "description": 
        """
        Este módulo permite gestionar las consultas psicológicas a través de un sitio web, incluyendo la creación de citas, el seguimiento de pacientes y la gestión de historiales clínicos. Es ideal para clínicas psicológicas, consultorios privados y profesionales de la salud mental que desean organizar su trabajo de manera eficiente y ofrecer una experiencia en línea a sus pacientes.
        """,
    "author": ["MaxRetana"],
    "category": "base",
    "version": "19.1.0",
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "depends": ["base", "website", "psychological_consultation"],
    "data": [
        "security/groups.xml",
        "views/psychological_consultation_calendar_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "psychological_consultation_web_site/static/src/css/consultations_calendar.css",
            "psychological_consultation_web_site/static/src/js/consultations_calendar.js",
        ],
    },
}
