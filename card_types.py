""" A JSON-like structure with Dominion card data
    Structure is a dictionary containing 3 keys:
        kingdom, treasure, and victory
    The value of each key is a list of dictionaries
    Each card is represented as a dictionary object
"""
card_types = \
    {'kingdom':
     [{'Cellar': {'cost': 2, 'add_actions': 1,
                  'action': '+1 card for each discarded card'}},
      {'Chapel': {'cost': 2, 'action': 'trash cards', 'action_limit': 4}},
      {'Moat':   {'cost': 2, 'add_cards': 2,
                  'action': 'protect against other player attack card'}},
      {'Chancellor':   {'cost': 3, 'value': 2,
                        'action': 'deck into discard'}},
      {'Village':      {'cost': 3, 'add_actions': 2, 'add_cards': 1}},
      {'Woodcutter':   {'cost': 3, 'value': 2, 'add_buys': 1}},
      {'Workshop':     {'cost': 3, 'gain_card': True, 'gain_card_limit': 4}},
      {'Feast':        {'cost': 4, 'gain_card': True, 'gain_card_limit': 5,
                        'trash': True}},
      {'Militia':      {'cost': 4, 'value': 2,
                        'action': 'other players discard to 3 cards'}},
      {'Moneylender':  {'cost': 4, 'action': 'trash copper, value +=3'}},
      {'Remodel':      {'cost': 4,
                        'action': 'trash any card in hand, gain card=card.cost+2'}},
      {'Bureaucrat':   {'cost': 4,
                        'action': 'add silver to top of deck, other players victory card to top of deck'}},
      {'Smithy':       {'cost': 4, 'add_cards': 3}},
      {'Spy':          {'cost': 4, 'add_cards': 1, 'add_actions': 1,
                        'action': 'reveal top card, either discard or put back on top'}},
      {'Thief':        {'cost': 4, 'action': 'complex card'}},
      {'Throne Room':  {'cost': 4, 'action': 'play any action card twice'}},
      {'Council Room': {'cost': 5, 'add_cards': 2, 'add_buys': 1}},
      {'Festival':     {'cost': 5, 'add_actions': 2, 'add_buys': 1,
                        'value': 2}},
      {'Laboratory':   {'cost': 5, 'add_cards': 2, 'add_actions': 1}},
      {'Library':      {'cost': 5, 'action': 'complex card'}},
      {'Market':       {'cost': 5, 'add_cards': 1, 'add_actions': 1,
                        'add_buys': 1, 'value': 1}},
      {'Mine':         {'cost': 5,
                        'action': 'trash treasure card, add treasure card = trashed card+3'}},
      {'Witch':        {'cost': 5, 'add_cards': 2,
                        'action': 'other players gain curse card'}},
      {'Adventurer':   {'cost': 6, 'action': 'add 2 treasure cards to hand'}},
      ],
     'treasure':
     [{'Copper': {'cost': 0, 'value': 1}},
      {'Silver': {'cost': 3, 'value': 2}},
      {'Gold':   {'cost': 6, 'value': 3}}],
     'victory':
     [{'Estate':   {'cost': 2, 'victory_points': 1}},
      {'Duchy':    {'cost': 5, 'victory_points': 3}},
      {'Province': {'cost': 8, 'victory_points': 6}}]
     }
