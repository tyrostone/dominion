import copy
import unittest

from dominion import Board, Card, Dominion, Phase, Player, Slot, Turn
from dominion import KingdomCard, TreasureCard, VictoryCard


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

    def test_turn_starts_with_one_action(self):
        player = Player()
        turn = Turn(player)
        self.assertEqual(1, turn.actions)

    def test_turn_starts_with_one_buy(self):
        player = Player()
        turn = Turn(player)
        self.assertEqual(1, turn.buys)

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
        phase = Phase('action', player)
        self.assertFalse(first_turn.take_phase(phase))

    def test_action_phase_plays_action_card_if_one_available(self):
        player = Player()
        player.generate_hand()
        player.current_hand.append(KingdomCard('Village'))
        turn = Turn(player)
        phase = Phase('action', player)
        self.assertTrue(turn.take_phase(phase))

    def test_action_phase_passes_if_no_action_cards_available(self):
        player = Player()
        turn = Turn(player)
        phase = Phase('action', player)
        self.assertFalse(turn.take_phase(phase))


class PlayerTest(unittest.TestCase):

    def test_player_starts_with_three_victory_points(self):
        player = Player()
        self.assertEqual(3, player.victory_points)

    def test_player_starts_with_ten_total_cards_in_deck(self):
        player = Player()
        self.assertEqual(10, len(player.deck))

    def test_player_starts_with_seven_treasure_copper_cards(self):
        player = Player()
        self.assertEqual(7, len(player.get_cards_of_type('treasure')))

    def test_player_starts_with_three_victory_estate_cards(self):
        player = Player()
        self.assertEqual(3, len(player.get_cards_of_type('victory')))

    def test_player_starts_with_no_action_cards(self):
        player = Player()
        action_cards = player.get_cards_of_type('kingdom')
        self.assertEqual([], action_cards)

    def test_player_starts_not_as_starting_player(self):
        player = Player()
        self.assertFalse(player.is_starting)

    def test_player_returns_action_card_if_one_available(self):
        player = Player()
        player.deck.append(KingdomCard('Village'))
        self.assertIsInstance(
            player.get_cards_of_type('kingdom')[0], KingdomCard)

    def test_player_can_play_card_in_hand(self):
        player = Player()
        turn = Turn(player)
        player.current_hand.append(KingdomCard('Village'))
        player.play_card(player.current_hand[0], turn)

    def test_player_cannot_play_card_not_in_hand(self):
        player = Player()
        turn = Turn(player)
        player.generate_hand()
        deck_card = KingdomCard('Village')
        player.deck.append(deck_card)
        self.assertRaises(Exception, player.play_card, deck_card, turn)

    def test_player_generates_hand_of_five_cards(self):
        player = Player()
        player.generate_hand()
        self.assertEqual(5, len(player.current_hand))

    def test_player_cards_in_hand_not_in_deck(self):
        player = Player()
        player.generate_hand()
        for card in player.current_hand:
            self.assertNotIn(card, player.deck)

    def test_player_discard_starts_empty(self):
        player = Player()
        self.assertEqual([], player.discard)

    def test_player_discard_hand_empties_hand(self):
        player = Player()
        player.generate_hand()
        player.discard_hand()
        self.assertEqual([], player.current_hand)

    def test_player_discard_hand_goes_to_discard(self):
        player = Player()
        player.generate_hand()
        hand = copy.copy(player.current_hand)
        player.discard_hand()
        self.assertEqual(hand, player.discard)

    def test_player_discards_card_after_playing_it(self):
        player = Player()
        turn = Turn(player)
        player.generate_hand()
        card_to_play = player.current_hand[0]
        player.play_card(player.current_hand[0], turn)
        self.assertIn(card_to_play, player.discard)


class BoardTest(unittest.TestCase):

    def test_board_defaults_to_two_players(self):
        board = Board()
        self.assertEqual(2, board.num_players)

    def test_board_has_ten_slots_for_kingdom_cards(self):
        board = Board()
        self.assertEqual(10, len(board.kingdom_slots))

    def test_board_has_three_treasure_card_slots(self):
        board = Board()
        self.assertEqual(3, len(board.treasure_slots))

    def test_board_has_three_victory_card_slots(self):
        board = Board()
        self.assertEqual(3, len(board.victory_slots))

    def test_kingdom_cards_in_board_slots_are_unique_to_board(self):
        board = Board()
        card_names = [x.card.name for x in board.kingdom_slots]
        card_names_set = set(card_names)
        self.assertEqual(len(card_names_set), len(card_names))

    def test_board_has_trash_pile(self):
        board = Board()
        self.assertEqual([], board.trash)


class SlotTest(unittest.TestCase):

    def test_board_slot_contains_card(self):
        slot = Slot()
        self.assertIsInstance(slot.card, Card)

    def test_board_slot_default_card_type_is_kingdom(self):
        slot = Slot()
        self.assertEqual('kingdom', slot.card.type)

    def test_board_treasure_slot_copper_has_card_type_treasure(self):
        slot = Slot(TreasureCard('Copper'))
        self.assertEqual('treasure', slot.card.type)

    def test_board_victory_slot_estate_has_card_type_treasure(self):
        slot = Slot(VictoryCard('Estate'))
        self.assertEqual('victory', slot.card.type)

    def test_board_slot_has_ten_cards_of_card_type_kingdom(self):
        slot = Slot()
        self.assertEqual(10, slot.num_cards)

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
        player = Player()
        turn = Turn(player)
        card = KingdomCard('Village')
        card.play(turn)
        self.assertEqual(3, turn.actions)

    def test_playing_kingdom_card_woodcutter_adds_no_actions_to_turn(self):
        player = Player()
        turn = Turn(player)
        card = KingdomCard('Woodcutter')
        card.play(turn)
        self.assertEqual(1, turn.actions)

    def test_playing_kingdom_card_village_adds_card_to_hand(self):
        player = Player()
        turn = Turn(player)
        card = KingdomCard('Village')
        card.play(turn)
        self.assertEqual(1, len(turn.player.current_hand))

    def test_playing_kingdom_card_smithy_adds_three_cards_to_hand(self):
        player = Player()
        turn = Turn(player)
        card = KingdomCard('Smithy')
        card.play(turn)
        self.assertEqual(3, len(turn.player.current_hand))

    def test_playing_kingdom_card_woodcutter_adds_no_cards_to_hand(self):
        player = Player()
        turn = Turn(player)
        card = KingdomCard('Woodcutter')
        card.play(turn)
        self.assertEqual(0, len(turn.player.current_hand))

if __name__ == '__main__':
    unittest.main()
