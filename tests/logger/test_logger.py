import pytest

from cohortify.candidate import Candidate
from cohortify.logger import Logger, LogType

OFFER_ROUND = 1
PROPOSER = "Alice"
RECIPIENT = "Bob"


@pytest.fixture(scope="function", name="logger")
def mock_logger(alice: Candidate, bob: Candidate):
    """Creates a logger fixture"""
    logger = Logger()
    logger.init_round(
        offer_round=OFFER_ROUND,
        proposer=alice,
        recipient=bob,
    )
    return logger


def test_init_round(logger: Logger) -> None:
    """Tests that init_round functions as expected"""
    # validation -- Check that class attributes are set correctly
    assert logger.offer_round == OFFER_ROUND
    assert logger.proposer == PROPOSER
    assert logger.recipient == RECIPIENT
    # validation -- Check that the logs contain the correct entry
    last_log = logger.logs[0]
    assert last_log.log_type == LogType.init_round.value
    assert last_log.offer_round == OFFER_ROUND
    assert last_log.proposer == PROPOSER
    assert last_log.recipient == RECIPIENT
    assert last_log.message != ""


def test_has_capacity_recipient(logger: Logger) -> None:
    """Tests that init_round functions as expected"""
    # setup
    logger.has_capacity(kind="recipient")
    # validation
    last_log = logger.logs[-1]
    assert last_log.log_type == LogType.has_capacity_recipient.value


def test_has_capacity_proposer(logger: Logger) -> None:
    """Tests that logger.has_capacity() records the correct log type"""
    # setup
    logger.has_capacity(kind="proposer")
    # validation
    last_log = logger.logs[-1]
    assert last_log.log_type == LogType.has_capacity_proposer.value


def test_exceeds_capacity_proposer(logger: Logger) -> None:
    """Tests that logger.exceeds_capacity() records the correct log type"""
    # setup
    logger.exceeds_capacity(kind="proposer")
    # validation
    last_log = logger.logs[-1]
    assert last_log.log_type == LogType.exceeds_capacity_proposer.value


def test_exceeds_capacity_recipient(logger: Logger) -> None:
    """Tests that logger.exceeds_capacity() records the correct log type"""
    # setup
    logger.exceeds_capacity(kind="recipient")
    # validation
    last_log = logger.logs[-1]
    assert last_log.log_type == LogType.exceeds_capacity_recipient.value


def test_rejects_offer(logger: Logger) -> None:
    """Tests that logger.new_offer_rejected() records the correct log type"""
    # setup
    logger.new_offer_rejected()
    # validation
    last_log = logger.logs[-1]
    assert last_log.log_type == LogType.rejects_offer.value


def test_accepts_offer(logger: Logger, charlie: Candidate) -> None:
    """Tests that logger.new_offer_accepted() records the correct log type"""
    # setup
    logger.new_offer_accepted(old_offer=charlie)
    # validation
    last_log = logger.logs[-1]
    assert last_log.log_type == LogType.accepts_offer.value


def test_no_offers(logger: Logger, charlie: Candidate) -> None:
    """Tests that logger.no_offers_left() records the correct log type"""
    # setup
    logger.no_offers_left(
        offer_round=OFFER_ROUND,
        proposer=charlie,
    )
    # validation
    last_log = logger.logs[-1]
    assert last_log.log_type == LogType.no_offers.value


def test_has_offers(logger: Logger, charlie: Candidate) -> None:
    """Tests that logger.has_offers_left() records the correct log type"""
    # setup
    logger.has_offers_left(candidate=charlie)
    # validation
    last_log = logger.logs[-1]
    assert last_log.log_type == LogType.has_offers.value
