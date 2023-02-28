from __future__ import annotations
import math
from typing import List, Optional, Dict, Tuple

Name = str
Offer = str
Preferences = Dict[Name, List[Name]]
Capacities = Dict[Name, int]


class Candidate:
    """Represents a candidate in a matching market"""

    def __init__(
        self,
        name: Name,
        prefs: List[Offer],
        capacity: int,
    ) -> None:
        """Initializes the Candidate candidate class

        Parameters
        ----------
        name: str
            The name of the candidate
        prefs: List[str]
            A list of offers, ranked according to the candidate's preference,
            with an index of 0 representing the most preferred offer
        capacity: int
            The maximum number of offers a candidate can accept
        """
        self.name = name
        self.prefs = prefs
        self.capacity = capacity
        self.offers_left = (offer for offer in prefs)
        self.matches = set()
        self._rankings = None

    def ranks(
        self,
        offer: str,
        default: Optional[int] = None,
    ) -> Optional[int]:
        """Return candidate's ranking of a given offer, with optional default"""
        return self.rankings.get(offer, default)

    def prefers(self, new: str, to: str) -> bool:
        """Does the candidate prefer new offer to the current offer?"""
        new_rank = self.ranks(new, default=math.inf)
        old_rank = self.ranks(to, default=math.inf)
        if new_rank == math.inf and old_rank == math.inf:
            raise ValueError
        return old_rank > new_rank

    def compare_offers(self, new_offer: str) -> str:
        """Compare new offer to existing matches return least preferred offer"""
        offer_to_reject = new_offer
        if not self.ranks(new_offer):
            return offer_to_reject
        for current_offer in self.matches:
            if self.prefers(new=offer_to_reject, to=current_offer):
                offer_to_reject = current_offer
        return offer_to_reject

    @property
    def has_capacity(self) -> bool:
        """Does this candidate have capacity for additional matches?"""
        return len(self.matches) < self.capacity

    def has_offers(self) -> bool:
        """Does this candidate have offers left to make?"""
        return self.offers_left is not None

    @property
    def rankings(self) -> Dict[Name, int]:
        """Dictionary of candidate's preference for each ranked offer"""
        if not self._rankings:
            self._rankings = {p: rank + 1 for rank, p in enumerate(self.prefs)}
        return self._rankings


class CandidateList:
    """Dictionary of candidates keyed by their name"""

    def __init__(
        self,
        preferences: Preferences,
        capacities: Capacities,
        default_capacity: int = 1,
    ) -> None:
        """Initializes a CandidateList

        Parameters
        ----------
        preferences: Dict[Name, List[Name]]
            Dictionary of candidates mapped to their preferences
        capacities: Dict[Name, int]
            Dictionary of candidates mapped to their capacity for matches
        default_capacity: int
            The maximum number of matches for any candidate whose capacity was
            not set explicitly in the capacities dictionary, default is 1
        """
        self.candidates: Dict[str, Candidate] = {}
        for name, prefs in preferences.items():
            capacity = capacities.get(name, default_capacity)
            candidate = Candidate(name, prefs, capacity)
            self.candidates[name] = candidate

    def get(self, name: str) -> Candidate:
        """Retrieve the candidate by their name"""
        if name not in self.candidates:
            raise KeyError
        return self.candidates.get(name)

    def items(self) -> List[Tuple[Name, Candidate]]:
        """Return the candidates as a list of tuples to iterate over"""
        return self.candidates.items()

    def to_list(self) -> List[Name]:
        """Return the candidates as a list"""
        return list(self.candidates.keys())
