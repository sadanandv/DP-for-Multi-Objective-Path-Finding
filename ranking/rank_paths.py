class RankPaths:
    def __init__(self, paths, criteria):
        self.paths = paths
        self.criteria = criteria
        
    @staticmethod
    def rank(paths, criteria):
        completed_paths = [p for p in paths if p["completed"]]
        if criteria == "distance":
            return sorted(completed_paths, key=lambda p: p["cost"])
        elif criteria == "time":
            return sorted(completed_paths, key=lambda p: p["time"])
        return completed_paths
