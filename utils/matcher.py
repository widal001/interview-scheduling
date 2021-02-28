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
