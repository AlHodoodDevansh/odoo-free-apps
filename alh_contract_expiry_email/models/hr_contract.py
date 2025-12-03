# -*- coding: utf-8 -*-
#############################################################################
#    Alhodood Technologies.
#
#    Copyright (C) 2025-TODAY Alhodood Technologies
#    (<https://www.alhodood.com>)
#
#    Author: Alhodood Technologies (<https://www.alhodood.com>)
#
#    You can modify it under the terms of the GNU Affero General Public
#    License (AGPL v3), Version 3.
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
from datetime import date, timedelta
from odoo import fields, models, _

class HrContract(models.Model):
    _inherit = 'hr.version'

    def update_state_expiry_mail(self):
        """Send expiry reminder mail for contract or work permit."""
        date_limit = date.today() + timedelta(days=70)

        contracts = self.env['hr.version'].search([
            '|',
            ('date_end', '<=', fields.Date.to_string(date_limit)),
            (
                'employee_id.work_permit_expiration_date',
                '<=',
                fields.Date.to_string(date_limit)
            )
        ])

        for contract in contracts:
            employee = contract.employee_id
            employee_name = employee.name
            contract_name = contract.name

            mail_content = (
                f"Hello {employee_name},<br>"
                f"Your contract <b>{contract_name}</b> will expire "
                f"in <b>70 days</b>."
            )

            hr_manager_group = self.env.ref('hr.group_hr_manager')
            manager_emails = self.env['res.users'].search([
                ('group_ids', 'in', [hr_manager_group.id])
            ]).mapped('email')

            email_to = ', '.join(manager_emails) if manager_emails else ''

            subject = _('%s - Contract Is Going To Expire') % employee_name

            mail_values = {
                'subject': subject,
                'author_id': self.env.user.partner_id.id,
                'body_html': mail_content,
                'email_to': email_to,
            }

            self.env['mail.mail'].sudo().create(mail_values).send()
