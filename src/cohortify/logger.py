from dataclasses import dataclass
from enum import Enum
from typing import Optional

from loguru import logger

from cohortify.candidate import Candidate


class LogType(Enum):
    """List of log types supported by Logger class"""

    init_round = "New Offer Round Started"
    has_capacity_proposer = "Proposer Has Capacity"
    has_capacity_recipient = "Recipient Has Capacity"
    exceeds_capacity_proposer = "Proposer Exceeds Capacity"
    exceeds_capacity_recipient = "Proposer Exceeds Capacity"
    has_offers = "Proposer Has Offers Left"
    no_offers = "Proposer Has No Offers Left"
    accepts_offer = "Recipient Accents New Offer"
    rejects_offer = "Recipient Rejects New Offer"


@dataclass
class LogEntry:
    """Stores the details of a log entry"""

    offer_round: int
    proposer: str
    log_type: str
    message: str
    recipient: Optional[str] = None

    def __repr__(self) -> str:
        return f"""{self.message}\n
        \tType: {self.log_type}
        \tRound: {self.offer_round}
        \tProposer: {self.proposer}
        \tRecipient: {self.recipient}
        \tMessage: {self.message}
        """


class Logger:
    """Records logs throughout a series of matching rounds"""

    def __init__(self) -> None:
        self.logs: list[LogEntry] = []
        self._offer_round: Optional[int] = None
        self._proposer: Optional[Candidate] = None
        self._recipient: Optional[Candidate] = None

    @property
    def offer_round(self) -> int:
        """Offer round in which we are recording logs"""
        if not self._offer_round:
            raise KeyError
        return self._offer_round

    @property
    def proposer(self) -> str:
        """Proposer associated with the current round"""
        if not self._proposer:
            raise KeyError
        return self._proposer.name

    @property
    def recipient(self) -> str:
        """The recipient associated with the current round"""
        if not self._recipient:
            return None
        return self._recipient.name

    def init_round(
        self,
        offer_round: int,
        proposer: Candidate,
        recipient: Candidate,
    ) -> None:
        """Initialize a new offer round for logging"""
        # update class attributes
        self._offer_round = offer_round
        self._proposer = proposer
        self._recipient = recipient
        # record log
        message = (
            f"We are starting offer round {self.offer_round} with "
            f"{self.proposer} as the proposer"
        )
        self.record_log(message, LogType.init_round)

    def has_capacity(self, kind: str) -> None:
        """Record that a proposer or recipient has capacity for new matches"""
        if kind == "proposer":
            message = (
                f"{self.proposer} still has capacity for additional matches and "
                "will be returned to the pool of proposers."
            )
            self.record_log(message, LogType.has_capacity_proposer)
        else:
            message = (
                f"{self.recipient} has capacity for additional matches, "
                f"and will accept the offer from {self.proposer}."
            )
            self.record_log(message, LogType.has_capacity_recipient)

    def exceeds_capacity(self, kind: str) -> None:
        """Record that a proposer or recipient has no capacity for new matches"""
        if kind == "proposer":
            message = (
                f"{self.proposer} meets or exceeds their capacity for matches "
                "and will not be returned to the pool of proposers."
            )
            self.record_log(message, LogType.exceeds_capacity_proposer)
        else:
            message = (
                f"{self.recipient} meets their capacity for matches, and will "
                f"compare the offer from {self.proposer} to their current "
                "matches to determine which offer they will reject."
            )
            self.record_log(message, LogType.exceeds_capacity_recipient)

    def has_offers_left(self, candidate: Candidate) -> None:
        """Record that a proposer still has offers to make to recipients"""
        message = (
            f"{candidate.name} still has no offers left to make and will be "
            "returned to the proposer pool."
        )
        self.record_log(
            message=message,
            log_type=LogType.has_offers,
            proposer=candidate,
            recipient="N/A",
        )

    def no_offers_left(self):
        """Record that a proposer does not have any remaining offers to make"""
        message = (
            f"{self.proposer} does not have any offers left to make "
            "and will not be returned to the pool of proposers."
        )
        self.record_log(message, LogType.no_offers, recipient="N/A")

    def new_offer_rejected(self):
        """Record that the recipient accepted an offer from the current proposer"""
        message = (
            f"{self.recipient} did not prefer {self.proposer} to any of their "
            "current matches and as a result rejects this new offer."
        )
        self.record_log(message, LogType.rejects_offer)

    def new_offer_accepted(self, old_offer: Candidate) -> None:
        """Record that the recipient rejected an old offer to accept a new one"""
        message = (
            f"{self.recipient} prefers {self.proposer} to {old_offer.name} "
            f"and as a result rejects the old offer from {old_offer.name} and "
            f"accepts the new offer from {self.proposer}."
        )
        self.record_log(message, LogType.accepts_offer)

    def record_log(
        self,
        message: str,
        log_type: LogType,
        proposer: str = None,
        recipient: str = None,
    ) -> None:
        """Record a new log to std error and to the logs list"""
        entry = LogEntry(
            offer_round=self.offer_round,
            proposer=proposer or self.proposer,
            recipient=recipient or self.recipient,
            log_type=log_type.value,
            message=message,
        )
        self.logs.append(entry)
        logger.info(entry)
