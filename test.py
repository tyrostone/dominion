import unittest

from dominion import Board, Card, Dominion, KingdomCard, Phase, Player, Slot, Turn


class DominionTest(unittest.TestCase):

    def test_game_sets_starting_player(self):
        game = Dominion()
        game.run()
        self.assertIsInstance(game.starting_player, Player)

    def test_game_has_specified_number_of_players(self):
        game = Dominion(4)
        game.run()
        self.assertEqual(4, len(game.players))

    def test_game_has_two_players_if_none_specified(self):
        game = Dominion()
        game.run()
        self.assertEqual(2, len(game.players))

    def test_game_players_type_is_player_object(self):
        game = Dominion()
        game.run()
        players = game.players
        for player in players:
            self.assertIsInstance(player, Player)

    def test_game_has_board(self):
        game = Dominion()
        game.run()
        self.assertIsInstance(game.board, Board)

    def test_game_generates_turn_when_run(self):
        game = Dominion()
        turn = game.run()
        self.assertIsInstance(turn, Turn)


class TurnTest(unittest.TestCase):

    def test_turn_has_three_phases(self):
        player = Player()
        turn = Turn(player)
        self.assertEqual(3, len(turn.phases))

    def test_turn_first_phase_is_action(self):
        player = Player()
        turn = Turn(player)
        self.assertEqual('action', turn.phases[0].type)

    def test_first_action_phase_has_no_effect(self):
        player = Player()
        first_turn = Turn(player)
        self.assertFalse(first_turn.take_phase('action', player))

    def test_action_phase_plays_action_card_if_one_available(self):
        player = Player()
        player.cards['kingdom_cards'] = [KingdomCard('Village')]
        turn = Turn(player)
        # self.assert


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

    def test_player_starts_with_no_action_cards(self):
        player = Player()
        action_cards = player.get_action_cards()
        self.assertIsNone(action_cards)

    def test_player_returns_action_card_if_one_available(self):
        player = Player()
        player.cards['kingdom_cards'] = [KingdomCard('Village')]
        self.assertIsInstance(player.get_action_cards()[0], KingdomCard)

    def test_player_can_play_card(self):
        player = Player()
        player.cards['kingdom_cards'] = [KingdomCard('Village')]
        player.play_card(player.get_action_cards()[0])

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
