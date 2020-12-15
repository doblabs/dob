# This file exists within 'dob':
#
#   https://github.com/tallybark/dob
#
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
#
# 'dob' is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License  as  published by the Free Software Foundation,
# either version 3  of the License,  or  (at your option)  any   later    version.
#
# 'dob' is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY  or  FITNESS FOR A PARTICULAR
# PURPOSE.  See  the  GNU General Public License  for  more details.
#
# You can find the GNU General Public License reprinted in the file titled 'LICENSE',
# or visit <http://www.gnu.org/licenses/>.

from gettext import gettext as _

from easy_as_pypi_termio import attr, coloring

__all__ = (
    'help_header_format',
)


def help_header_format(text):
    return '{underlined}{text}{reset}{optolon}'.format(
        underlined=attr('underlined'),
        text=text,
        reset=attr('reset'),
        optolon=not coloring() and _(':') or '',
    )

