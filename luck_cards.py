class LuckCard:
    EFFECTS = [
        "advance_steps",
        "advance_to_name",
        "advance_to_nearest",
        "collect",
        "collect_from_players",
        "get_out_of_jail_free",
        "go_directly_to_jail",
        "ignore_salary",
        "pay",
        "pay_factor",
        "pay_per_hotel",
        "pay_per_house",
        "pay_players"
    ]

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

    def get_not_none_effects(self) -> dict:
        return_value = {}
        for effect, value in self.effects.items():
            if value is not None:
                return_value[effect] = value

        return return_value

    @staticmethod
    def get_card_classes() -> list:
        return [ChanceCard, CommunityChestCard]

    @staticmethod
    def get_card_classes_str() -> list:
        return [clazz.__name__ for clazz in LuckCard.get_card_classes()]


class ChanceCard(LuckCard):
    def __init__(self, text, **effects):
        super().__init__(text, **effects)


class CommunityChestCard(LuckCard):
    def __init__(self, text, **effects):
        super().__init__(text, **effects)
