from __future__ import annotations
import math
from typing import List, Optional, Dict

Name = str
Preferences = Dict[Name, List[Name]]
Capacities = Dict[Name, int]


class Candidate:
    def __init__(
        self,
        name: Name,
        prefs: List[Name],
        capacity: int,
    ) -> None:
        self.name = name
        self.prefs = prefs
        self.capacity = capacity
        self._offers_left = (offer for offer in prefs)
        self.matches = set()
        self._rankings = None

    def rank_for(
        self,
        offer: str,
        default: Optional[int] = None,
    ) -> Optional[int]:
        """Return candidate's ranking of a given offer, with optional default"""
        return self.rankings.get(offer, default)

    def prefers(self, new: str, to: str) -> bool:
        """Does the candidate prefer new offer to the current offer?"""
        new_rank = self.rank_for(new, default=math.inf)
        old_rank = self.rank_for(to, default=math.inf)
        if new_rank == math.inf and old_rank == math.inf:
            raise ValueError
        return old_rank > new_rank

    def compare_offers(self, new_offer: str) -> str:
        """Compare new offer to existing matches return least preferred offer"""
        offer_to_reject = new_offer
        if not self.rank_for(new_offer):
            return offer_to_reject
        for current_offer in self.matches:
            if self.prefers(new=offer_to_reject, to=current_offer):
                offer_to_reject = current_offer
        return offer_to_reject

    @property
    def has_capacity(self) -> bool:
        """Does this candidate have capacity for additional matches?"""
        return len(self.matches) < self.capacity

    @property
    def rankings(self) -> Dict[Name, int]:
        """Dictionary of candidate's preference for each ranked offer"""
        if not self._rankings:
            self._rankings = {p: rank for rank, p in enumerate(self.prefs)}
        return self._rankings


class CandidateList:
    """Dictionary of candidates keyed by their name"""

    def __init__(
        self,
        preferences: Preferences,
        capacities: Capacities,
        default_capacity: int,
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
            not set explicitly in the capacities dictionary
        """
        self.candidates: Dict[str, Candidate] = {}
        for name, prefs in preferences.items():
            capacity = capacities.get(name, default_capacity)
            candidate = Candidate(name, prefs, capacity)
            self.candidates[name] = candidate

    def get(self, name: str) -> Candidate:
        if name not in self.candidates:
            raise KeyError
        return self.candidates.get(name)

    def to_list(self) -> List[Name]:
        return list(self.candidates.keys())
