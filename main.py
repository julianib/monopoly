from game import Game

require_input = False


def main():
    game = Game()
    while not game.game_over:
        game.next_turn()

        if require_input:
            input_str = input()
            if input_str:
                break

    for player in game.players:
        print(f"{player.name}: ${player.money} (bankrupt={player.is_bankrupt})")


if __name__ == '__main__':
    main()

# todo buy deeds if can afford
# todo don't go bankrupt if possessing deeds
# todo houses and hotels
# todo random trading if possessing > 50% of lots in a color group
# todo jail and triple throwing to get out
# todo get out of jail free card functionality
