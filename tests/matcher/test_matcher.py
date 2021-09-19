from pprint import pprint
from copy import deepcopy

from cohortify.matcher import Matcher
from tests.matcher.matcher_data import PREFS, INTERVIEWS


class TestInit:
    """Tests Matcher.init()"""

    def test_init(self):
        """Tests that Matcher instantiates correctly

        Validates following conditions:
        - Matcher.c_prefs matches the input c_prefs
        - Matcher.p_prefs matches the input p_prefs
        - Matcher.candidates contains all of the candidates
        - Matcher.positions contains all of the positions
        """
        # setup
        c_prefs = PREFS["complete"]["candidates"]
        p_prefs = PREFS["complete"]["positions"]
        candidates = ["Alice", "Bob", "Charlie"]
        positions = ["Position 1", "Position 2", "Position 3"]

        # execution
        m = Matcher(c_prefs, p_prefs)

        # validation
        assert m.c_prefs == c_prefs
        assert m.p_prefs == p_prefs
        assert m.candidates == candidates
        assert m.positions == positions


class TestAssingInterviews:
    """Tests Matcher.assign_interviews()"""

    def test_complete(self):
        """Tests that Matcher.assign_interviews() matches all positions and
        candidates to interviews
        """
        # inputs
        c_prefs = PREFS["complete"]["candidates"]
        p_prefs = PREFS["complete"]["positions"]
        c_matches = INTERVIEWS["complete"]["candidates"]
        p_matches = INTERVIEWS["complete"]["positions"]

        # execution
        m = Matcher(c_prefs, p_prefs)
        m.assign_interviews(c_min=1, c_max=3, p_min=1, p_max=3)

        print("EXPECTED")
        pprint(c_matches)
        print("ACTUAL")
        pprint(m.c_matches)
        print("EXPECTED")
        pprint(p_matches)
        print("ACTUAL")
        pprint(m.p_matches)

        # validation
        assert m.c_matches == c_matches
        assert m.p_matches == p_matches
        assert m.c_remaining == []
        assert m.p_remaining == []

    def test_unmatched_candidate(self):
        """Tests that the correct set of candidates are listed as unmatched if
        they can't be matched to interviews based on their preferences
        """
        # inputs
        c_prefs = deepcopy(PREFS["complete"]["candidates"])
        p_prefs = deepcopy(PREFS["complete"]["positions"])
        c_matches = deepcopy(INTERVIEWS["complete"]["candidates"])
        p_matches = deepcopy(INTERVIEWS["complete"]["positions"])
        c_prefs["Dana"] = {"Position 1": 1, "Position 2": 2, "Position 3": 3}
        c_matches["Dana"] = []

        # execution
        m = Matcher(c_prefs, p_prefs)
        m.assign_interviews(c_min=1, c_max=3, p_min=1, p_max=3)

        print("EXPECTED")
        pprint(c_matches)
        print("ACTUAL")
        pprint(m.c_matches)
        print("EXPECTED")
        pprint(p_matches)
        print("ACTUAL")
        pprint(m.p_matches)

        # validation
        assert m.c_matches == c_matches
        assert m.p_matches == p_matches
        assert m.c_remaining == ["Dana"]
        assert m.p_remaining == []

    def test_unmatched_position(self):
        """Tests that the correct set of positions are listed as unmatched if
        they can't be matched to interviews based on their preferences
        """
        # inputs
        c_prefs = deepcopy(PREFS["complete"]["candidates"])
        p_prefs = deepcopy(PREFS["complete"]["positions"])
        c_matches = deepcopy(INTERVIEWS["complete"]["candidates"])
        p_matches = deepcopy(INTERVIEWS["complete"]["positions"])
        p_prefs["Position 4"] = {"Alice": 1, "Bob": 2, "Charlie": 3}
        p_matches["Position 4"] = []

        # execution
        m = Matcher(c_prefs, p_prefs)
        m.assign_interviews(c_min=1, c_max=3, p_min=1, p_max=3)

        print("EXPECTED")
        pprint(c_matches)
        print("ACTUAL")
        pprint(m.c_matches)
        print("EXPECTED")
        pprint(p_matches)
        print("ACTUAL")
        pprint(m.p_matches)

        # validation
        assert m.c_matches == c_matches
        assert m.p_matches == p_matches
        assert m.c_remaining == []
        assert m.p_remaining == ["Position 4"]

    def test_match_swapping(self):
        """Tests that the correct interviews are assigned when a position
        receives an interview from a more preferred candidate after it has
        already reached its max number of interviews.
        """
        # inputs
        c_prefs = deepcopy(PREFS["match swapping"]["candidates"])
        p_prefs = deepcopy(PREFS["match swapping"]["positions"])
        c_matches = deepcopy(INTERVIEWS["match swapping"]["candidates"])
        p_matches = deepcopy(INTERVIEWS["match swapping"]["positions"])

        # execution
        m = Matcher(c_prefs, p_prefs)
        m.assign_interviews(c_min=1, c_max=2, p_min=1, p_max=2)

        print("EXPECTED")
        pprint(c_matches)
        print("ACTUAL")
        pprint(m.c_matches)
        print("EXPECTED")
        pprint(p_matches)
        print("ACTUAL")
        pprint(m.p_matches)
        print("REQUESTS")
        pprint(m.requests_left)

        # validation
        assert m.c_matches == c_matches
        assert m.p_matches == p_matches
        assert m.c_remaining == []
        assert m.p_remaining == []
