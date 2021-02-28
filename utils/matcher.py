from pprint import pprint


class Matcher:
    def __init__(self, c_prefs, p_prefs):
        """Initializes the Matcher class for interview or placement matching

        Args:
            c_prefs: c_prefs[c][p] is candidate c's ranking of position p
            p_prefs: p_prefs[p][c] is position p's ranking of candidate c
        Returns:
            candidates: List of candidates who submitted preferences
            positions: List of positions who submitted preferences
        """
        self.c_prefs = c_prefs
        self.p_prefs = p_prefs
        self.candidates = list(c_prefs.keys())
        self.positions = list(p_prefs.keys())

    def assign_interviews(self, c_min=0, c_max=999, p_min=0, p_max=999):

        # create copies of
        candidates = self.candidates.copy()
        p_prefs = self.p_prefs
        requests = {}
        match_log = []  # TODO: Add log
        p_matches = {p: [] for p in self.positions}
        c_matches = {c: [] for c in self.candidates}
        round = 1

        # populate requests based on candidate preference
        for c in candidates:
            prefs = self.c_prefs[c]
            requests[c] = {"active": sorted(prefs, key=prefs.get), "on hold": []}

        while candidates:
            # gets the next candidate from the pool
            round += 1
            c = candidates.pop(0)
            requests_left = requests[c]["active"]

            # skip c if they have no more requests
            if not requests_left:
                continue
            # or reached the max number of interviews
            elif len(c_matches[c]) >= c_max:
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
            elif len(matches) >= p_max:
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
