from util import *
from cards import CHANCE_CARDS, COMMUNITY_CHEST_CARDS


class Board:
    def __init__(self, game):
        self.game = game
        self.spaces = BOARD_SPACES
        self.community_chest_cards = COMMUNITY_CHEST_CARDS
        self.chance_cards = CHANCE_CARDS

        random.shuffle(self.chance_cards)
        print(f"Shuffled {len(CHANCE_CARDS)} chance cards")
        random.shuffle(self.community_chest_cards)
        print(f"Shuffled {len(CHANCE_CARDS)} community chest cards")

    def __iter__(self):
        for i, space in enumerate(self.spaces):
            yield i, space

    def draw_chance_card(self):
        card = self.chance_cards.pop(0)
        if not card["get_out_of_jail_free"]:
            self.chance_cards.append(card)

        return card

    def draw_community_chest_card(self):
        card = self.community_chest_cards.pop(0)
        if not card["get_out_of_jail_free"]:
            self.chance_cards.append(card)

        return card

    def get_go_index(self) -> int:
        return self.get_index("GO")

    def get_index(self, of_space) -> int:
        for i, space in self:
            if space == of_space:
                return i

    def get_jail_index(self) -> int:
        return self.get_index("IJ")

    def get_owner(self, space):
        for player in self.game.players:
            if space in player.deeds:
                return player

    def get_space(self, of_index) -> str:
        for i, space in enumerate(self.spaces):
            if i == of_index:
                return space
