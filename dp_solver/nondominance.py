class Nondominance:
    @staticmethod
    def is_nondominated(cost1, cost2):
        return all(c1 <= c2 for c1, c2 in zip(cost1, cost2)) and any(c1 < c2 for c1, c2 in zip(cost1, cost2))
