from util import *


class MoveReason:
    DICE_ROLL = 0
    LUCK_CARD = 1

    @staticmethod
    def get_reasons():
        return [MoveReason.DICE_ROLL, MoveReason.LUCK_CARD]


class Player:
    def __init__(self, game, name):
        self.game = game

        self.lot_deeds = []
        self.railroad_deeds = []
        self.utility_deeds = []
        self.get_out_of_jail_free_cards = []
        self.is_jailed = False
        self.rolls_in_jail_left = 0
        self.is_bankrupt = False
        self.money = 1000
        self.name = "Player " + str(name)
        self.pos = 0  # index of board.spaces
        self.last_dice_result = []

    def __repr__(self):
        return f"{self.name} @ {self.pos} ({self.game.board[self.pos]}) with ${self.money}"

    def advance_steps(self, steps, collect_salary=True):
        # assert steps != 0, "attempted to move 0 steps"

        if steps < 0:  # backwards
            # todo verify moving backwards never gives GO salary
            print(f"Going back {steps} steps...")
            while steps < 0:
                self.pos -= 1
                if self.pos < 0:
                    self.pos += self.game.board.n_spaces

                steps += 1

        else:
            print(f"Advancing {steps} steps...")
            while steps:
                self.pos += 1
                self.pos %= self.game.board.n_spaces

                steps -= 1

                if steps > 0:  # steps left, so passed a space
                    passed_space = self.game.board[self.pos]
                    if collect_salary and type(passed_space) == Go:
                        # todo add some .player_passed method for spaces for flexibility
                        print(f"Passed GO, collecting salary...")
                        self.earn(passed_space.salary)
                        self.game.n_salary_collected += 1

        print(f"Landed on {self.game.board[self.pos]}")

    def advance_to_name(self, to_name: str, collect_salary=True):
        # TODO bug: this finds the first item from GO (index 0), not from the PLAYER POS!

        for i, space in self.game.board:
            if space.name == to_name:
                self.advance_to_index(i, collect_salary=collect_salary)
                return

        raise ValueError(f"no space found with name: {to_name}")

    def advance_to_index(self, to_index: int, collect_salary=True):
        take_steps = to_index - self.pos

        if self.pos > to_index:  # target space is behind player, so go around the board
            take_steps += self.game.board.n_spaces

        self.advance_steps(take_steps, collect_salary)

    def can_afford(self, amount) -> bool:
        if self.money >= amount:
            return True

        return False

    def do_turn(self):  # todo check for jail status
        rolls = 0
        while True:
            rolls += 1
            dice_result, is_double = get_dice_result()
            print(f"Roll #{rolls}: {dice_result}")

            if self.is_jailed:
                if self.get_out_of_jail_free_cards:
                    self.game.used_get_out_of_jail_free_card(self.get_out_of_jail_free_cards.pop())
                    print("Used a get out of jail free card")

                else:
                    if not is_double:
                        self.rolls_in_jail_left -= 1
                        if self.rolls_in_jail_left:
                            print(f"Didn't throw a double, still in jail "
                                  f"(rolls left: {self.rolls_in_jail_left}")
                            break

                        else:  # forced to pay the fine to get out
                            self.pay_tax(self.game.jail_fine)

            elif is_double and rolls == self.game.rolls_required_to_go_to_jail:
                self.go_directly_to_jail()  # raises EndTurn
                return

            self.last_dice_result = dice_result
            self.advance_steps(sum(dice_result))
            self.resolve_current_space(MoveReason.DICE_ROLL)

            if self.is_jailed:
                self.is_jailed = False
                break  # not allowed to throw again if player just got out of jail

            if not is_double:
                break

    def earn(self, amount):
        self.money += amount
        print(f"{self.name} earned ${amount}")

    def go_directly_to_jail(self):  # send to jail and end turn
        self.advance_to_index(self.game.board[Jail], collect_salary=False)
        self.is_jailed = True
        self.rolls_in_jail_left = self.game.rolls_in_jail
        raise EndTurn

    def pay_player(self, player, amount):
        assert player != self, "tried to pay self"

        transfer_amount = min(amount, self.money)
        print(f"{self.name} pays {player.name} ${transfer_amount}")
        self.money -= transfer_amount
        player.earn(transfer_amount)

        if not self.money:
            raise Bankrupt

    def pay_tax(self, amount):
        transfer_amount = min(amount, self.money)
        print(f"{self.name} dumped ${transfer_amount} on the tax pile")
        self.money -= transfer_amount
        self.game.tax_pile += transfer_amount

        if not self.money:
            raise Bankrupt

    def resolve_current_space(self, move_reason, pay_factor=None):
        space = self.game.board[self.pos]
        print(f"Resolving space: {space}...")
        space.n_landed_on += 1
        space_type = type(space)

        # Spaces that do not have deeds
        if space_type is Chance:
            card = self.game.draw_luck_card(ChanceCard)
            self.resolve_luck_card(card)
            return

        if space_type is CommunityChest:
            card = self.game.draw_luck_card(CommunityChestCard)
            self.resolve_luck_card(card)
            return

        if space_type is FreeParking:
            space: FreeParking
            if space.collect_tax_pile:
                self.earn(self.game.tax_pile)
                self.game.tax_pile = 0
            return

        if space_type is Go:
            space: Go
            self.earn(space.salary)
            self.game.n_salary_collected += 1
            return

        if space_type is GoToJail:
            self.go_directly_to_jail()
            return  # never reaches this, as go_jail() raises EndTurn

        if space_type is Jail:
            return  # no effect

        if space_type is Tax:
            space: Tax
            self.pay_tax(space.tax_amount)
            return

        # Spaces that have deeds
        assert isinstance(space, HasDeed)
        deed = space.deed
        owner: Player = deed.owner

        if space_type is Lot:
            if owner:
                if owner == self:
                    return

                space: Lot
                rent = deed.rent_per_building[space.buildings]
                if pay_factor:
                    rent *= pay_factor

                self.pay_player(owner, rent)

            else:
                pass  # purchase or something

            return

        if space_type is Railroad:
            if owner:
                if owner == self:
                    return

                n_railroads_owned = len(owner.railroad_deeds)
                assert n_railroads_owned > 0, "discrepancy in owner data, superposition railroad?"

                rent = Railroad.BASE_RENT * 2**n_railroads_owned
                if pay_factor:
                    rent *= pay_factor

                self.pay_player(owner, rent)

            else:
                pass  # purchase or something

            return

        if space_type is Utility:
            if owner:
                if owner == self:
                    return

                assert move_reason in MoveReason.get_reasons(), "unknown move reason"
                if move_reason == MoveReason.LUCK_CARD:
                    dice_result, _ = get_dice_result()
                    print(f"{self} rolled {dice_result} (utility rent)")
                    dice_sum = sum(dice_result)

                else:
                    dice_sum = sum(self.last_dice_result)

                if not pay_factor:
                    n_utility_owned = len(owner.utility_deeds)
                    assert n_utility_owned > 0, "discrepancy in owner data, superposition utility?"

                    pay_factor = Utility.OWNED_FACTOR[n_utility_owned - 1]

                rent = dice_sum * pay_factor
                self.pay_player(owner, rent)

            else:
                pass  # purchase or something

            return

    def resolve_luck_card(self, card):
        print(f"Resolving luck card: {card}")

        if card["advance_steps"]:
            self.advance_steps(card["advance_steps"], collect_salary=not card["ignore_salary"])
            self.resolve_current_space(MoveReason.LUCK_CARD, pay_factor=card["pay_factor"])

        if card["advance_to_name"]:
            self.advance_to_name(card["advance_to_name"], collect_salary=not card["ignore_salary"])
            self.resolve_current_space(MoveReason.LUCK_CARD, pay_factor=card["pay_factor"])

        if card["advance_to_nearest"]:
            to_index = self.game.board.get_nearest_index_from_of(self.pos, card["advance_to_nearest"])
            self.advance_to_index(to_index, collect_salary=not card["ignore_salary"])
            self.resolve_current_space(MoveReason.LUCK_CARD, pay_factor=card["pay_factor"])

        if card["collect"]:
            self.earn(card["collect"])

        if card["collect_from_players"]:
            for player in self.game.get_non_bankrupt_players():
                if player == self:
                    continue

                player.pay_player(self, card["collect_from_players"])

        if card["get_out_of_jail_free"]:
            self.get_out_of_jail_free_cards.append(card)
            print("Received a Get Out of Jail Free card")

        if card["pay"]:
            self.pay_tax(card["pay"])

        if card["pay_per_hotel"]:
            pass  # todo implement

        if card["pay_per_house"]:
            pass  # todo implement

        if card["pay_players"]:
            for player in self.game.get_non_bankrupt_players():
                if player == self:
                    continue

                self.pay_player(player, card["pay_players"])

        # this card effect ends the turn, so first check for other effects
        if card["go_directly_to_jail"]:
            self.go_directly_to_jail()
