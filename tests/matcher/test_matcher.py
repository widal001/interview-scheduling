from pprint import pprint
from copy import deepcopy

from utils.matcher import Matcher
from tests.matcher.matcher_data import PREFS, INTERVIEWS


class TestInit:
    def test_complete(self):
        # setup
        c_prefs = PREFS["complete"]["candidates"]
        p_prefs = PREFS["complete"]["positions"]
        candidates = ["Alice", "Bob", "Charlie"]
        positions = ["Position 1", "Position 2", "Position 3"]

        # execution
        m = Matcher(c_prefs, p_prefs)

        # validation
        m.c_prefs = c_prefs
        m.p_prefs = p_prefs
        m.candidates = candidates
        m.positions = positions


class TestAssingInterviews:
    def test_complete(self):

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
