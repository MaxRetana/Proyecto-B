{
    "name": "Consultas Psicológicas",
    "summary": "Módulo para gestionar consultas psicológicas",
    "description": 
        """
        Este módulo permite gestionar las consultas psicológicas, incluyendo la creación de citas, el seguimiento de pacientes y la gestión de historiales clínicos. Es ideal para clínicas psicológicas, consultorios privados y profesionales de la salud mental que desean organizar su trabajo de manera eficiente.
        """,
    "author": ["MaxRetana"],
    "category": "base",
    "version": "19.1.0",
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "depends": ["base", "mail", "hr"],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "security/record_rule.xml",
        "views/hr_employee_views.xml",
        "views/psychological_consultation_views.xml",
        "views/psychological_consultation_read_views.xml",
        "views/time_work_consultation_views.xml",
        "views/time_work_consultation__lines_views.xml",
    ],
}
