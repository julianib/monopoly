# Space classes, the various spaces found on the board
class Space:
    def __init__(self, name, has_deed=False):
        self.name = name
        self.has_deed = has_deed  # probably unnecessary, isinstance is sufficient

    def __repr__(self):
        return self.name


class Chance(Space):
    def __init__(self):
        super().__init__("Chance")


class CommunityChest(Space):
    def __init__(self):
        super().__init__("Community Chest")


class FreeParking(Space):
    def __init__(self, collect_tax_pile=True):
        self.collect_tax_pile = collect_tax_pile  # house rule -> True
        super().__init__("Free Parking")


class Go(Space):
    def __init__(self, salary=200):
        self.salary = salary
        super().__init__("GO")


class GoToJail(Space):
    def __init__(self):
        super().__init__("Go to jail")


class Jail(Space):
    def __init__(self):
        super().__init__(f"Jail")


class Tax(Space):
    def __init__(self, tax_type, tax_amount):
        self.tax_amount = tax_amount
        super().__init__(f"{tax_type} Tax: {tax_amount}")


# HasDeed classes, spaces that have a deed
class HasDeed(Space):
    def __init__(self, name, deed):
        self.deed = deed
        self.deed.name = name
        super().__init__(name, has_deed=True)


class Lot(HasDeed):
    def __init__(self, color_group, name, deed):
        self.color_group = color_group
        self.buildings = 0
        super().__init__(f"{color_group}{name}", deed)


class Railroad(HasDeed):
    BASE_RENT = 25

    def __init__(self, name, deed):
        super().__init__(f"Railroad {name}", deed)


class Utility(HasDeed):
    OWNED_FACTOR = 4, 10

    def __init__(self, name, deed):
        super().__init__(name, deed)
