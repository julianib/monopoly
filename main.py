from util import *

from game import Game

REQUIRE_INPUT = False
MAX_TURNS = 100


def main():
    game = Game(max_turns=MAX_TURNS)
    while not game.game_over:
        game.next_turn()

        if REQUIRE_INPUT:
            input_str = input()
            if input_str:
                break

    richest_players = game.get_richest_players()
    if len(richest_players) == 1:
        print(f"Richest player: {richest_players[0].name}")
    else:
        print(f"Multiple winners!")

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
    lines.extend([f"{space} ({i}): {space.n_landed_on} times" for i, space in game.board.get_hotspots()[:5]])

    print("\n".join(lines))

    return game.current_turn


if __name__ == '__main__':
    start_time = time.time()
    turns = main()
    elapsed = time.time() - start_time
    print(f"/// Finished main() in {round(elapsed * 1000)} ms, {turns} turns")

# rules: https://www.hasbro.com/common/instruct/monins.pdf
# shortend: https://en.wikibooks.org/wiki/Monopoly/Official_Rules
# todo buy deeds if can afford
# todo don't go bankrupt if possessing deeds
# todo houses and hotels
# todo random trading if possessing > 50% of lots in a color group
# todo bidding on lots not wanted by the person who landed on it
# todo sell get ouf of jail free cards
# todo land on tax -> either pay the tax amount or 10% of total worth
# todo even if in jail, still able to buy and sell deeds, buildings and collect rent
# todo free parking house rule -> if no money on pile -> receive 100
# todo allowed to buy/sell buildings even if its not your turn
# todo auction buildings if there are not enough left to satisfy the demand of that turn
# todo before selling deeds, sell all buildings on that deed (with respect to other lots in that color group)
# todo selling buildings gives 0.5 * building cost back
# todo mortgaging Before an improved property can be mortgaged, all the buildings on all the properties of its color-group must be sold back to the Bank at half price.
# todo mortgage interest (10% default)
# todo when selling mortgaged property, buyer pays extra 10% interest if deciding not to unmortgage it
# todo unmortgaging: pay back mortgage-received money and 10% interest as penalty