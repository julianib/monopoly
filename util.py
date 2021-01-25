import random
import time
from typing import List

from spaces import *
from deeds import *
from luck_cards import *


def get_dice_result() -> tuple:
    dice = [random.randint(1, 6), random.randint(1, 6)]
    is_double = dice[0] == dice[1]
    return dice, is_double


class Bankrupt(BaseException):
    pass


class EndTurn(BaseException):
    pass
