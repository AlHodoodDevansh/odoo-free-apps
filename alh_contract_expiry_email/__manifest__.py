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
{
    'name': 'Contract Expiry Email',
    'version': '19.0.0.0.0',
    'category': 'Human Resources',
    'summary': (
        'Automatically sends an email reminder 70 days before an employee’s '
        'contract expiry date.'
    ),
    'description': (
        'Automatically sends an email reminder 70 days before an employee’s '
        'contract expiry date.'
    ),
    'company': 'Alhodood Technologies',
    'maintainer': 'Alhodood Technologies',
    'support': 'sales@alhodood.com',
    'website': 'https://www.alhodood.com',
    'author': 'Alhodood Technologies',
    'depends': [
        'hr_payroll_community',],
    'data': [
        'data/hr_contract_expiry_data.xml',
    ],
    'assets': {},
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
