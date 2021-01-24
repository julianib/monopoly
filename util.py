import random


ASSETS_FOLDER = "assets"

PASS_GO_REWARD = 200
INCOME_TAX_AMOUNT = 200
LUXURY_TAX_AMOUNT = 100
RAILROAD_PRICE = 200
FREE_PARKING_COLLECT_PILE = True  # house rule

BOARD_SPACES = {}
with open(ASSETS_FOLDER + "/board_spaces.txt", "r") as f:
    for line in f.readlines():
        if line.startswith("#"):
            continue

        line_split = line.strip().split()
        BOARD_SPACES[line_split[0]] = line_split[1]

    assert len(BOARD_SPACES) == 40
    print("Read board_spaces.txt")

POS_TO_SPACE = list(BOARD_SPACES.keys())


def get_dice_result():
    dice = [random.randint(1, 6), random.randint(1, 6)]
    is_double = dice[0] == dice[1]
    return dice, is_double


class Bankrupt(Exception):
    pass
