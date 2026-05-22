# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request


class PortalAttendanceSync(http.Controller):

    @http.route(
        "/portal/attendance/toggle",
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
    )
    def portal_attendance_toggle(self, **post):
        user = request.env.user
        group = "portal_attendance_sync.group_portal_attendance"

        # Verificamos que el usuario tenga el grupo y un empleado asociado
        if user.has_group(group) and user.employee_id:
            # Ejecución con sudo para evitar restricciones de acceso del portal
            # _attendance_action_change es el método estándar de Odoo para conmutar entrada/salida
            user.employee_id.sudo()._attendance_action_change()

        # Redirección segura a la página anterior o al home del portal
        return request.redirect(request.httprequest.referrer or "/my/home")
