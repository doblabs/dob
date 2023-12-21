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
        capsys,
    ):
        """
        Test input validation and assignment of start/end time(s).

        To test just this function — and nark's factoid_fixture — try:

          pytest --pdb -s -vv \
            tests/facts/test_add_fact.py::TestAddFact::test_add_new_fact
        """

        # HINT: To test a specific factoid from factoid_fixture,
        #       you can skip the other tests. Try something like:
        #
        #   if (raw_fact, time_hint) != ('Monday-13:00: foo@bar', 'verify_both'):
        #       return
        #
        # - And add a set_trace() below.
        def _test_add_new_fact():
            if "err" in expectation and expectation["err"]:
                with pytest.raises(SystemExit):
                    _test_add_new_fact_and_validate()
                out, err = capsys.readouterr()
                # There may or may not be stdout.
                #   assert not out and err
                assert expectation["err"] in err or expectation["err"] in out
            else:
                _test_add_new_fact_and_validate()
                out, err = capsys.readouterr()
                assert out and not err

        def _test_add_new_fact_and_validate():
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

        _test_add_new_fact()


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
            # Enable lenient, otherwise raises exception:
            #   "Expected to find an "@" indicating the activity."
            # - Well, use lenient, or specifiy time and activity, e.g.,
            #     factoid="now: foo@bar",
            lenient=True,
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
