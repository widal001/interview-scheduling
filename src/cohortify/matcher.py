from __future__ import annotations  # prevents NameErrors for typing
from typing import Dict

Preferences = Dict[str, Dict[str, int]]


class Matcher:
    """Matches Candidates and Positions for interviews"""

    def __init__(self, c_prefs: Preferences, p_prefs: Preferences):
        """Initializes the Matcher class for interview or placement matching

        Parameters
        ----------
        c_prefs:
            Dictionary of candidate's rankings of positions with format:
            {"CandidateA": {"PositionA": 1, "PositionB": 2}}
            p_prefs: p_prefs[p][c] is position p's ranking of candidate c
        """
        self.c_prefs = c_prefs
        self.p_prefs = p_prefs
        self.candidates = list(c_prefs.keys())
        self.positions = list(p_prefs.keys())

        # set by self.assign_interviews()
        self.c_remaining: list = None
        self.p_remaining: list = None
        self.log: list = []
        self.c_matches: dict = {}
        self.p_matches: dict = {}
        self.requests_left: dict = {}

    def assign_interviews(
        self,
        c_min: int = 0,
        c_max: int = 100,
        p_min: int = 0,
        p_max: int = 1000,
    ) -> None:
        """Match candidates to positions for interviews

        Parameters
        ----------
        c_min: int, optional
            The minimum number of interviews each candidate should receive.
            Default is to have no minimum requirement.
        c_max: int, optional
            The maximum number of interviews each candidate should receive.
            Default is a limit of 100 interviews per candidate.
        p_min: int, optional
            The minimum number of interviews each candidate should receive.
            Default is to have no minimum requirement.
        p_max: int, optional
            The maximum number of interviews each candidate should receive.
            Default is a limit of 1000 interviews per position.
        """
        # create copies of
        candidates = self.candidates.copy()
        p_prefs = self.p_prefs
        requests = {}
        match_log = []  # TODO: Add log
        p_matches = {p: [] for p in self.positions}
        c_matches = {c: [] for c in self.candidates}
        _round = 1

        # populate requests based on candidate preference
        for c in candidates:
            prefs = self.c_prefs[c]
            requests[c] = {
                "active": sorted(prefs, key=prefs.get),
                "on hold": [],
            }

        while candidates:
            # gets the next candidate from the pool
            _round += 1
            c = candidates.pop(0)
            requests_left = requests[c]["active"]

            # skip c if they have no more requests
            if not requests_left:
                continue
            # or reached the max number of interviews
            if len(c_matches[c]) >= c_max:
                requests[c]["on hold"].extend(requests_left)
                continue

            # otherwise grab the next position c prefers
            p = requests_left.pop(0)
            pref = p_prefs[p]
            matches = p_matches[p]

            # if p didn't rank c, add them back to pool
            if not pref.get(c):
                print(f"{p} didn't rank {c}")
                candidates.append(c)
                continue
            # if p already has max number of interviews
            if len(matches) >= p_max:
                c_to_drop = c
                # check if c preferred to any current matches
                for i in range(len(matches)):
                    current_match = p_matches[p][i]
                    # if c is preferred to a current match
                    if pref[c_to_drop] < pref[current_match]:
                        # swap places, then repeat loop
                        c_to_keep = c_to_drop
                        c_to_drop = current_match
                        p_matches[p][i] = c_to_keep
                # if c was preferred to a previous match
                if c_to_drop != c:
                    # move p from previous match to c's list
                    c_matches[c_to_drop].remove(p)
                    c_matches[c].append(p)
                    # TODO: check if c_to_drop has requests on hold
            # otherwise add c to p's list and vice versa
            else:
                p_matches[p].append(c)
                c_matches[c].append(p)

            # add c back to pool
            candidates.append(c)

        self.c_remaining = [c for c, m in c_matches.items() if len(m) < c_min]
        self.p_remaining = [p for p, m in p_matches.items() if len(m) < p_min]
        self.log = match_log
        self.c_matches = c_matches
        self.p_matches = p_matches
        self.requests_left = {c: r["on hold"] for c, r in requests.items()}
