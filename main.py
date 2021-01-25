from util import *

from game import Game

REQUIRE_INPUT = False
MAX_TURNS = 100000


def main():
    game = Game(max_turns=MAX_TURNS)
    while not game.game_over:
        game.next_turn()

        if REQUIRE_INPUT:
            input_str = input()
            if input_str:
                break

    for player in game.players:
        print(f"{player.name}: ${player.money} (bankrupt={player.is_bankrupt})")

    lines = [
        "/// GAME STATS:",
        f"n salary collected: {game.n_salary_collected}",
        f"n chance cards drawn: {game.n_chance_cards_drawn}",
        f"n community chest cards drawn: {game.n_community_chest_cards_drawn}",
        f"Get out of jail free cards used: {game.n_get_out_of_jail_free_cards_used}",
        f"Most landed on tiles:",
    ]
    lines.extend([f"{i}: {space}, {space.n_landed_on} times" for i, space in game.board.get_hotspots()[:5]])

    print("\n".join(lines))

    return game.current_turn


if __name__ == '__main__':
    start_time = time.time()
    turns = main()
    elapsed = time.time() - start_time
    print(f"Finished main() in {round(elapsed * 1000)} ms, {turns} turns")

# rules source: https://en.wikibooks.org/wiki/Monopoly/Official_Rules
# todo buy deeds if can afford
# todo don't go bankrupt if possessing deeds
# todo houses and hotels
# todo random trading if possessing > 50% of lots in a color group
# todo get out of jail free card functionality
