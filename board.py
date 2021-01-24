from util import *
from luck_cards import ChanceCard, CommunityChestCard
from spaces import *
from deeds import *


class Board:
    def __init__(self, game):
        self.game = game
        self.chance_cards = []
        self.community_chest_cards = []
        self.spaces = []
        self.n_spaces = 0

        self.reset_board()
        self.reset_luck_cards()

    def __iter__(self):
        for i, space in enumerate(self.spaces):
            yield i, space

    def draw_chance_card(self):
        print("Drawing Chance card...")

        card = self.chance_cards.pop(0)
        if not card["get_out_of_jail_free"]:
            self.chance_cards.append(card)

        return card

    def draw_community_chest_card(self):
        print("Drawing Community Chest card...")

        card = self.community_chest_cards.pop(0)
        if not card["get_out_of_jail_free"]:
            self.community_chest_cards.append(card)

        return card

    def get_go_index(self) -> int:
        return self.get_space_index(name="GO")

    def get_space_index(self, name, space_type=None) -> int:
        # for param, value in search_params.items():
        #     if param not in ["name", "group"]:
        #         raise ValueError(f"Invalid space search param: {param}")

        for i, space in self:
            if space_type and type(space) == space_type:
                return i

            if space.name == name:
                return i

    def get_jail_index(self) -> int:
        return self.get_space_index(name="Jail")

    def get_space_at(self, at_index) -> Space:
        for i, space in enumerate(self.spaces):
            if i == at_index:
                return space

    def get_nearest_index_from_of(self, pos, space_type):
        distances = []
        for i, space in self:
            if type(space) == space_type:
                distance = i - pos
                if pos > i:
                    distance += self.n_spaces

                distances.append(distance)

        if not distances:
            raise Exception(f"No such space type on this board: {space_type}")

        return min(distances) + pos

    def print_spaces(self):
        lines = ["/// BOARD SPACES:"]
        lines.extend([space.name for _, space in self])
        print("\n".join(lines))

    def reset_board(self):
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
        lots = [space for space in self.spaces if type(space) == Lot]
        print(f"Reset board: {self.n_spaces} spaces, with {len(lots)} lots")

    def reset_luck_cards(self):
        print("Resetting luck cards...")

        self.chance_cards = [
            # source: https://monopoly.fandom.com/wiki/Chance
            ChanceCard("Advance to GO", advance_to_name="GO"),
            ChanceCard("Advance to E3", advance_to_name="Ec"),
            ChanceCard("Advance to C1", advance_to_name="Ca"),
            ChanceCard("Advance to nearest utility, if owned throw dice & pay 10x",
                       advance_to_nearest=Utility, pay_factor=10),
            ChanceCard("Advance to nearest railroad, if owned pay 2x rent",
                       advance_to_nearest=Railroad, pay_factor=2),
            ChanceCard("Bank pays dividend", collect=50),
            ChanceCard("Get Out of Jail Free", get_out_of_jail_free=True),
            ChanceCard("Go back 3 spaces", advance_steps=-3),
            ChanceCard("Go directly to jail", advance_to_nearest=Jail, ignore_salary=True),
            ChanceCard("Make property repairs", pay_per_house=25, pay_per_hotel=100),
            ChanceCard("Pay poor tax", pay=15),
            ChanceCard("Take a trip to R1", advance_to_name="Railroad W"),
            ChanceCard("Take a walk on the Boardwalk", advance_to_name="Hb"),
            ChanceCard("Elected Chairman, pay all players", pay_players=50),
            ChanceCard("Your building loan matures", collect=150),
            ChanceCard("You have won a competition", collect=100)
        ]

        random.shuffle(self.chance_cards)
        print(f"Shuffled {len(self.chance_cards)} chance cards")

        self.community_chest_cards = [  # source: https://monopoly.fandom.com/wiki/Community_Chest
            CommunityChestCard("Advance to GO", advance_to_name="GO"),
            CommunityChestCard("Bank error", collect=200),
            CommunityChestCard("Doctor's fees", pay=50),
            CommunityChestCard("From sale of stock, get $", collect=50),
            CommunityChestCard("Get Out of Jail Free", get_out_of_jail_free=True),
            CommunityChestCard("Go directly to jail", advance_to_nearest=Jail, ignore_salary=True),
            CommunityChestCard("Grand Opera Night", collect_from_players=50),
            CommunityChestCard("Holiday Fund matures", collect=100),
            CommunityChestCard("Income tax refund", collect=20),
            CommunityChestCard("It is your birthday", collect_from_players=10),
            CommunityChestCard("Life insurance matures", collect=100),
            CommunityChestCard("Hospital fees", pay=50),
            CommunityChestCard("School fees", pay=50),
            CommunityChestCard("Receive consultancy fee", collect=25),
            CommunityChestCard("Assessed for street repairs", pay_per_house=40, pay_per_hotel=115),
            CommunityChestCard("Won second price in beauty contest", collect=10),
            CommunityChestCard("You inherit $", collect=100)
        ]

        random.shuffle(self.community_chest_cards)
        print(f"Shuffled {len(self.community_chest_cards)} community chest cards")
