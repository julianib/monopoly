from util import *
from board import Board
from player import Player


class Game:
    def __init__(self, n_players=4):
        print(f"Initializing game with {n_players} players")
        self.players = []
        for i in range(1, n_players + 1):
            player = Player(self, i)
            self.players.append(player)

        self.board = Board(self)
        self.current_turn = 0
        self.next_turn_player_index = random.randint(0, n_players - 1)
        self.game_over = False
        self.max_turns = 1000
        self.rolls_required_to_go_to_jail = 3
        self.tax_pile = 0

        self.board.print_spaces()

    def get_non_bankrupt_players(self):
        return [player for player in self.players if not player.is_bankrupt]

    def next_turn(self):
        dice_roller = self.players[self.next_turn_player_index]
        if dice_roller.is_bankrupt:
            print(f"{dice_roller} is already bankrupt, skipping turn")
            return

        self.current_turn += 1
        print(f"/// TURN {self.current_turn}: {dice_roller}")

        try:
            dice_roller.do_turn()
        except Bankrupt:
            dice_roller.is_bankrupt = True
            print(f"{dice_roller} ended up bankrupt!")

        self.update_next_turn_player_index()
        if self.check_game_over():
            self.game_over = True

    def update_next_turn_player_index(self):
        self.next_turn_player_index += 1
        self.next_turn_player_index %= len(self.players)

    def check_game_over(self):
        n_non_bankrupt_players = len(self.get_non_bankrupt_players())

        if n_non_bankrupt_players == 1:
            print("Game over - only 1 player left")
            return True

        if n_non_bankrupt_players == 0:
            print("Game over - 0 players left somehow")
            return True

        if self.current_turn == self.max_turns:
            print(f"Game over - max turns reached ({self.max_turns})")
            return True
