from util import *
from board import Board
from player import Player


class Game:
    def __init__(self, n_players=4, max_turns=1000):
        print(f"Initializing game with {n_players} players")
        self.n_players = n_players
        self.max_turns = max_turns

        self.players = []
        for i in range(1, n_players + 1):
            player = Player(self, i)
            self.players.append(player)

        self.board = Board(self)
        self.chance_cards = []
        self.community_chest_cards = []
        self.current_turn = 0
        self.game_over = False
        self.jail_fine = 50
        self.n_get_out_of_jail_free_cards_used = 0
        self.n_salary_collected = 0
        self.n_chance_cards_drawn = 0
        self.n_community_chest_cards_drawn = 0
        self.next_turn_player_index = random.randint(0, n_players - 1)
        self.rolls_required_to_go_to_jail = 3
        self.rolls_in_jail = 3
        self.tax_pile = 0

        self.reset_luck_cards()

    def check_game_over(self) -> bool:
        n_non_bankrupt_players = len(self.get_non_bankrupt_players())

        if n_non_bankrupt_players == 1:
            print("GAME OVER - only 1 player left")
            return True

        if n_non_bankrupt_players == 0:
            print("GAME OVER - 0 players left somehow")
            return True

        if self.current_turn == self.max_turns:
            print(f"GAME OVER - max turns reached ({self.max_turns})")
            return True

        return False

    def draw_luck_card(self, card_class: type) -> LuckCard:
        assert card_class in LuckCard.get_card_classes(), "invalid luck card class"

        print(f"Drawing luck card: {card_class.__name__}...")

        if card_class is ChanceCard:
            card = self.chance_cards.pop(0)  # todo catch exception if no cards left
            if not card["get_out_of_jail_free"]:
                self.chance_cards.append(card)

            self.n_chance_cards_drawn += 1

        else:  # if card_class is CommunityChestCard:
            card = self.community_chest_cards.pop(0)  # todo catch exception
            if not card["get_out_of_jail_free"]:
                self.community_chest_cards.append(card)

            self.n_community_chest_cards_drawn += 1

        return card

    def get_non_bankrupt_players(self) -> list:
        return [player for player in self.players if not player.is_bankrupt]

    def next_turn(self):
        dice_roller = self.players[self.next_turn_player_index]
        if dice_roller.is_bankrupt:
            print(f"{dice_roller.name} is already bankrupt, skipping turn")
            return

        self.current_turn += 1
        print(f"/// TURN {self.current_turn}: {dice_roller}")

        try:
            dice_roller.do_turn()
        except Bankrupt:
            dice_roller.is_bankrupt = True
            print(f"{dice_roller.name} is bankrupt! bye")
        except EndTurn:
            print(f"{dice_roller.name}'s turn ended")

        self.update_next_turn_player_index()
        if self.check_game_over():
            self.game_over = True

    def update_next_turn_player_index(self):
        self.next_turn_player_index += 1
        self.next_turn_player_index %= len(self.players)

    def used_get_out_of_jail_free_card(self, card):
        assert type(card) in LuckCard.get_card_classes(), "invalid GOOJF card class"

        self.n_get_out_of_jail_free_cards_used += 1

        if isinstance(card, ChanceCard):
            self.chance_cards.append(card)
            return

        if isinstance(card, CommunityChestCard):
            self.community_chest_cards.append(card)
            return

    def reset_luck_cards(self):
        print(f"Resetting luck cards (classes: {LuckCard.get_card_classes_str()})...")

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
            ChanceCard("Go directly to jail", go_directly_to_jail=True),
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
            CommunityChestCard("Go directly to jail", go_directly_to_jail=True),
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
