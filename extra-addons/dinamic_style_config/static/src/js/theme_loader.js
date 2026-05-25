/** @odoo-module **/

import { registry } from "@web/core/registry";

const dynamicThemeLoaderService = {
    start() {
        const existing = document.getElementById("o_dynamic_style_config_theme");
        if (existing) {
            return;
        }

        const link = document.createElement("link");
        link.id = "o_dynamic_style_config_theme";
        link.rel = "stylesheet";
        link.type = "text/css";
        link.href = `/dinamic_style_config/theme.css?v=${Date.now()}`;
        document.head.appendChild(link);
    },
};

registry.category("services").add("dynamic_style_config_theme_loader", dynamicThemeLoaderService);
