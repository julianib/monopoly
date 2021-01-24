class Card:
    PROPERTIES = [
        "advance",
        "advance_to",
        "advance_to_nearest",
        "collect",
        "collect_from_players",
        "factor",
        "get_out_of_jail_free",
        "ignore_go",
        "pay",
        "pay_flag",
        "pay_per_hotel",
        "pay_per_house",
        "pay_players"
    ]

    RENT = 0
    THROW_DICE = 1

    CHANCE = 0
    COMMUNITY_CHEST = 1

    def __init__(self, text, **properties):
        self.text = text
        self.properties = {}
        for prop in Card.PROPERTIES:
            self.properties[prop] = None

        for prop, value in properties.items():
            if prop not in Card.PROPERTIES:
                raise ValueError(f"Invalid card property for CardDrawingCard: {prop}")

            self.properties[prop] = value

    def __getitem__(self, item):
        return self.properties[item]

    def __repr__(self):
        return self.text


class ChanceCard(Card):
    def __init__(self, text, **properties):
        super().__init__(text, **properties)


class CommunityChestCard(Card):
    def __init__(self, text, **properties):
        super().__init__(text, **properties)


CHANCE_CARDS = [  # source: https://monopoly.fandom.com/wiki/Chance
    ChanceCard("Advance to GO", advance_to="GO"),
    ChanceCard("Advance to E3", advance_to="E3"),
    ChanceCard("Advance to C1", advance_to="C1"),
    ChanceCard("Advance to nearest utility, if owned throw dice & pay 10x",
               advance_to_nearest="U", pay_flag=Card.THROW_DICE,
               factor=10),
    ChanceCard("Advance to nearest railroad, if owned pay 2x rent",
               advance_to_nearest="R", pay_flag=Card.RENT,
               factor=2),
    ChanceCard("Bank pays dividend", collect=50),
    ChanceCard("Get Out of Jail Free", get_out_of_jail_free=True),
    ChanceCard("Go back 3 spaces", advance=-3),
    ChanceCard("Go directly to jail", advance_to="IJ", ignore_go=True),
    ChanceCard("Make property repairs", pay_per_house=25, pay_per_hotel=100),
    ChanceCard("Pay poor tax", pay=15),
    ChanceCard("Take a trip to R1", advance_to="R1"),
    ChanceCard("Take a walk on the Boardwalk", advance_to="H2"),
    ChanceCard("Elected Chairman, pay all players", pay_players=50),
    ChanceCard("Your building loan matures", collect=150),
    ChanceCard("You have won a competition", collect=100)
]


COMMUNITY_CHEST_CARDS = [  # source: https://monopoly.fandom.com/wiki/Community_Chest
    CommunityChestCard("Advance to GO", advance_to="GO"),
    CommunityChestCard("Bank error", collect=200),
    CommunityChestCard("Doctor's fees", pay=50),
    CommunityChestCard("From sale of stock, get $", collect=50),
    CommunityChestCard("Get Out of Jail Free", get_out_of_jail_free=True),
    CommunityChestCard("Go directly to jail", advance_to="IJ", ignore_go=True),
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