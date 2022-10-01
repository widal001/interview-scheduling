from __future__ import annotations
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
        self.rankings = {p: rank for rank, p in enumerate(prefs)}
        self.offers_left = (offer for offer in prefs)
        self.matches = set()

    def rank_for(self, offer: str) -> Optional[int]:
        return self.rankings.get(offer)

    def prefers(self, new: str, to: str) -> bool:
        """Does the candidate prefer new offer to the current offer"""
        new_rank = self.rank_for(new)
        old_rank = self.rank_for(to)
        if not new_rank:
            return False
        return old_rank > new_rank

    def compare_offers(self, new_offer: str) -> str:
        offer_to_reject = new_offer
        if not self.rank_for(new_offer):
            return offer_to_reject
        for current_offer in self.matches:
            if self.prefers(new=offer_to_reject, to=current_offer):
                offer_to_reject = current_offer
        return offer_to_reject

    @property
    def has_capacity(self) -> bool:
        return len(self.matches) < self.capacity


class CandidateList:
    def __init__(
        self,
        preferences: Preferences,
        capacities: Capacities,
        default_capacity: int,
    ) -> None:

        self.candidates: Dict[str, Candidate] = {}

        for name, prefs in preferences:
            capacity = capacities.get(name, default_capacity)
            candidate = Candidate(name, prefs, capacity)
            self.candidates[name] = candidate

    def get(self, name: str) -> Candidate:
        if name not in self.candidates:
            raise KeyError
        return self.candidates.get(name)

    def to_list(self) -> List[Name]:
        return list(self.candidates.keys())
