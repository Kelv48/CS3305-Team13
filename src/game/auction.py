from src.game.player import Player
from src.game.button import buttons
from src.game.bot import AI
from src.game.utils import playerDecision, arrangeRoom, drawPlayer
from src.gui.constants import BB




def auction(common_cards=None):
    """
    the function displays each player available option about auction,
    after selecting the option, it changes the player attributes
    the function ends when each player enters the game or resign
    :param common_cards: list of common cards, if stage game is preflop then common cards is None
    """

    player_list = Player.player_list

    # makes a list of players who are alive this round
    player_list = [player for player in player_list if player.live]

    number_decisions = sum([player.decision for player in player_list])
    number_player = len(player_list)

    # auction end when each player make a decision or all players except one fold
    every_fold = False
    while number_decisions != number_player and not every_fold:

        # list how much bet each player in this round of auction
        # bet_list = [0 for i in range(len(player_list))]
        for player in player_list:

            if not player.decision and player.live:
                input_stack_list = [player.input_stack for player in player_list]
                bet_list = [player.bet_auction for player in player_list]

                # Create a set of options for the player
                dict_options = {'fold': True, 'all-in': True, 'call': False, 'check': False, 'raise': False}

                raise_list = sorted(input_stack_list, reverse=True)
                bet_list = sorted(bet_list, reverse=True)

                # calculate call value, min and max value raise
                call_value = max(input_stack_list) - player.input_stack
                min_raise = call_value + bet_list[0] - bet_list[1]
                if min_raise < BB:
                    min_raise = BB
                max_raise = player.stack

                # activate available option for player
                if player.input_stack == max(input_stack_list):
                    dict_options['check'] = True
                elif player.stack > max(input_stack_list) - player.input_stack:
                    dict_options['call'] = True
                if player.stack > min_raise:
                    dict_options['raise'] = True

                pot = sum(raise_list) # everything that's on the tablee
                pot_table = sum(input_stack_list) - sum(bet_list)

                # ask player for decision

                if player.kind == 'human':
                    decision = playerDecision(buttons, dict_options, min_raise, max_raise, common_cards)


                elif player.kind == 'AI':
                    n_fold = 0
                    for gamer in player_list:
                        if gamer.live == 0 and gamer.alin == 0:
                            n_fold += 1
                    n_player_in_round = number_player - n_fold

                    bot = AI(player.cards, dict_options, call_value, min_raise, max_raise, pot, n_player_in_round,
                             common_cards)
                    decision = bot.decision()
                    print(player.name, decision)

                # Processing of player decision

                # decision always has 2 elements
                if decision[0] == 'raise':
                    chips = int(decision[1])
                decision = decision[0]

                if decision == 'call':
                    chips = max(input_stack_list) - player.input_stack
                    if player.stack > chips:
                        player.drop(chips)
                    else:
                        player.drop(player.stack)
                        player.allin()

                elif decision == 'fold':
                    player.fold()

                elif decision == 'check':
                    player.decision = True

                elif decision == 'all-in':
                    player.drop(player.stack)
                    for gamer in player_list:
                        # if any of player bets all-in, then each player who not bet all-in and has bet less than
                        # that player all-in, will have to make the decision again
                        if gamer.live and gamer.decision and gamer.input_stack < player.input_stack:
                            gamer.decision = False
                    player.allin()

                elif decision == 'raise':

                    for gamer in player_list:
                        if gamer.live and gamer.decision:
                            gamer.decision = False
                    if player.stack > chips:
                        player.drop(chips)
                    else:
                        player.drop(player.stack)
                        player.allin()

                # Update player label at gui
                arrangeRoom(common_cards)
                drawPlayer()


            # check if the every except one player fold then don't ask him about decision
            sum_live = 0
            sum_alin = 0
            for gamer in player_list:
                sum_live += gamer.live
                sum_alin += gamer.alin
            if sum_live == 1 and sum_alin == 0:
                every_fold = True
                break

        number_decisions = sum([player.decision for player in player_list])

    # After auction players who fold or all-in have no decision made until the next round
    for player in player_list:
        player.nextAuction()
        if player.live:
            player.decision = False
