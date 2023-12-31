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

from dob import cmds_list


class TestCategories(object):
    """Unittest related to category listings."""

    def test_categories(self, controller_with_logging, category, mocker, capsys):
        """Make sure the categories get displayed to the user."""
        controller = controller_with_logging
        mocker.patch.object(controller.categories, "get_all", return_value=[category])
        cmds_list.category.list_categories(controller)
        out, err = capsys.readouterr()
        assert category.name in out
        assert controller.categories.get_all.called
