from __future__ import annotations
from typing import List, Optional


class Candidate:
    def __init__(
        self,
        name: str,
        prefs: List[str],
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

    def copy(self) -> Candidate:
        return Candidate(
            name=self.name,
            prefs=self.prefs,
            capacity=self.capacity,
        )

    @property
    def has_capacity(self) -> bool:
        return len(self.matches) < self.capacity
