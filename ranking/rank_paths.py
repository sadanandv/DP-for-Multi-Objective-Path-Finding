class RankPaths:
    def __init__(self, paths, criteria):
        self.paths = paths
        self.criteria = criteria

    def rank(self):
        """Rank paths by the specified criteria."""
        if self.criteria == "distance":  # Currently assumes "cost" is equivalent to "distance"
            return sorted(self.paths, key=lambda p: p["cost"])
        return self.paths
