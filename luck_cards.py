class LuckCard:
    EFFECTS = [
        "advance_steps",
        "advance_to_name",
        "advance_to_nearest",
        "collect",
        "collect_from_players",
        "get_out_of_jail_free",
        "ignore_salary",
        "pay",
        "pay_factor",
        "pay_per_hotel",
        "pay_per_house",
        "pay_players"
    ]

    CHANCE = 0
    COMMUNITY_CHEST = 1

    def __init__(self, text, **effects):
        self.text = text
        self.effects = {}
        for effect in LuckCard.EFFECTS:
            self.effects[effect] = None

        for effect, value in effects.items():
            if effect not in LuckCard.EFFECTS:
                raise ValueError(f"Invalid luck card effect: {effect}")

            self.effects[effect] = value

    def __getitem__(self, item):
        return self.effects[item]

    def __repr__(self):
        return self.text

    def get_not_none_effects(self):
        return_value = {}
        for effect, value in self.effects.items():
            if value is not None:
                return_value[effect] = value

        return return_value


class ChanceCard(LuckCard):
    def __init__(self, text, **effects):
        super().__init__(text, **effects)


class CommunityChestCard(LuckCard):
    def __init__(self, text, **effects):
        super().__init__(text, **effects)
