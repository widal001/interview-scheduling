from __future__ import annotations  # prevents NameErrors for typing
from typing import Dict, List, Tuple, Optional, Union

from cohortify.candidate import Candidate, CandidateList
from cohortify.logger import Logger, LogEntry

Member = str
Preferences = Dict[Member, List[Member]]
Capacity = Dict[Member, int]
Match = Tuple[Member, Member]


class MatchResult:
    """Stores results of a matching between proposers and recipients"""

    def __init__(
        self,
        proposers: CandidateList,
        recipients: CandidateList,
        match_logs: list[LogEntry],
        p_min: int = 0,
        r_min: int = 0,
    ) -> None:
        """Initializes the matcher result class

        Parameters
        ----------
        proposers: CandidateList
            The list of candidates who made offers to recipients during the match
        recipients: CandidateList
            The list of candidates who accepted or rejected offers from proposers
        p_min: int
            The minimum number of matches we expected proposers to have
        r_min: int
            The minimum number of matches we expected recipients to have
        """
        self.proposers = proposers
        self.recipients = recipients
        self.match_logs = match_logs
        self.p_min = p_min
        self.r_min = r_min

    @property
    def matches(self) -> List[Match]:
        """Return a list of matches between proposers and recipients"""
        match_list = []
        for p_name, proposer in self.proposers.items():
            matches = proposer.matches
            match_list.extend([(p_name, r_name) for r_name in matches])
        return match_list

    def get_remaining(self, kind: str = "proposers") -> List[Candidate]:
        """Returns candidates that have fewer than the minimum match threshold

        Parameters
        ----------
        kind: str, default "proposers"
            The kind of candidate to return, must one of proposers or recipients

        Returns
        -------
        List[Candidates]
            List of candidates who have fewer matches than either the p_min or
            the r_min for proposers and recipients, respectively
        """
        if kind not in ["proposers", "recipients"]:
            raise KeyError
        if kind == "proposers":
            candidates = self.proposers.candidates.values()
            min_matches = self.p_min
        else:
            candidates = self.recipients.candidates.values()
            min_matches = self.r_min
        return [c for c in candidates if len(c.matches) < min_matches]


class Matcher:
    """Match Proposers to Recipients using deferred acceptance algorithm"""

    def __init__(
        self,
        proposer_prefs: Preferences,
        recipient_prefs: Preferences,
    ):
        """Initializes the Matcher class for interview or placement matching

        Parameters
        ----------
        proposer_prefs: Dict[Member, List[Members]]
            Dictionary that maps a proposer to their ranked list of recipients
        recipient_prefs: Dict[Member, List[Members]]
            Dictionary that maps a recipient to their ranked list of proposers
        """
        self.proposer_prefs = proposer_prefs
        self.recipient_prefs = recipient_prefs
        self.log = Logger()

    def assign_matches(
        self,
        p_capacity: Union[int, Capacity] = 1,
        r_capacity: Union[int, Capacity] = 1,
        p_min: int = 0,
        r_min: int = 0,
    ) -> MatchResult:
        """Match Proposers to Recipients using deferred acceptance algorithm

        Parameters
        ----------
        p_capacity: int | Capacity, default = 1
            The maximum number of recipients a proposer can be matched to.
            This value can either be passed as an int to make all capacities
            the same, or as a dictionary to set capacities individually
        r_capacity: int | Capacity, default = 1
            The maximum number of proposers a recipient can be matched to.
            This value can either be passed as an int to make all capacities
            the same, or as a dictionary to set capacities individually
        p_min: int
            The minimum number of matches each proposer should have by the end
            of the matching process. Proposers below this threshold are flagged
            as "remaining" in the match result
        r_min: int
            The minimum number of matches each proposer should have by the end
            of the matching process. Proposers below this threshold are flagged
            as "remaining" in the match result

        Returns
        -------
        MatchResult
            An instance of MatchResult that maps proposers to recipients
        """

        # TODO: refactor these lines
        if isinstance(p_capacity, int):
            p_capacity = {p: p_capacity for p in self.proposer_prefs}
        if isinstance(r_capacity, int):
            r_capacity = {r: r_capacity for r in self.recipient_prefs}

        recipients = CandidateList(self.recipient_prefs, r_capacity)
        proposers = CandidateList(self.proposer_prefs, p_capacity)
        proposers_left = proposers.to_list()

        # start the deferred acceptance algorithm
        offer_round = 0
        while proposers_left:
            offer_round += 1

            # get the next proposer with an offer to make
            proposer = proposers.get(proposers_left.pop(0))
            recipient = self.get_next_valid_offer(proposer, recipients)
            self.log.init_round(offer_round, proposer, recipient)

            if not recipient:
                self.log.no_offers_left()
                continue

            if recipient.has_capacity:
                self.log.has_capacity(kind="recipient")
                self.match(proposer, recipient)
            else:
                self.log.exceeds_capacity(kind="recipient")
                # if the recipient prefers this offer to their current matches
                # replace the lowest ranked match with the new proposer
                rejected = recipient.compare_offers(proposer.name)
                if proposer.name != rejected:
                    rejected = proposers.get(rejected)
                    self.log.new_offer_accepted(old_offer=rejected)
                    self.replace_current_match(
                        recipient=recipient,
                        old_match=rejected,
                        new_match=proposer,
                    )
                    if rejected.has_offers:
                        self.log.has_offers_left(candidate=rejected)
                        proposers_left.append(rejected.name)
                else:
                    self.log.new_offer_rejected()

            # if they have capacity, add the proposer back to the pool
            if proposer.has_capacity:
                self.log.has_capacity(kind="proposer")
                proposers_left.append(proposer)
            else:
                self.log.exceeds_capacity(kind="proposer")

        return MatchResult(
            proposers=proposers,
            recipients=recipients,
            match_logs=self.log.logs,
            p_min=p_min,
            r_min=r_min,
        )

    def replace_current_match(
        self,
        recipient: Candidate,
        old_match: Candidate,
        new_match: Candidate,
    ) -> None:
        """Unmatch recipient and old_match and match recipient with new_match"""
        self.unmatch(recipient, old_match)
        self.match(recipient, new_match)

    @staticmethod
    def match(proposer: Candidate, recipient: Candidate) -> None:
        """Add a proposer and a recipient to each other's list of matches"""
        recipient.matches.add(proposer.name)
        proposer.matches.add(recipient.name)

    @staticmethod
    def unmatch(proposer: Candidate, recipient: Candidate) -> None:
        """Remove candidates from one another's list of matches"""
        proposer.matches.discard(recipient.name)
        recipient.matches.discard(proposer.name)

    def get_next_valid_offer(
        self,
        proposer: Candidate,
        recipients: CandidateList,
    ) -> Optional[Candidate]:
        """Get the next preferred recipient who has also ranked the proposer"""
        for offer in proposer.offers_left:
            recipient = recipients.get(offer)
            if recipient.ranks(proposer.name):
                return recipient
        return None
