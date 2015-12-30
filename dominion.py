import random

from card_types import card_types


class Dominion(object):
    def __init__(self, players=2):
        self.board = self.generate_board(players)
        self.players = self.check_and_generate_players(players)

    def run(self):
        self.starting_player = self.determine_player_order()
        current_turn = Turn(self.starting_player, self.board)
        return current_turn

    def generate_board(self, players):
        return Board(players)

    def check_and_generate_players(self, players):
        if players > 4:
            players = 4
        return self.generate_players(players)

    def generate_players(self, players):
        players_list = []
        for player in range(players):
            players_list.append(Player(self.board))
        return players_list

    def determine_player_order(self):
        starting_player = self.determine_starting_player()
        self.players = self.sort_players(starting_player)
        return starting_player

    def determine_starting_player(self):
        random_int = random.randint(0, len(self.players)-1)
        return self.players[random_int]

    def sort_players(self, starting_player):
        sorted_player_list = []
        player_list = self.players

        sorted_player_list.append(starting_player)
        for player in player_list:
            if player == starting_player:
                continue
            sorted_player_list.append(player)
        return sorted_player_list


class Turn(object):
    def __init__(self, player, board):
        self.board = board
        self.player = player
        self.actions = 1
        self.buys = 1
        self.phases = [Phase('action', self.player), Phase('buy', self.player),
                       Phase('cleanup', self.player)]

        # TODO: Implement phase logic
        #for phase in self.phases:
        #    outcome = self.take_phase(phase, self.player)

    def take_phase(self, phase):
        if phase.type == 'action':
            actions_taken = 0
            available_actions = self.actions
            while available_actions > 0:
                action_cards = [card for card in self.player.current_hand
                                if card.type == 'kingdom']
                if not action_cards:
                    break
                if action_cards:
                    actions_taken += 1
                    if len(action_cards) == 1:
                        self.player.play_card(action_cards[0], self)
                    else:
                        pass
            if actions_taken > 0:
                return True
            return False
        if phase.type == 'buy':
            while self.buys > 0:
                available_cards = self.board.display_cards()
                purchase = self.player.determine_purchase(available_cards)
                purchase_slot = [slot for slot in self.board.slots
                                 if slot.card == purchase][0]
                index = self.board.slots.index(purchase_slot)
                self.board.slots[index].num_cards -= 1
                self.player.buy_card(purchase)
                self.buys -= 1
            return True
        if phase.type == 'cleanup':
            pass


class Phase(object):
    def __init__(self, phase_type, player):
        self.player = player
        self.type = phase_type


class Player(object):
    def __init__(self, board):
        self.board = board
        self.deck = self.generate_starting_cards()
        self.current_hand = []
        self.discard = []
        self.victory_points = self.calculate_victory_points()
        self.is_starting = False

    def calculate_victory_points(self):
        return len(self.get_cards_of_type('victory'))

    def generate_starting_cards(self):
        cards = [TreasureCard('Copper') for x in range(7)] + \
                [VictoryCard('Estate') for x in range(3)]
        return cards

    def generate_hand(self):
        hand = []
        for i in range(5):
            random_int = random.randint(0, len(self.deck)-1)
            hand.append(self.deck.pop(random_int))
        self.current_hand = hand

    def discard_hand(self):
        for i in range(len(self.current_hand)):
            card = self.current_hand.pop(0)
            self.discard.append(card)

    def get_cards_of_type(self, card_type):
        return [card for card in self.deck if card.type == card_type] + \
               [card for card in self.current_hand if card.type == card_type] + \
               [card for card in self.discard if card.type == card_type]

    def play_card(self, card, turn):
        if card in self.current_hand:
            card.play(turn)
            if card.type == 'kingdom':
                turn.actions -= 1
            self.discard.append(self.current_hand.pop(
                self.current_hand.index(card)))
        else:
            raise Exception

    def buy_card(self, card):
        self.discard.append(card)

    def determine_purchase(self, options):
        coins = self.count_coins_in_hand()
        affordable_options = self.determine_affordable_options(options, coins)
        if len(affordable_options) == 1:
            return affordable_options[0]

    def count_coins_in_hand(self):
        count = 0
        for value in [x.value for x in self.current_hand]:
            try:
                count += value
            except TypeError:
                continue
        return count

    def determine_affordable_options(self, options, coins):
        affordable = []
        for option in options:
            if option.cost <= coins:
                affordable.append(option)
        return affordable

    def trash(self, card):
        card = self.current_hand.pop(self.current_hand.index(card))
        self.board.trash.append(card)


class Board(object):
    def __init__(self, num_players=2):
        self.num_players = num_players
        self.kingdom_slots = self.generate_and_check_kingdom_slots()
        self.treasure_slots = self.generate_treasure_slots()
        self.victory_slots = self.generate_victory_slots()
        self.slots = self.kingdom_slots + self.treasure_slots + self.victory_slots
        self.trash = []

    def generate_and_check_kingdom_slots(self):
        slots = []
        for x in range(10):
            new_slot_is_unique = False
            while not new_slot_is_unique:
                new_slot = Slot()
                new_slot_is_unique = self.check_slot_card_is_unique(
                    slots, new_slot)
            slots.append(new_slot)
        return slots

    def generate_treasure_slots(self):
        return [Slot(TreasureCard('Copper'), self.num_players),
                Slot(TreasureCard('Silver')),
                Slot(TreasureCard('Gold'))]

    def generate_victory_slots(self):
        return [Slot(VictoryCard('Estate')),
                Slot(VictoryCard('Duchy')),
                Slot(VictoryCard('Province'))]

    def check_slot_card_is_unique(self, current_slot_list, slot):
        for s in current_slot_list:
            if s.card.name == slot.card.name:
                return False
        return True

    def display_cards(self):
        return [slot.card for slot in self.slots]


class Slot(object):
    def __init__(self, card=None, num_players=2):
        self.num_players = num_players
        self.card = card if card is not None else self.generate_card()
        self.num_cards = self.generate_num_cards()

    def generate_card(self):
        card_name = self.generate_random_card_name()
        return KingdomCard(name=card_name)

    def generate_random_card_name(self):
        names = card_types['kingdom']
        random_int = random.randint(0, len(names)-1)
        return names[random_int].keys()[0]

    def generate_num_cards(self):
        if self.card.type == 'kingdom':
            return 10
        elif self.card.type == 'treasure':
            cards = {'Copper': 60, 'Silver': 40, 'Gold': 30}
            return self.calculate_treasure_card_number(cards)
        elif self.card.type == 'victory':
            return self.calculate_victory_card_number()

    def calculate_treasure_card_number(self, cards):
        for key in cards:
            if self.card.name == key:
                if key == 'Copper':
                    return cards[key] - (7 * self.num_players)
                else:
                    return cards[key]

    def calculate_victory_card_number(self):
        if self.num_players > 2:
            return 12
        else:
            return 8


class Card(object):
    def __init__(self, card_type, name=None, cost=None):
        card_types_list = ['kingdom', 'treasure', 'victory']
        self.name = name
        self.type = card_type if card_type in card_types_list else None
        self.value = self.set_card_attribute(name, card_type, 'value')
        self.cost = self.set_card_attribute(name, card_type, 'cost')
        self.victory_points = self.set_card_attribute(
            name, card_type, 'victory_points')
        self.actions = self.set_card_attribute(name, card_type, 'add_actions')
        self.cards = self.set_card_attribute(name, card_type, 'add_cards')
        self.buys = self.set_card_attribute(name, card_type, 'add_buys')

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

    def play(self, turn):
        actions = ['actions', 'buys', 'cards']
        for action in actions:
            if action == 'cards':
                self.add_cards_to_current_hand(turn)
            elif getattr(self, action) is not None:
                self.set_turn_attr(turn, action)

    def add_cards_to_current_hand(self, turn):
        try:
            value = getattr(self, 'cards')
            for i in range(value):
                card = turn.player.deck.pop(-1)
                turn.player.current_hand.append(card)
        except TypeError:
            pass

    def set_turn_attr(self, turn, action):
        value = getattr(turn, action)
        value += getattr(self, action)
        setattr(turn, action, value)


class KingdomCard(Card):
    def __init__(self, name=None):
        Card.__init__(self, card_type='kingdom', name=name)


class TreasureCard(Card):
    def __init__(self, name=None):
        Card.__init__(self, card_type='treasure', name=name)


class VictoryCard(Card):
    def __init__(self, name=None):
        Card.__init__(self, card_type='victory', name=name)
