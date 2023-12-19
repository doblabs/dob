# This file exists within 'dob':
#
#   https://github.com/tallybark/dob
#
# Copyright © 2019-2020 Landon Bouma. All rights reserved.
#
# This program is free software:  you can redistribute it  and/or  modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3  of the License,  or  (at your option)  any later version  (GPLv3+).
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY;  without even the implied warranty of MERCHANTABILITY or  FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU  General  Public  License  for  more  details.
#
# If you lost the GNU General Public License that ships with this software
# repository (read the 'LICENSE' file), see <http://www.gnu.org/licenses/>.

from config_decorator import KeyChainedValue

from .. import __package_name__

# Set the prefix used for specifying config via environs,
# e.g., `DOB_EDITOR_CENTERED=false dob edit`:
#  KeyChainedValue._envvar_prefix = 'DOB_'
KeyChainedValue._envvar_prefix = '{}_'.format(__package_name__.upper())

