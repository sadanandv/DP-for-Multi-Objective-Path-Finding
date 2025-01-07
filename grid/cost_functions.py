class CostFunctions:
    @staticmethod
    def static_cost(x1, y1, x2, y2):
        return 1  # Constant cost for all transitions

    @staticmethod
    def dynamic_cost(x1, y1, x2, y2, time_step):
        return 1 + (time_step % 5)  # Example dynamic cost
