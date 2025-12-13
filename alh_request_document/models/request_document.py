# -*- coding: utf-8 -*-
#############################################################################
#
#    Alhodood Technologies.
#    Copyright (C) 2025-TODAY 
#    Alhodood Technologies (https://www.alhodood.com)
#
#    You can modify it under the terms of the GNU Affero General Public
#    License (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#    See the GNU Affero General Public License (AGPL v3) for more details.
#
#############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class DocumentRequest(models.Model):
    _name = 'document.request'
    _description = 'Document Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.user,
        tracking=True
    )

    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee",
        related='user_id.employee_id',
        tracking=True
    )

    name = fields.Char(
        string="Name Of Doc",
        tracking=True
    )
    doc_type = fields.Many2one(
        'request.document.type',
        string="Document Type",
        tracking=False
    )
    reason = fields.Char(string="Reason", tracking=True)
    reject_reason = fields.Char(string="Reject Reason", tracking=True)
    subject = fields.Char(string="Subject", tracking=True)

    state = fields.Selection(
        [
            ('new', 'NEW'),
            ('request', 'Request'),
            ('approved', 'Approved'),
            ('reject', 'Reject'),
        ],
        string="State",
        default='new',
        tracking=True
    )

    # ---------------------------------------------------------
    # BUSINESS METHODS
    # ---------------------------------------------------------

    def request_document(self):
        """Send mail to approvers and mark request as sent."""
        approver_group = self.env.ref(
            'alh_request_document.group_emp_appr'
        )

        approvers = self.env['res.users'].search([
            ('group_ids', 'in', [approver_group.id])
        ])

        if not approvers:
            raise UserError(
                _("No Document Approvers found in the Approver group!")
            )

        logged_user = self.env.user
        subject = _(
            "Document Request Submitted: %s"
        ) % (self.employee_id.name or 'Employee')

        body = f"""
            <p>Hello Document Approver,</p>
            <p>The employee {self.employee_id.name or 'Employee'} 
               has submitted a document request.</p>
            <p><strong>Document Requested:</strong> {self.name}</p>
            <p><strong>Reason:</strong> {self.reason}</p>
            <p>Please review and take necessary action.</p>
            <br/>
            <p>Best Regards,<br/>{logged_user.name}</p>
        """

        for approver in approvers:
            mail_values = {
                'subject': subject,
                'body_html': body,
                'email_to': approver.email,
                'email_from': logged_user.email
                or self.env.company.email,
            }
            mail = self.env['mail.mail'].sudo().create(mail_values)
            mail.send()

        self.state = 'request'

    def approve_request(self):
        """Approve the request and notify the user."""
        if not self.user_id.email:
            raise UserError(_("The requestor does not have an email set!"))
        if not self.env.user.email:
            raise UserError(_("The approver does not have an email set!"))

        subject = _("Document Request Approved: %s") % self.name
        now_str = fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        body = f"""
            <p>Hello {self.user_id.name},</p>
            <p>Your document request has been approved.</p>
            <p><strong>Document Name:</strong> {self.name}</p>
            <p><strong>Approval Date:</strong> {now_str}</p>
            <br/>
            <p>Best Regards,<br/>{self.env.user.name}</p>
        """

        mail_values = {
            'subject': subject,
            'body_html': body,
            'email_to': self.user_id.email,
            'email_from': self.env.user.email,
        }

        mail = self.env['mail.mail'].sudo().create(mail_values)
        mail.send()

        self.state = 'approved'

    def reject_request_add(self):
        """Open popup for rejection feedback."""
        if not self.user_id.email:
            raise UserError(_("The requestor does not have an email set!"))
        if not self.env.user.email:
            raise UserError(_("The approver does not have an email set!"))

        return {
            'name': _('Rejection Feedback'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'rejection.feedback.wizard',
            'target': 'new',
            'context': {'active_id': self.id},
        }


class RequestDocumentType(models.Model):
    _name = 'request.document.type'
    _description = 'Document Type'

    name = fields.Char(string="Document Type", required=True)
    code = fields.Char(string="Code")
    description = fields.Text(string="Description")
