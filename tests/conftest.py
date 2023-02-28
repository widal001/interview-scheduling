import pytest

from cohortify.candidate import Candidate


@pytest.fixture(scope="function", name="alice")
def mock_candidate_alice():
    """Creates a mock candidate named Alice for tests"""
    return Candidate(
        name="Alice",
        prefs=["Bob", "Charlie", "Dana"],
        capacity=1,
    )


@pytest.fixture(scope="function", name="bob")
def mock_candidate_bob():
    """Creates a mock candidate named Alice for tests"""
    return Candidate(
        name="Bob",
        prefs=["Alice", "Charlie", "Dana"],
        capacity=1,
    )


@pytest.fixture(scope="function", name="charlie")
def mock_candidate_charlie():
    """Creates a mock candidate named Alice for tests"""
    return Candidate(
        name="Charlie",
        prefs=["Alice", "Charlie", "Dana"],
        capacity=1,
    )
