from util import *


class Board:
    def __init__(self, game):
        self.game = game
        self.spaces = []
        self.n_spaces = 0

        self.reset()
        print(self)

    def __repr__(self):
        lines = ["/// THE BOARD:"]
        lines.extend([f"{i}: {space}" for i, space in self])
        return "\n".join(lines)

    def __iter__(self):
        return enumerate(self.spaces)

    def __getitem__(self, space_class_or_index):
        if isinstance(space_class_or_index, type(Space)):  # get (FIRST) index of found space
            for i, space in self:
                if type(space) is space_class_or_index:
                    return i

            raise ValueError(f"no such space class on board: {space_class_or_index}")

        assert isinstance(space_class_or_index, int), f"invalid type passed: {space_class_or_index}"

        return self.spaces[space_class_or_index]  # indexing item must an int

    def get_nearest_index_from_of(self, pos, space_type) -> int:
        distances = []
        for i, space in self:
            if type(space) is space_type:
                distance = i - pos
                if pos > i:
                    distance += self.n_spaces

                distances.append(distance)

        if not distances:
            raise ValueError(f"no such space type on board: {space_type}")

        return (min(distances) + pos) % self.n_spaces  # modulo needed?

    def get_hotspots(self) -> List[tuple]:
        with open(".temp.txt", "w") as f:
            spaces = [space.n_landed_on for _, space in self]
            f.write(",".join(spaces))

        return sorted(self, key=lambda t: t[1].n_landed_on, reverse=True)

    def reset(self):
        print("Resetting board...")

        self.spaces = [
            # from https://images-na.ssl-images-amazon.com/images/I/81btrHKgO0L._AC_SL1500_.jpg
            Go(),
            Lot("A", "a", LotDeed(60, 50, (2, 10, 30, 90, 160, 250))),
            CommunityChest(),
            Lot("A", "b", LotDeed(60, 50, (4, 20, 60, 180, 320, 450))),
            Tax("Income", 200),
            Railroad("W", RailroadDeed()),
            Lot("B", "a", LotDeed(100, 50, (6, 30, 90, 270, 400, 550))),
            Chance(),
            Lot("B", "b", LotDeed(100, 50, (6, 30, 90, 270, 400, 550))),
            Lot("B", "c", LotDeed(120, 50, (8, 40, 100, 300, 450, 600))),

            Jail(),
            Lot("C", "a", LotDeed(140, 100, (10, 50, 150, 450, 625, 750))),
            Utility("Electric Company", UtilityDeed()),
            Lot("C", "b", LotDeed(140, 100, (10, 50, 150, 450, 625, 750))),
            Lot("C", "c", LotDeed(160, 100, (12, 60, 180, 500, 700, 900))),
            Railroad("X", RailroadDeed()),
            Lot("D", "a", LotDeed(180, 100, (14, 70, 200, 550, 750, 950))),
            CommunityChest(),
            Lot("D", "b", LotDeed(180, 100, (14, 70, 200, 550, 750, 950))),
            Lot("D", "c", LotDeed(200, 100, (16, 80, 220, 600, 800, 1000))),

            FreeParking(),
            Lot("E", "a", LotDeed(220, 150, (18, 90, 250, 700, 875, 1050))),
            Chance(),
            Lot("E", "b", LotDeed(220, 150, (18, 90, 250, 700, 875, 1050))),
            Lot("E", "c", LotDeed(240, 150, (20, 100, 300, 750, 925, 1100))),
            Railroad("Y", RailroadDeed()),
            Lot("F", "a", LotDeed(260, 150, (22, 110, 330, 800, 975, 1150))),
            Lot("F", "b", LotDeed(260, 150, (22, 110, 330, 800, 975, 1150))),
            Utility("Water Works", UtilityDeed()),
            Lot("F", "c", LotDeed(280, 150, (24, 120, 360, 850, 1025, 1200))),

            GoToJail(),
            Lot("G", "a", LotDeed(300, 200, (26, 130, 390, 900, 1100, 1275))),
            Lot("G", "b", LotDeed(300, 200, (26, 130, 390, 900, 1100, 1275))),
            CommunityChest(),
            Lot("G", "c", LotDeed(320, 200, (28, 150, 450, 1000, 1200, 1400))),
            Railroad("Z", RailroadDeed()),
            Chance(),
            Lot("H", "a", LotDeed(350, 200, (35, 175, 500, 1100, 1300, 1500))),
            Tax("Luxury", 100),
            Lot("H", "b", LotDeed(400, 200, (50, 200, 600, 1400, 1700, 2000)))
        ]

        self.n_spaces = len(self.spaces)
        lots = [space for _, space in self if isinstance(space, Lot)]
        print(f"Reset board: {self.n_spaces} spaces, with {len(lots)} lots")
