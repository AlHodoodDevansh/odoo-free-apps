# -*- coding: utf-8 -*-
#############################################################################
#    Alhodood Technologies.
#
#    Copyright (C) 2024-TODAY Alhodood Technologies(<https://www.alhodood.com>)
#    Author: Alhodood Technologies(<https://www.alhodood.com>)
#
#    You can modify it under the terms of the GNU Affero General Public License
#    (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License (AGPL v3) for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one(
        'project.project',
        string='Related Project',
        readonly=True,
        copy=False
    )

    create_project_on_confirm = fields.Boolean(
        string='Create Project on Confirmation',
        default=True,
        help=(
            "If checked, a project will be created when confirming "
            "this Sales Order."
        ),
    )

    project_name = fields.Char(
        string='Project Name',
        help=(
            "If provided, this name will be used for the project "
            "created on confirmation."
        ),
    )

    @api.onchange('partner_id', 'create_project_on_confirm')
    def _onchange_project_name_default(self):
        """Default project name to customer name when partner is selected."""
        for order in self:
            if order.create_project_on_confirm and order.partner_id:
                order.project_name = order.partner_id.name

    def _prepare_project_vals(self):
        """Base values used to create project."""
        self.ensure_one()
        return {
            'partner_id': self.partner_id.id or False,
            'sale_order_id': self.id,
            'privacy_visibility': 'followers',
        }

    def action_confirm(self):
        """Confirm SO and create project with sequence code + customer name."""
        res = super(SaleOrder, self).action_confirm()

        for order in self.filtered(lambda o: o.create_project_on_confirm 
            and not o.project_id):
            order._create_project_with_sequence()
        return res

    def _create_project_with_sequence(self):
        """Create project with code + name pattern '<code>_<customer>'."""
        self.ensure_one()
        Project = self.env['project.project'].sudo()

        project_code = self.env['ir.sequence'].next_by_code('project.project.code') or _('New')
        project_name = f"{project_code} - {self.partner_id.name or ''}"

        project_vals = self._prepare_project_vals()
        project_vals.update({
            'project_code': project_code,
            'name': project_name,
        })
        project = Project.create(project_vals)
        self.sudo().write({'project_id': project.id})
        self.message_post(body=_("Project created: %s") % project.display_name)

    def action_cancel(self):
        """
        Cancel the Sale Order and delete its related project if it was auto-created.
        """
        for order in self:
            if order.project_id and order.create_project_on_confirm:
                try:
                    project_name = order.project_id.display_name
                    order.project_id.sudo().unlink()
                    order.message_post(
                        body=_(
                            "Related project %s deleted due to order cancellation."
                        ) % project_name
                    )
                except Exception:
                    order.message_post(
                        body=_(
                            "Could not delete project %s due to dependencies."
                        ) % project_name
                    )
        return super(SaleOrder, self).action_cancel()

