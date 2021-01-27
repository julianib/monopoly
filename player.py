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

        self.auction_min = random.randint(0, 100)
        self.auction_max = self.auction_min + random.randint(0, 900)
        self.participate_in_auction_chance = round(random.random(), 2)
        self.deed_buy_chance = round(random.random() / 2, 2)
        self.deeds = []
        self.get_out_of_jail_free_cards = []
        self.is_jailed = False
        self.rolls_in_jail_left = 0
        self.is_bankrupt = False
        self.money = game.starting_money
        self.name = "Player " + str(name)
        self.pos = 0  # position of player in board.spaces
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

        print(f"Landed on {self.pos}: {self.game.board[self.pos]}")

    def advance_to_name(self, to_name: str, collect_salary=True):
        # TODO bug if name is not unique:
        # this finds the first item from GO (index 0), not from the PLAYER POS!
        # fix: use get nearest index from of, add str support there
        for i, space in enumerate(self.game.board.spaces):
            if space.name == to_name:
                self.advance_to_index(i, collect_salary=collect_salary)
                return

        raise ValueError(f"no space found with name: {to_name}")

    def advance_to_index(self, to_index: int, collect_salary=True):
        to_index %= self.game.board.n_spaces  # prevent index out of range

        take_steps = to_index - self.pos

        if self.pos > to_index:  # target space is behind player
            take_steps += self.game.board.n_spaces

        self.advance_steps(take_steps, collect_salary)

    def can_afford(self, amount) -> bool:
        if self.money >= amount:
            return True

        return False

    def do_turn(self):
        rolls = 0
        while True:
            rolls += 1
            dice_result, is_double = get_dice_result()
            print(f"Roll #{rolls}: {dice_result}")

            if self.is_jailed:
                if self.get_out_of_jail_free_cards:
                    self.game.append_get_out_of_jail_free_card(self.get_out_of_jail_free_cards.pop())
                    print("Used a get out of jail free card")

                else:
                    if not is_double:
                        self.rolls_in_jail_left -= 1
                        if self.rolls_in_jail_left:
                            print(f"Didn't throw a double, still in jail "
                                  f"(rolls left: {self.rolls_in_jail_left})")
                            break

                        else:  # forced to pay the fine to get out
                            self.pay(self.game.jail_fine, tax_pile=True)

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

    def pay(self, amount, tax_pile=True):
        transfer_amount = min(amount, self.money)
        self.money -= transfer_amount

        if tax_pile:
            print(f"{self.name} threw ${transfer_amount} onto the tax pile")
            self.game.tax_pile += transfer_amount
        else:
            print(f"{self.name} paid ${transfer_amount} to the bank")

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
                print("Grabbing all the money on the tax pile!")
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
            print("Just visiting!")
            return

        if space_type is Tax:
            space: Tax
            self.pay(space.tax_amount, tax_pile=True)
            return

        # Spaces that have deeds (and maybe an owner)
        assert isinstance(space, HasDeed), "no proper handle for this non-HasDeed space"
        deed = space.deed
        owner: Player = deed.owner

        if owner == self:  # assuming "self" is never None
            print(f"You own {space} already!")
            return

        elif owner:  # owned by someone else, pay rent
            print(f"{space} is owned by {owner.name}")
            if space_type is Lot:  # todo double the rent if unimproved and owner has all lots in this color group
                space: Lot
                rent = deed.rent_per_building[space.buildings]
                if pay_factor:
                    rent *= pay_factor

            elif space_type is Railroad:
                n_railroads_owned = len([deed for deed in owner.deeds if type(deed) == RailroadDeed])
                assert n_railroads_owned > 0, "discrepancy in owner data, superposition railroad?"
                rent = Railroad.RENT * Railroad.BASE ** (n_railroads_owned - 1)

                if pay_factor:
                    rent *= pay_factor

            else:  # if space_type is Utility
                assert move_reason in MoveReason.get_reasons(), "unknown move reason"

                if move_reason == MoveReason.LUCK_CARD:
                    dice_result, _ = get_dice_result()
                    print(f"{self} rolled {dice_result} (utility rent)")
                    dice_sum = sum(dice_result)

                else:  # if move_reason == MoveReason.DICE_ROLL
                    dice_sum = sum(self.last_dice_result)

                if not pay_factor:
                    n_utility_owned = len([deed for deed in owner.deeds if type(deed) == UtilityDeed])
                    assert n_utility_owned > 0, "discrepancy in owner data, superposition utility?"

                    pay_factor = Utility.OWNED_FACTOR[n_utility_owned - 1]

                rent = dice_sum * pay_factor

            print(f"Calculated rent owed: ${rent}")
            self.pay_player(owner, rent)

        else:  # not owned by anyone, todo: decide whether to buy or not
            if self.can_afford(deed.price):
                rand = random.random()
                if rand < self.deed_buy_chance:
                    print(f"Buying the deed of {space}...")
                    self.pay(deed.price, tax_pile=False)
                    self.deeds.append(deed)
                    deed.owner = self
                else:
                    print(f"Decided not to buy the deed of {space}")
                    self.game.auction_deed(deed)

            else:
                print(f"Can't afford to buy the deed of {space}")
                self.game.auction_deed(deed)

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
            self.pay(card["pay"], tax_pile=True)

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
