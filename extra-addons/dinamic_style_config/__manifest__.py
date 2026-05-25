{
	"name": "Configuración Dinámica de Estilos",
	"summary": "Personaliza dinámicamente colores y tipografía del backend",
	"description": "Permite definir temas visuales para el backend de Odoo con alcance por usuario, grupo, empresa o global.",
	"author": ["MaxRetana"],
	"category": "Tools",
	"version": "19.1.0",
	"license": "LGPL-3",
	"depends": ["base", "web", "mail"],
	"data": [
		"security/ir.model.access.csv",
		"views/dinamic_style_config_views.xml",
		"views/theme_loader_template.xml",
	],
	"assets": {
		"web.assets_backend": [
			"dinamic_style_config/static/src/js/theme_loader.js",
		],
	},
	"installable": True,
	"application": False,
}
