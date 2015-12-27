import unittest

from dominion import Board, Card, Dominion, KingdomCard, Player, Slot


class DominionTest(unittest.TestCase):

    def test_game_sets_starting_player_on_run(self):
        game = Dominion()
        game.run()
        self.assertIsInstance(game.starting_player, Player)

    def test_game_has_specified_number_of_players(self):
        game = Dominion(players=4)
        self.assertEqual(4, len(game.players))

    def test_game_has_two_players_if_none_specified(self):
        game = Dominion()
        self.assertEqual(2, len(game.players))

    def test_game_players_type_is_player_object(self):
        game = Dominion()
        players = game.players
        for player in players:
            self.assertIsInstance(player, Player)

    def test_game_has_board(self):
        game = Dominion()
        self.assertIsInstance(game.board, Board)


class PlayerTest(unittest.TestCase):

    def test_player_starts_with_three_victory_points(self):
        player = Player()
        self.assertEqual(3, player.victory_points)

    def test_player_starts_with_ten_total_cards(self):
        player = Player()
        treasure_cards = len(player.cards['treasure_cards'])
        victory_cards = len(player.cards['victory_cards'])
        self.assertEqual(10, treasure_cards + victory_cards)

    def test_player_starts_with_seven_treasure_copper_cards(self):
        player = Player()
        self.assertEqual(7, len([x for x in player.cards['treasure_cards']
                                 if x.name == 'Copper']))

    def test_player_starts_with_three_victory_estate_cards(self):
        player = Player()
        self.assertEqual(3, len([x for x in player.cards['victory_cards']
                                 if x.name == 'Estate']))

    def test_player_starts_not_as_starting_player(self):
        player = Player()
        self.assertFalse(player.is_starting)


class BoardTest(unittest.TestCase):

    def test_board_has_ten_slots_for_card_sets(self):
        board = Board()
        self.assertEqual(10, len(board.slots))

    def test_cards_in_board_slots_are_unique_to_board(self):
        board = Board()
        card_names = [x.card.name for x in board.slots]
        card_names_set = set(card_names)
        self.assertEqual(len(card_names_set), len(card_names))


class SlotTest(unittest.TestCase):

    def test_board_slot_contains_card(self):
        slot = Slot()
        self.assertIsInstance(slot.card, Card)

    def test_board_slot_card_type_is_kingdom(self):
        slot = Slot()
        self.assertEqual('kingdom', slot.card.type)

    def test_board_slot_name_generation_returns_string(self):
        slot = Slot()
        string = 'example string'
        self.assertEqual(type(slot.card.name), type(string))


class KingdomCardTest(unittest.TestCase):

    def test_kingdom_card_type_is_kingdom(self):
        card = KingdomCard()
        self.assertEqual('kingdom', card.type)

    def test_kingdom_card_village_has_name_village(self):
        card = KingdomCard('Village')
        self.assertEqual('Village', card.name)

    def test_kingdom_card_village_has_cost(self):
        card = KingdomCard('Village')
        self.assertEqual(3, card.cost)

    def test_kingdom_card_village_has_no_value(self):
        card = KingdomCard('Village')
        self.assertIsNone(card.value)

    def test_kingdom_card_woodcutter_has_value(self):
        card = KingdomCard('Woodcutter')
        self.assertEqual(2, card.value)

if __name__ == '__main__':
    unittest.main()
