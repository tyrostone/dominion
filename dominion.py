import random

from card_types import card_types


class Dominion(object):
    def __init__(self, players=2):
        self.players = self.generate_players(players)
        self.board = self.generate_board()
        self.starting_player = self.determine_starting_player()

    def run(self):
        pass

    def generate_board(self):
        return Board()

    def generate_players(self, players):
        players_list = []
        for player in range(players):
            players_list.append(Player())
        return players_list

    def determine_starting_player(self):
        random_int = random.randint(0, len(self.players)-1)
        return self.players[random_int]


class Player(object):
    def __init__(self):
        self.cards = self.generate_starting_cards()
        self.victory_points = len(self.cards['victory_cards'])
        self.is_starting = False

    def generate_starting_cards(self):
        cards = {}
        cards['treasure_cards'] = [TreasureCard('Copper') for x in range(7)]
        cards['victory_cards'] = [VictoryCard('Estate') for x in range(3)]
        return cards


class Board(object):
    def __init__(self):
        self.slots = self.generate_and_check_slots()

    def generate_and_check_slots(self):
        slots = []
        for x in range(10):
            new_slot_is_unique = False
            while not new_slot_is_unique:
                new_slot = Slot()
                new_slot_is_unique = self.check_slot_card_is_unique(
                    slots, new_slot)
            slots.append(new_slot)
        return slots

    def check_slot_card_is_unique(self, current_slot_list, slot):
        for s in current_slot_list:
            if s.card.name == slot.card.name:
                return False
        return True


class Slot(object):
    def __init__(self, card=None):
        self.num_cards = 10
        self.card = card if card is not None else self.generate_card()

    def generate_card(self):
        card_name = self.generate_random_card_name()
        return KingdomCard(name=card_name)

    def generate_random_card_name(self):
        names = card_types['kingdom']
        random_int = random.randint(0, len(names)-1)
        return names[random_int].keys()[0]


class Card(object):
    def __init__(self, card_type, name=None, cost=None):
        card_types_list = ['kingdom', 'treasure', 'victory']
        self.name = name
        self.type = card_type if card_type in card_types_list else None
        self.value = self.set_card_attribute(
            name, card_type, 'value')
        self.cost = self.set_card_attribute(
            name, card_type, 'cost')
        self.victory_points = self.set_card_attribute(
            name, card_type, 'victory_points')

    def set_card_attribute(self, name, card_type, attribute):
        return None if name is None else self.get_card_info_from_name(
            card_type, name, attribute)

    def get_card_info_from_name(self, card_type, name, info):
        for card in card_types[card_type]:
            if card.keys()[0] == name:
                try:
                    return card.values()[0][info]
                except KeyError:
                    return None


class KingdomCard(Card):
    def __init__(self, name=None):
        Card.__init__(self, card_type='kingdom', name=name)


class TreasureCard(Card):
    def __init__(self, name=None):
        Card.__init__(self, card_type='treasure', name=name)


class VictoryCard(Card):
    def __init__(self, name=None):
        Card.__init__(self, card_type='victory', name=name)
