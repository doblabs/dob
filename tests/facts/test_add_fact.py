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

import pytest
from freezegun import freeze_time
from nark.tests.helpers.conftest import factoid_fixture

from dob.facts.add_fact import add_fact


class TestAddFact(object):
    """Unit test related to starting a new fact."""

    @freeze_time("2015-12-25 18:00")
    @pytest.mark.parametrize(*factoid_fixture)
    def test_add_new_fact(
        self,
        controller_with_logging,
        mocker,
        raw_fact,
        time_hint,
        expectation,
    ):
        """
        Test that input validation and assignment of start/end time(s) works as expected.

        To test just this function -- and the parametrize, above -- try:

          workon dob
          cdproject
          py.test --pdb -vv -k test_add_new_fact tests/

        """
        controller = controller_with_logging
        mocker.patch.object(controller.facts, "save")
        add_fact(controller, raw_fact, time_hint=time_hint, use_carousel=False)
        assert controller.facts.save.called
        args, kwargs = controller.facts.save.call_args
        fact = args[0]
        assert fact.start == expectation["start"]
        assert fact.end == expectation["end"]
        assert fact.activity_name == expectation["activity"]
        assert fact.category_name == expectation["category"]
        expecting_tags = ""
        tagnames = list(expectation["tags"])
        if tagnames:
            tagnames.sort()
            expecting_tags = ["#{}".format(name) for name in tagnames]
            expecting_tags = "{}".format(" ".join(expecting_tags))
        assert fact.tagnames() == expecting_tags
        expect_description = expectation.get("description", None) or None
        assert fact.description == expect_description


# ***


class TestStop(object):
    """Unit test concerning the stop command."""

    def test_stop_existing_ongoing_fact(
        self,
        ongoing_fact,
        controller_with_logging,
        mocker,
    ):
        """Make sure stopping an ongoing fact works as intended."""
        mockfact = mocker.MagicMock()
        mockfact.activity.name = "foo"
        mockfact.category.name = "bar"
        mocktime = mocker.MagicMock(return_value="%Y-%m-%d %H:%M")
        mockfact.start.strftime = mocktime
        mockfact.end.strftime = mocktime
        current_fact = mocker.MagicMock(return_value=mockfact)
        # While nark still has stop_current_fact, dob replaced stop_fact
        # with add_fact, so it can use all the same CLI magic that the
        # other add-fact commands use. So while we're testing stop-fact
        # here, we're really testing add-fact with a verify-end time-hint.
        controller_with_logging.facts.save = current_fact
        # 2019-12-06: stop_fact was deleted, replaced with add_fact + time_hint.
        add_fact(
            controller_with_logging,
            factoid="",
            time_hint="verify_end",
            use_carousel=False,
        )
        assert controller_with_logging.facts.save.called

    def test_stop_no_existing_ongoing_fact(self, controller_with_logging):
        """Make sure that stop without actually an ongoing fact leads to an error."""
        with pytest.raises(SystemExit):
            # 2019-12-06: stop_fact was deleted, replaced with add_fact + time_hint.
            add_fact(
                controller_with_logging,
                factoid="",
                time_hint="verify_end",
                use_carousel=False,
            )
