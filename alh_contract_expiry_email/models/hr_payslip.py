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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#    See the GNU Affero General Public License (AGPL v3) for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.constrains('employee_id', 'date_from', 'date_to', 'state', 
        'contract_id')
    def _check_contract_expiry(self):
        """Ensure payroll cannot be processed for expired or closed 
        contracts."""
        for payslip in self:
            contract = payslip.contract_id

            if not contract:
                continue

            if contract.state != 'open':
                raise ValidationError(_(
                    "The contract for employee %s is not open. "
                    "Payroll cannot be processed."
                ) % payslip.employee_id.name)

            if (
                contract.date_end
                and contract.date_end < fields.Date.today()
            ):
                raise ValidationError(_(
                    "The contract for employee %s has expired on %s. "
                    "Payroll cannot be processed."
                ) % (payslip.employee_id.name, contract.date_end))
