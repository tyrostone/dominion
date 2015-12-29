import copy
import unittest

from dominion import Board, Card, Dominion, Phase, Player, Slot, Turn
from dominion import KingdomCard, TreasureCard, VictoryCard


class DominionTest(unittest.TestCase):

    def setUp(self):
        self.game = Dominion()
        self.game.run()

    def tearDown(self):
        pass

    def test_game_sets_starting_player(self):
        self.assertIsInstance(self.game.starting_player, Player)

    def test_game_has_two_players_if_none_specified(self):
        self.assertEqual(2, len(self.game.players))

    def test_game_has_specified_number_of_players(self):
        game = Dominion(4)
        self.assertEqual(4, len(game.players))

    def test_game_cannot_have_more_than_four_players(self):
        game = Dominion(20)
        self.assertEqual(4, len(game.players))

    def test_game_players_type_is_player_object(self):
        for player in self.game.players:
            self.assertIsInstance(player, Player)

    def test_game_has_board(self):
        self.assertIsInstance(self.game.board, Board)

    def test_game_generates_turn_when_run(self):
        turn = self.game.run()
        self.assertIsInstance(turn, Turn)


class TurnTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.player = Player(self.board)
        self.turn = Turn(self.player, self.board)

    def tearDown(self):
        pass

    def test_turn_starts_with_one_action(self):
        self.assertEqual(1, self.turn.actions)

    def test_turn_starts_with_one_buy(self):
        self.assertEqual(1, self.turn.buys)

    def test_turn_has_three_phases(self):
        self.assertEqual(3, len(self.turn.phases))

    def test_turn_first_phase_is_action(self):
        self.assertEqual('action', self.turn.phases[0].type)

    def test_turn_second_phase_is_buy(self):
        self.assertEqual('buy', self.turn.phases[1].type)

    def test_turn_third_phase_is_cleanup(self):
        self.assertEqual('cleanup', self.turn.phases[-1].type)

    def test_action_phase_plays_action_card_if_one_available(self):
        board = Board()
        player = Player(board)
        self.player.generate_hand()
        player.current_hand.append(KingdomCard('Village'))
        turn = Turn(player, board)
        phase = Phase('action', player)
        self.assertTrue(turn.take_phase(phase))

    def test_action_phase_passes_if_no_action_cards_available(self):
        phase = Phase('action', self.player)
        self.assertFalse(self.turn.take_phase(phase))

    def test_buy_phase_adds_card_to_player_discard(self):
        phase = Phase('buy', self.player)
        self.turn.take_phase(phase)
        self.assertEqual(1, len(self.player.discard))

    def test_buy_phase_removes_card_from_board(self):
        phase = Phase('buy', self.player)
        self.turn.take_phase(phase)
        self.assertEqual(9, self.board.slots[0].num_cards)


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.player = Player(self.board)

    def test_player_starts_with_three_victory_points(self):
        self.assertEqual(3, self.player.victory_points)

    def test_player_starts_with_ten_total_cards_in_deck(self):
        self.assertEqual(10, len(self.player.deck))

    def test_player_starts_with_seven_treasure_copper_cards(self):
        self.assertEqual(7, len(self.player.get_cards_of_type('treasure')))

    def test_player_starts_with_three_victory_estate_cards(self):
        self.assertEqual(3, len(self.player.get_cards_of_type('victory')))

    def test_player_starts_with_no_action_cards(self):
        action_cards = self.player.get_cards_of_type('kingdom')
        self.assertEqual([], action_cards)

    def test_player_starts_not_as_starting_player(self):
        self.assertFalse(self.player.is_starting)

    def test_player_returns_action_card_if_one_available(self):
        self.player.deck.append(KingdomCard('Village'))
        self.assertIsInstance(
            self.player.get_cards_of_type('kingdom')[0], KingdomCard)

    def test_player_can_play_card_in_hand(self):
        turn = Turn(self.player, self.board)
        self.player.current_hand.append(KingdomCard('Village'))
        self.player.play_card(self.player.current_hand[0], turn)

    def test_player_cannot_play_card_not_in_hand(self):
        turn = Turn(self.player, self.board)
        self.player.generate_hand()
        deck_card = KingdomCard('Village')
        self.player.deck.append(deck_card)
        self.assertRaises(Exception, self.player.play_card, deck_card, turn)

    def test_player_generates_hand_of_five_cards(self):
        self.player.generate_hand()
        self.assertEqual(5, len(self.player.current_hand))

    def test_player_cards_in_hand_not_in_deck(self):
        self.player.generate_hand()
        for card in self.player.current_hand:
            self.assertNotIn(card, self.player.deck)

    def test_player_discard_starts_empty(self):
        self.assertEqual([], self.player.discard)

    def test_player_discard_hand_empties_hand(self):
        self.player.generate_hand()
        self.player.discard_hand()
        self.assertEqual([], self.player.current_hand)

    def test_player_discard_hand_goes_to_discard(self):
        self.player.generate_hand()
        hand = copy.copy(self.player.current_hand)
        self.player.discard_hand()
        self.assertEqual(hand, self.player.discard)

    def test_player_discards_card_after_playing_it(self):
        turn = Turn(self.player, self.board)
        self.player.generate_hand()
        card_to_play = self.player.current_hand[0]
        self.player.play_card(self.player.current_hand[0], turn)
        self.assertIn(card_to_play, self.player.discard)

    def test_player_can_buy_copper_treasure_card(self):
        card = TreasureCard('Copper')
        self.player.buy_card(card)
        self.assertIn(card, self.player.discard)

    def test_player_can_discard_copper_treasure_card(self):
        self.player.generate_hand()
        copper = [card for card in self.player.current_hand
                  if card.name == 'Copper'][0]
        self.player.trash(copper)
        self.assertIn(copper, self.player.board.trash)


class BoardTest(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_board_defaults_to_two_players(self):
        self.assertEqual(2, self.board.num_players)

    def test_board_has_ten_slots_for_kingdom_cards(self):
        self.assertEqual(10, len(self.board.kingdom_slots))

    def test_board_has_three_treasure_card_slots(self):
        self.assertEqual(3, len(self.board.treasure_slots))

    def test_board_has_three_victory_card_slots(self):
        self.assertEqual(3, len(self.board.victory_slots))

    def test_kingdom_cards_in_board_slots_are_unique_to_board(self):
        card_names = [x.card.name for x in self.board.kingdom_slots]
        card_names_set = set(card_names)
        self.assertEqual(len(card_names_set), len(card_names))

    def test_board_has_trash_pile(self):
        self.assertEqual([], self.board.trash)

    def test_board_displays_available_cards(self):
        all_cards = self.board.display_cards()
        for card in all_cards:
            self.assertIsInstance(card, Card)


class SlotTest(unittest.TestCase):

    def setUp(self):
        self.slot = Slot()

    def test_board_slot_contains_card(self):
        self.assertIsInstance(self.slot.card, Card)

    def test_board_slot_default_card_type_is_kingdom(self):
        self.assertEqual('kingdom', self.slot.card.type)

    def test_board_treasure_slot_copper_has_card_type_treasure(self):
        slot = Slot(TreasureCard('Copper'))
        self.assertEqual('treasure', slot.card.type)

    def test_board_victory_slot_estate_has_card_type_treasure(self):
        slot = Slot(VictoryCard('Estate'))
        self.assertEqual('victory', slot.card.type)

    def test_board_slot_has_ten_cards_of_card_type_kingdom(self):
        self.assertEqual(10, self.slot.num_cards)

    def test_board_slot_has_forty_six_copper_cards_by_default(self):
        slot = Slot(TreasureCard('Copper'))
        self.assertEqual(46, slot.num_cards)

    def test_board_slot_has_thirty_nine_copper_cards_if_three_players(self):
        slot = Slot(TreasureCard('Copper'), 3)
        self.assertEqual(39, slot.num_cards)

    def test_board_slot_has_forty_silver_cards(self):
        slot = Slot(TreasureCard('Silver'))
        self.assertEqual(40, slot.num_cards)

    def test_board_slot_has_thirty_gold_cards(self):
        slot = Slot(TreasureCard('Gold'))
        self.assertEqual(30, slot.num_cards)

    def test_board_slot_has_eight_victory_cards_by_default(self):
        slot = Slot(VictoryCard('Estate'))
        self.assertEqual(8, slot.num_cards)

    def test_board_slot_has_twelve_victory_cards_if_three_players(self):
        slot = Slot(VictoryCard('Estate'), 3)
        self.assertEqual(12, slot.num_cards)


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

    def test_kingdom_card_village_has_two_actions(self):
        card = KingdomCard('Village')
        self.assertEqual(2, card.actions)

    def test_kingom_card_village_has_actions_attribute(self):
        card = KingdomCard('Village')
        self.assertEqual(2, card.actions)

    def test_kingom_card_woodcutter_has_no_actions_attribute(self):
        card = KingdomCard('Woodcutter')
        self.assertIsNone(card.actions)

    def test_kingdom_card_woodcutter_has_buys_attribute(self):
        card = KingdomCard('Woodcutter')
        self.assertEqual(1, card.buys)

    def test_kingom_card_village_has_no_buys_attribute(self):
        card = KingdomCard('Village')
        self.assertIsNone(card.buys)

    def test_playing_kingdom_card_village_adds_two_actions_to_turn(self):
        board = Board()
        player = Player(board)
        turn = Turn(player, board)
        card = KingdomCard('Village')
        card.play(turn)
        self.assertEqual(3, turn.actions)

    def test_playing_kingdom_card_woodcutter_adds_no_actions_to_turn(self):
        board = Board()
        player = Player(board)
        turn = Turn(player, board)
        card = KingdomCard('Woodcutter')
        card.play(turn)
        self.assertEqual(1, turn.actions)

    def test_playing_kingdom_card_village_adds_card_to_hand(self):
        board = Board()
        player = Player(board)
        turn = Turn(player, board)
        card = KingdomCard('Village')
        card.play(turn)
        self.assertEqual(1, len(turn.player.current_hand))

    def test_playing_kingdom_card_smithy_adds_three_cards_to_hand(self):
        board = Board()
        player = Player(board)
        turn = Turn(player, board)
        card = KingdomCard('Smithy')
        card.play(turn)
        self.assertEqual(3, len(turn.player.current_hand))

    def test_playing_kingdom_card_woodcutter_adds_no_cards_to_hand(self):
        board = Board()
        player = Player(board)
        turn = Turn(player, board)
        card = KingdomCard('Woodcutter')
        card.play(turn)
        self.assertEqual(0, len(turn.player.current_hand))

if __name__ == '__main__':
    unittest.main()
