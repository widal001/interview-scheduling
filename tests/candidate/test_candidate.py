import pytest

from cohortify.candidate import Candidate, CandidateList


class TestRankFor:
    """Tests the Candidate.rank_for() method"""

    def test_get_ranked_candidate(self, alice: Candidate):
        """Return the correct rank for a ranked offer"""
        # validation
        assert alice.ranks("Bob") == 0

    def test_returns_none_if_unranked_without_default(self, alice: Candidate):
        """Return None if the offer is unranked and no default is set"""
        # validation
        assert alice.ranks("Eddie") is None

    def test_returns_default_if_unranked_with_default(self, alice: Candidate):
        """Returns the default value if offer is unranked"""
        assert alice.ranks("Eddit", 99) == 99


class TestPrefers:
    """Tests the Candidate.prefers() method"""

    def test_prefers_new_offer(self, alice: Candidate):
        """Test return True for when new offer is preferred"""
        # setup
        assert alice.ranks("Bob") == 0
        assert alice.ranks("Charlie") == 1
        # validation
        assert alice.prefers("Bob", to="Charlie") is True

    def test_prefers_old_offer(self, alice: Candidate):
        """Test return False for when old offer is preferred"""
        # setup
        assert alice.ranks("Bob") == 0
        assert alice.ranks("Charlie") == 1
        # validation
        assert alice.prefers("Charlie", to="Bob") is False

    def test_prefers_ranked_to_unranked(self, alice: Candidate):
        """Test that a ranked candidate is preferred to an unranked candidate"""
        # setup
        ranked = "Dana"
        unranked = "Eddie"
        assert alice.ranks(ranked) is not None
        assert alice.ranks(unranked) is None
        # validation
        assert alice.prefers(ranked, to=unranked) is True
        assert alice.prefers(unranked, to=ranked) is False

    def test_raise_error_if_both_unranked(self, alice: Candidate):
        """Test that ValueError is raised when both are unranked"""
        # setup
        unranked1 = "Frank"
        unranked2 = "Eddie"
        assert alice.ranks(unranked1) is None
        assert alice.ranks(unranked2) is None
        # validation
        with pytest.raises(ValueError):
            alice.prefers(unranked1, to=unranked2)


class TestHasCapacity:
    """Tests Candidate.has_capacity property"""

    def test_does_not_have_capacity(self, alice: Candidate):
        """Tests has capacity is False if capacity equals number of matches"""
        # setup
        alice.matches.add("Bob")
        alice.capacity = 1
        # validation
        assert alice.has_capacity is False

    def test_has_capacity(self, alice: Candidate):
        """Test has capacity is True if capacity is greater than number of matches"""
        # setup
        alice.matches.add("Bob")
        alice.capacity = 99
        # validation
        assert alice.has_capacity is True


def test_create_candidate_list():
    """Test create candidate list"""
    # setup
    preferences = {
        "Alice": ["Bob", "Charlie"],
        "Bob": ["Alice", "Charlie"],
        "Charlie": ["Bob", "Alice"],
    }
    capacities = {"Alice": 2, "Bob": 2}
    # execution
    candidates = CandidateList(preferences, capacities, default_capacity=1)
    charlie = candidates.get("Charlie")
    c_list = candidates.to_list()
    # validation
    assert charlie is not None
    assert charlie.capacity == 1
    for name in preferences:
        assert name in c_list
