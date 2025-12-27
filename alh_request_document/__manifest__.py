# -*- coding: utf-8 -*-
#############################################################################

#    Alhodood Technologies.
#
#    Copyright (C) 2025-TODAY Alhodood Technologies(<https://www.alhodood.com>)
#    Author: Alhodood Technologies(<https://www.alhodood.com>)
#
# You can modify it under the terms of the GNU Affero General Public License
# (AGPL v3), Version 3.
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
{
    'name': 'Request Document',
    'version': '19.0.0.0.0',
    'category': 'Human Resources',
    'summary': ('Employee document request management with approvals and ' 
        'alerts.'),
    'description': (
        'This module allows employees to submit document requests that are '
        'reviewed and approved by authorized users. Approvers receive ' 
        'automatic email alerts, and employees are notified of the approval '
        'or rejection. Document types are configurable, and all actions are '
        'tracked through chatter for transparency and compliance.'
    ),
    'company': 'Alhodood Technologies',
    'maintainer': 'Alhodood Technologies',
    'support': 'sales@alhodood.com',
    'website': 'https://www.alhodood.com',
    'author': 'Alhodood Technologies',
    'depends': [
        'hr',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/request_document.xml',
        'wizard/reject_reason.xml',
    ],
    'images': ['static/description/banner.gif'],
    'assets': {},
    # 'price': 5.0,
    # 'currency': 'USD',
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
