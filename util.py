import random


def get_dice_result():
    dice = [random.randint(1, 6), random.randint(1, 6)]
    is_double = dice[0] == dice[1]
    return dice, is_double


class Bankrupt(BaseException):
    pass
