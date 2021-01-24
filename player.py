from util import *
from cards import Card


class Player:
    def __init__(self, game, name):
        self.game = game

        self.deeds = []
        self.in_jail = False
        self.is_bankrupt = False
        self.money = 0
        self.name = "Player " + str(name)
        self.pos = 0

    def __repr__(self):
        return self.name + " @ " + POS_TO_SPACE[self.pos]

    def do_turn(self):
        rolls = 0
        while True:
            rolls += 1
            dice_result, is_double = get_dice_result()
            print(f"Roll {rolls}: {dice_result}")
            self.advance(sum(dice_result))
            self.resolve_space()

            if not is_double:
                break

            elif rolls == 3:
                pass  # go to jail

    def earn(self, amount):
        self.money += amount
        print(f"Earned ${amount}")

    def tax(self, amount):
        if self.can_afford(amount):
            self.money -= amount

        else:
            # ask for loans or something, not enough money
            raise Bankrupt

    def advance(self, steps, collect_go=True):
        print(f"Advancing {steps} steps...")
        while steps:
            self.pos += 1
            self.pos %= 40
            steps -= 1

            if collect_go and self.pos == 0 and steps > 0:
                print(f"Passed GO")
                self.earn(200)

    def advance_to(self, space):
        pass

    def go_to_jail(self):
        self.advance_to("IJ")
        self.in_jail = True

    def resolve_space(self, pay_flag=None, factor=0):
        space: str = self.game.board.get_space(self.pos)
        print(f"Resolving space: {space}")

        if space == "FP" and FREE_PARKING_COLLECT_PILE:
            return

        if space == "GJ":
            self.go_to_jail()
            return

        if space == "GO":
            self.earn(200)
            return

        if space == "IJ":
            return

        if space.startswith("c"):
            card = self.game.board.draw_chance_card()
            self.resolve_card(card)
            return

        if space.startswith("y"):
            card = self.game.board.draw_community_chest_card()
            self.resolve_card(card)
            return

        # if it reaches here, space has a deed

        owner = self.game.board.get_owner(space)
        if owner:
            rent = self.game.board.get_deed(space).rent  # todo fix
            self.pay_advanced(owner, rent, pay_flag, factor)

        else:
            if self.can_afford(self.game.board.get_deed(space).cost):
                self.pay_bank()  # todo fix

    def can_afford(self, amount):
        if self.money >= amount:
            return True

        return False

    def pay(self, player, amount):
        transfer_amount = min(amount, self.money)
        player.earn(transfer_amount)
        self.money -= transfer_amount
        print(f"{self} paid {player} ${transfer_amount}")

        if not self.money:
            raise Bankrupt

    def pay_advanced(self, player, rent, pay_flag, factor):
        if pay_flag == Card.RENT:
            amount = rent * factor

        elif pay_flag == Card.THROW_DICE:
            amount = sum(get_dice_result()[0]) * factor

        else:
            raise ValueError(f"Invalid pay flag: {pay_flag}")

        self.pay(player, amount)

    def resolve_card(self, card):
        print(f"Resolving card: {card}")
        if card["advance"]:
            self.advance(card["advance"], collect_go=not card["ignore_go"])
            self.resolve_space()
