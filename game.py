from util import *
from board import Board
from player import Player


class Game:
    def __init__(self, n_players=4):
        print(f"Initializing game with {n_players} players")
        self.players = []
        for i in range(n_players):
            player = Player(self, i + 1)
            self.players.append(player)

        self.board = Board(self)
        self.current_turn = 0
        self.next_turn_player_index = random.randint(0, n_players - 1)
        print(f"next_turn_player_index={self.next_turn_player_index}")
        self.game_over = False
        self.max_turns = 2

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
        if self.next_turn_player_index == len(self.players):
            self.next_turn_player_index = 0

    def remove_player(self, player):
        self.players.remove(player)
        print(player + " is bankrupt")

    def check_game_over(self):
        if len(self.players) == 1:
            print("Game over - only 1 player left")
            return True

        elif len(self.players) == 0:
            print("Game over - nobody left somehow")
            return True

        elif self.current_turn == self.max_turns:
            print("Max turns reached")
            return True

    def print_board(self):
        lines = ["Game board:"]
        append_chars = []
        for space in self.board.spaces:
            append_chars.append(space)

            if len(append_chars) == 10:
                lines.append(" | ".join(append_chars))
                append_chars = []

        print("\n".join(lines))
