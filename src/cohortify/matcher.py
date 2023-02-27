from __future__ import annotations  # prevents NameErrors for typing
from typing import Dict, List, Tuple, Optional, Union

from cohortify.candidate import Candidate, CandidateList

Member = str
Preferences = Dict[Member, List[Member]]
Capacity = Dict[Member, int]
Match = Tuple[Member, Member]


class MatchResult:
    def __init__(
        self,
        proposers: CandidateList,
        recipients: CandidateList,
        p_min: int = 0,
        r_min: int = 0,
    ) -> None:
        self.proposers = proposers
        self.recipients = recipients
        self.p_min = p_min
        self.r_min = r_min

    @property
    def matches(self) -> List[Match]:
        match_list = []
        for p_name, proposer in self.proposers.items():
            matches = proposer.matches
            match_list.extend([(p_name, r_name) for r_name in matches])
        return match_list

    def get_remaining(self, kind: str = "proposers") -> List[Candidate]:
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

    def assign_matches(
        self,
        p_capacity: Union[int, Dict[Member, int]] = 1,
        r_capacity: Union[int, Dict[Member, int]] = 1,
        p_min: int = 0,
        r_min: int = 0,
    ) -> MatchResult:
        """Match Proposers to Recipients using deferred acceptance algorithm"""

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
            if not recipient:
                continue

            if recipient.has_capacity:
                self.match(proposer, recipient)
            else:
                # if the recipient prefers this offer to their current matches
                # replace the lowest ranked match with the new proposer
                rejected = recipient.compare_offers(proposer.name)
                if proposer.name != rejected:
                    rejected = proposers.get(rejected)
                    self.replace_current_match(
                        recipient=recipient,
                        new_match=proposer,
                        old_match=rejected,
                    )
                    if rejected.has_offers:
                        proposers_left.append(rejected.name)

            # if they have capacity, add the proposer back to the pool
            if proposer.has_capacity:
                proposers_left.append(proposer)

        return MatchResult(
            proposers=proposers,
            recipients=recipients,
            p_min=p_min,
            r_min=r_min,
        )

    @staticmethod
    def replace_current_match(
        recipient: Candidate,
        new_match: Candidate,
        old_match: Candidate,
    ) -> None:
        """Replace the recipients"""
        old_match.matches.discard(recipient.name)
        recipient.matches.discard(old_match.name)
        recipient.matches.add(new_match.name)
        new_match.matches.add(recipient.name)

    @staticmethod
    def match(proposer: Candidate, recipient: Candidate) -> None:
        """Add a proposer and a recipient to each other's list of matches"""
        print(f"Matching {proposer.name} to {recipient.name}")
        recipient.matches.add(proposer.name)
        proposer.matches.add(recipient.name)

    def get_next_valid_offer(
        self,
        proposer: Candidate,
        recipients: CandidateList,
    ) -> Optional[Candidate]:
        """Get the next ranked recipient who has also ranked the proposer"""
        for offer in proposer.offers_left:
            recipient = recipients.get(offer)
            if recipient.ranks(proposer.name):
                return recipient
        return None
