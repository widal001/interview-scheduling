import pytest

from cohortify.matcher import Matcher, MatchResult
from cohortify.logger import LogEntry
from tests.matcher.matcher_data import PREFS


@pytest.fixture(scope="function", name="matcher")
def mock_matcher():
    """Create a mock Matcher class for tests"""
    p_prefs = {
        "Alice": ["Position 1"],
        "Bob": ["Position 2"],
        "Charlie": ["Position 3"],
    }
    r_prefs = {
        "Position 1": ["Alice"],
        "Position 2": ["Bob"],
        "Position 3": ["Charlie"],
    }
    return Matcher(proposer_prefs=p_prefs, recipient_prefs=r_prefs)


class TestInit:
    """Tests Matcher.__init__()"""

    def test_init(self):
        """Tests that Matcher instantiates correctly

        Validates following conditions:
        - Matcher.c_prefs matches the input c_prefs
        - Matcher.p_prefs matches the input p_prefs
        """
        # setup
        p_prefs = PREFS["complete"]["candidates"]
        r_prefs = PREFS["complete"]["positions"]
        # execution
        m = Matcher(p_prefs, r_prefs)
        # validation
        assert m.proposer_prefs == p_prefs
        assert m.recipient_prefs == r_prefs


def test_match(matcher: Matcher, alice, bob):
    """Tests the Matcher.match() static method"""
    # setup
    assert bob.name not in alice.matches
    assert alice.name not in bob.matches
    # execution
    matcher.match(alice, bob)
    # validation
    assert bob.name in alice.matches
    assert alice.name in bob.matches


class TestReplaceCurrentMatch:
    """Tests the Matcher.match() static method"""

    def test_replace_when_already_matched(
        self,
        matcher: Matcher,
        alice,
        bob,
        charlie,
    ):
        """Should successfully remove and replace old match with new match"""
        # setup
        alice.matches.add(charlie.name)
        charlie.matches.add(alice.name)
        assert charlie.name in alice.matches
        assert alice.name in charlie.matches
        # execution
        matcher.replace_current_match(alice, old_match=charlie, new_match=bob)
        # validation
        assert bob.name in alice.matches
        assert alice.name in bob.matches
        assert alice.name not in charlie.matches

    def test_avoid_error_if_not_already_matched(
        self,
        matcher: Matcher,
        alice,
        bob,
        charlie,
    ):
        """Should not raise an error if old match isn't found in matches"""
        # setup
        charlie.matches.add(alice.name)
        assert charlie.name not in alice.matches  # shouldn't cause an error
        assert alice.name in charlie.matches
        # execution
        matcher.replace_current_match(alice, old_match=charlie, new_match=bob)
        # validation
        assert bob.name in alice.matches
        assert alice.name in bob.matches
        assert alice.name not in charlie.matches


class TestAssingInterviews:
    """Tests Matcher.assign_matches()"""

    def test_complete(self, matcher: Matcher):
        """Tests that Matcher.assign_matches() matches all positions and
        candidates to interviews
        """
        # setup
        expected = [
            ("Alice", "Position 1"),
            ("Bob", "Position 2"),
            ("Charlie", "Position 3"),
        ]
        # execution
        result = matcher.assign_matches(p_capacity=1, r_capacity=1)
        alice = result.proposers.get("Alice")
        print(alice.matches)
        # validation
        assert isinstance(result, MatchResult)
        assert result.matches == expected

    def test_unmatched_candidate(self, matcher: Matcher):
        """Tests that the correct set of candidates are listed as unmatched if
        they can't be matched to interviews based on their preferences
        """
        # setup
        matcher.recipient_prefs["Position 3"] = ["Alice"]
        # execution
        result = matcher.assign_matches(p_capacity=1, r_capacity=1, p_min=1)
        charlie = result.proposers.get("Charlie")
        position3 = result.recipients.get("Position 3")
        remaining = result.get_remaining(kind="proposers")
        print(charlie.matches)
        print(remaining)
        # validation
        assert charlie.matches == set()
        assert position3.matches == set()
        assert len(remaining) == 1
        assert remaining == [charlie]
        assert isinstance(result.match_logs[0], LogEntry)

    def test_unmatched_position(self, matcher: Matcher):
        """Tests that the correct set of positions are listed as unmatched if
        they can't be matched to interviews based on their preferences
        """
        # setup
        matcher.proposer_prefs["Alice"] = ["Position 2"]
        # execution
        result = matcher.assign_matches(p_capacity=1, r_capacity=1, r_min=1)
        position1 = result.recipients.get("Position 1")
        alice = result.proposers.get("Alice")
        remaining = result.get_remaining(kind="recipients")
        print(position1.matches)
        print(alice.matches)
        print(remaining)
        # validation
        assert position1.matches == set()
        assert alice.matches == set()
        assert len(remaining) == 1
        assert remaining == [position1]

    def test_two_matches_for_a_position(self, matcher: Matcher):
        """Assign multiple candidates to a position if the position has capacity"""
        # setup
        matcher.proposer_prefs["Bob"] = ["Position 1"]
        matcher.recipient_prefs["Position 1"] = ["Alice", "Bob"]
        # execution
        result = matcher.assign_matches(p_capacity=1, r_capacity=2)
        position1 = result.recipients.get("Position 1")
        alice = result.proposers.get("Alice")
        bob = result.proposers.get("Bob")
        print(position1.matches)
        print(alice.matches)
        print(bob.matches)
        # validation
        assert position1.capacity == 2
        assert position1.matches == {alice.name, bob.name}
        assert alice.matches == {position1.name}
        assert bob.matches == {position1.name}

    def test_candidate_matched_to_second_choice(self, matcher: Matcher):
        """Candidate matched to second choice after being rejeceted from first"""
        # setup
        matcher.proposer_prefs["Alice"] = ["Position 1", "Position 2"]
        matcher.proposer_prefs["Bob"] = ["Position 1"]
        matcher.recipient_prefs["Position 1"] = ["Bob", "Alice"]
        matcher.recipient_prefs["Position 2"] = ["Alice", "Bob"]
        # execution
        result = matcher.assign_matches(p_capacity=1, r_capacity=1)
        position1 = result.recipients.get("Position 1")
        position2 = result.recipients.get("Position 2")
        alice = result.proposers.get("Alice")
        bob = result.proposers.get("Bob")
        # validation
        assert position1.matches == {bob.name}
        assert position2.matches == {alice.name}
        assert alice.matches == {position2.name}
        assert bob.matches == {position1.name}
