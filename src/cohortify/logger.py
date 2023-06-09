from dataclasses import dataclass
from enum import Enum
from typing import Optional

from loguru import logger

from cohortify.candidate import Candidate


class LogType(Enum):
    """List of log types supported by Logger class"""

    init_round = "New Offer Round Started"
    has_capacity_proposer = "Proposer Returned to Pool"
    has_capacity_recipient = "Recipient Accepts Offer"
    exceeds_capacity_proposer = "Proposer Not Returned to Pool"
    exceeds_capacity_recipient = "Recipient Compares Offers"
    has_offers = "Proposer Returned to Pool"
    no_offers = "Proposer Has No Offers Left"
    accepts_offer = "Recipient Swaps Offers"
    rejects_offer = "Recipient Rejects Offer"
    recipient_not_found = "Recipient Not Found"
    proposer_not_ranked = "Proposer Not Ranked"


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
                f"{self.proposer} has room for {self._proposer.capacity} "
                f"matches, but only has {len(self._proposer.matches)} matches "
                "currently. As a result, they will be returned to the pool."
            )
            self.record_log(message, LogType.has_capacity_proposer)
        else:
            message = (
                f"{self.recipient} has room for {self._recipient.capacity} matches "
                f"but only has {len(self._recipient.matches)} matches currently. "
                f"As a result they will accept the offer from {self.proposer}."
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
            f"{candidate.name} still has offers left to make and will be "
            "returned to the proposer pool."
        )
        self.record_log(
            message=message,
            log_type=LogType.has_offers,
            proposer=candidate.name,
            recipient="N/A",
        )

    def no_offers_left(self, offer_round: int, proposer: Candidate):
        """Record that a proposer does not have any remaining offers to make"""
        message = (
            f"{proposer.name} does not have any offers left to make "
            "and will not be returned to the pool of proposers."
        )
        self.record_log(
            message,
            LogType.no_offers,
            offer_round=offer_round,
            proposer=proposer.name,
            recipient="N/A",
        )

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

    def recipient_not_found(
        self,
        offer_round: int,
        proposer: Candidate,
        recipient: str,
    ) -> None:
        """Record that the recipient wasn't found in the list of recipients"""
        message = (
            f"{proposer.name} ranked {recipient}, but {recipient} wasn't "
            "found in the list of recipients."
        )
        self.record_log(
            message=message,
            log_type=LogType.recipient_not_found,
            offer_round=offer_round,
            proposer=proposer.name,
            recipient=recipient,
        )

    def proposer_not_ranked(
        self,
        offer_round: int,
        proposer: Candidate,
        recipient: Candidate,
    ) -> None:
        """Record that the recipient didn't rank the proposer"""
        message = (
            f"{proposer.name} ranked {recipient.name}, but {recipient.name} "
            f"did not rank {proposer.name} in return."
        )
        self.record_log(
            message=message,
            log_type=LogType.recipient_not_found,
            offer_round=offer_round,
            proposer=proposer.name,
            recipient=recipient.name,
        )

    def record_log(
        self,
        message: str,
        log_type: LogType,
        offer_round: int = None,
        proposer: str = None,
        recipient: str = None,
    ) -> None:
        """Record a new log to std error and to the logs list"""
        entry = LogEntry(
            offer_round=offer_round or self.offer_round,
            proposer=proposer or self.proposer,
            recipient=recipient or self.recipient,
            log_type=log_type.value,
            message=message,
        )
        self.logs.append(entry)
        logger.info(entry)
