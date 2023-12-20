# This file exists within 'dob':
#
#   https://github.com/tallybark/dob
#
# Copyright © 2018-2020 Landon Bouma,  2015-2016 Eric Goller.  All rights reserved.
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

from dob.dob import _license


class TestDobLicenseWrapper(object):
    """Unittests for ``license`` command."""

    def test_dob_license_wrapper(self, capsys):
        """Make sure the license text is actually displayed."""
        _license()
        out, err = capsys.readouterr()
        assert out.startswith("GNU GENERAL PUBLIC LICENSE")
        assert "Version 3, 29 June 2007" in out
