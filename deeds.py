# Deed classes, the deeds that can be owned by players
class Deed:  # should be abstract
    def __init__(self, price):
        self.price = price
        self.mortgaged = False
        self.name = None
        self.owner = None


class LotDeed(Deed):
    def __init__(self, price, building_cost, rent_per_building,
                 monopoly_factor=2, mortgage_factor=0.5, mortgage_interest=1.1):
        self.building_cost = building_cost
        self.rent_per_building: tuple = rent_per_building
        self.monopoly_factor = monopoly_factor
        self.mortgage_factor = mortgage_factor
        self.mortgage_interest = mortgage_interest

        super().__init__(price)


class RailroadDeed(Deed):
    def __init__(self, price=200):
        super().__init__(price)


class UtilityDeed(Deed):
    def __init__(self, price=150):
        super().__init__(price)
