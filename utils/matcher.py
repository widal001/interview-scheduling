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
        requests = {}
        match_log = []
        p_matches = {p: [] for p in self.positions}
        c_matches = {c: [] for c in self.candidates}

        # populate requests based on candidate preference
        for c in candidates:
            prefs = self.c_prefs[c]
            requests[c] = {"active": sorted(prefs, key=prefs.get), "on hold": []}

        while candidates:

            new_candidate = candidates.pop(0)
            requests_left = requests[new_candidate]["active"]

            if requests_left:
                if len(c_matches[new_candidate]) >= c_max:
                    requests[new_candidate]["on hold"].extend(requests_left)
                    continue
                else:
                    next_position = requests_left.pop(0)
            else:
                continue

            # tries to get position's preference for candidate making request
            pref_for_request = self.p_prefs[next_position].get(new_candidate)

            if not pref_for_request:
                candidates.append(new_candidate)

            elif len(p_matches[next_position]) >= p_max:
                drop_candidate = new_candidate

                for i in range(len(p_matches[next_position])):
                    if (
                        self.p_prefs[next_position][drop_candidate]
                        < self.p_prefs[next_position][p_matches[next_position][i]]
                    ):
                        keep_candidate = drop_candidate
                        drop_candidate = p_matches[next_position][i]
                        p_matches[next_position][i] = keep_candidate

                if drop_candidate != new_candidate:
                    c_matches[drop_candidate].remove(next_position)
                    c_matches[new_candidate].append(next_position)

            else:
                p_matches[next_position].append(new_candidate)
                c_matches[new_candidate].append(next_position)

            candidates.append(new_candidate)

        self.c_remaining = [c for c, m in c_matches.items() if len(m) < c_min]
        self.p_remaining = [p for p, m in p_matches.items() if len(m) < p_min]
        self.log = match_log
        self.c_matches = c_matches
        self.p_matches = p_matches
