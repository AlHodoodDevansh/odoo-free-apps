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

{
    'name': 'Sale → Project',
    'version': '19.0.0.0.0',
    'summary': 'Automatically create Project and Project location when a Sale Order is confirmed',
    'description': 'Create project on sale order confirmation and create location.',
    'category': 'Sales',
    'author': 'Alhodood Technologies',
    'company': 'Alhodood Technologies',
    'maintainer': 'Alhodood Technologies',
    'depends': ['sale_management', 'project'],
    'data': [
        'data/data.xml', 
        'views/sale_order_views.xml', 
        'views/project_views.xml'
    ],
    'assets': {},
    'images': ['static/description/banner.gif'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
