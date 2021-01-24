from util import *
from game import Game


require_input = False
def main():
    game = Game()
    game.print_board()
    while not game.game_over:
        game.next_turn()

        if require_input:
            input_str = input()
            if input_str:
                break


if __name__ == '__main__':
    main()