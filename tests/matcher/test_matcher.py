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
        assert 1

    def test_unmatched_candidate(self):
        assert 1

    def test_unmatched_position(self):
        assert 1
