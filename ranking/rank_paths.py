class RankPaths:
    def __init__(self, paths, criteria):
        self.paths = paths
        self.criteria = criteria

    def rank(self):
        if self.criteria == "distance":
            return sorted(self.paths, key=lambda p: p["cost"])
        elif self.criteria == "time":
            return sorted(self.paths, key=lambda p: p["time"])
        return self.paths
