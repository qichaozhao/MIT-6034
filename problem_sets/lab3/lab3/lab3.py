# 6.034 Fall 2010 Lab 3: Games
# Name: Qichao Zhao
# Email: qczhao@gmail.com

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from basicplayer import *
from connectfour import *
from util import *


## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
# run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
# run_game(basic_player, human_player)

## Or watch the computer play against itself:
# run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """

    if board.longest_chain(board.get_current_player_id()) >= 4:
        score = 2000 - board.num_tokens_on_board()

    elif board.longest_chain(board.get_other_player_id()) >= 4:
        score = -2000 + board.num_tokens_on_board()

    else:
        # prefer center?
        score = board.longest_chain(board.get_current_player_id()) * 10
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3 - col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3 - col)

    return score


## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)


## You can try out your new evaluation function by uncommenting this line:
# run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.
def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):
    best_val = None
    alpha = NEG_INFINITY
    beta = INFINITY

    for move, new_board in get_next_moves_fn(board):

        # print "Checking move: " + str(move)
        val = max(alpha, alpha_beta_board_search('min', new_board, depth - 1, eval_fn, alpha, beta, get_next_moves_fn, is_terminal_fn))

        alpha = max(val, alpha)

        # print "Val: " + str(val)
        # print "Alpha: " + str(alpha)

        if best_val == None or val > best_val[0]:
            best_val = (val, move, new_board)

        if alpha >= beta:
            # if we can prune this branch
            break

    # if verbose:
    print "AlphaBeta: AlphaBeta Decided on column %s with rating %s" % (best_val[1], best_val[0])

    return best_val[1]


# @count_runs
def alpha_beta_board_search(node, board, depth, eval_fn, alpha, beta,
                            get_next_moves_fn=get_all_next_moves,
                            is_terminal_fn=is_terminal):
    """
    Alphabeta helper function: Return the minimax value of a particular board,
    given a particular depth to estimate to
    """

    a = alpha
    b = beta

    val = None

    if is_terminal_fn(depth, board):
        # at a leaf node
        # print board
        if node == 'max':
            val = eval_fn(board)
            return val
        else:
            val = -eval_fn(board)
            return val
            # return eval_fn(board)

    for move, new_board in get_next_moves_fn(board):

        if node == 'max':
            # this is the maximising play
            #     print "Checking: " + str(move)

            val = max(a, alpha_beta_board_search('min', new_board, depth - 1, eval_fn, a, b, get_next_moves_fn, is_terminal_fn))
            a = max(val, a)

            # print "Val: " + str(val)
            # print "Alpha: " + str(a)

            if a >= b:
                # if we can prune this branch
                break

        else:
            # this is the minimising play
            #     print "Checking: " + str(move)
            val = min(b, alpha_beta_board_search('max', new_board, depth - 1, eval_fn, a, b, get_next_moves_fn, is_terminal_fn))

            b = min(val, b)

            # print "Val: " + str(val)
            # print "Beta: " + str(b)

            if a >= b:
                # if we can prune this branch
                break

    return val


def alpha_beta_negamax(board, depth,
                       eval_fn,
                       # NOTE: You should use get_next_moves_fn when generating
                       # next board configurations, and is_terminal_fn when
                       # checking game termination.
                       # The default functions set here will work
                       # for connect_four.
                       get_next_moves_fn=get_all_next_moves,
                       is_terminal_fn=is_terminal,
                       ):
    """
    This is a negamax implementation of the alpha beta function
    :param board:
    :param depth:
    :param eval_fn:
    :param get_next_moves_fn:
    :param is_terminal_fn:
    :return:
    """

    alpha = NEG_INFINITY
    beta = INFINITY
    best_val = None

    for move, new_board in get_next_moves_fn(board):

        # print "Checking move: " + str(move)
        val = max(alpha, -1 * alpha_beta_negamax_board_search(-1, new_board, depth - 1, eval_fn, -beta, -alpha, get_next_moves_fn, is_terminal_fn))

        # print "Val: " + str(val)
        # print "Alpha: " + str(alpha)

        if best_val == None or val > best_val[0]:
            best_val = (val, move, new_board)

    # if verbose:
    print "AlphaBeta Negamax: AlphaBeta Decided on column %s with rating %s" % (best_val[1], best_val[0])

    return best_val[1]


def alpha_beta_negamax_board_search(node, board, depth, eval_fn, alpha, beta,
                                    get_next_moves_fn=get_all_next_moves,
                                    is_terminal_fn=is_terminal):
    """
    The helper function for the main negamax parameter
    :param node:
    :param board:
    :param depth:
    :param eval_fn:
    :param alpha:
    :param beta:
    :param get_next_moves_fn:
    :param is_terminal_fn:
    :return:
    """
    if is_terminal_fn(depth, board):
        if node == -1:
            return -eval_fn(board)
        else:
            return eval_fn(board)

    a = alpha
    b = beta

    for move, new_board in get_next_moves_fn(board):

        val = max(a, -1 * alpha_beta_negamax_board_search(-1 * node, new_board, depth - 1, eval_fn, -b, -a, get_next_moves_fn, is_terminal_fn))
        a = max(val, a)

        # print "move: " + move
        # print "value: " + str(a)

    return a

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)


# run_game(human_player, ab_iterative_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

def better_evaluate(board):
    """
    this evaluation function not only prefers the centre but also prioritises making chains
    :param board:
    :return:
    """
    score = 0
    if board.longest_chain(board.get_current_player_id()) >= 4:
        score = 100000 - board.num_tokens_on_board()

    elif board.longest_chain(board.get_other_player_id()) >= 4:
        score = -100000 + board.num_tokens_on_board()

    else:
        # maximise the length of existing chains and stop 3 chains from opposition
        my_chains = filter(lambda x: len(x) > 1, board.chain_cells(board.get_current_player_id()))
        opp_chains = filter(lambda x: len(x) > 1, board.chain_cells(board.get_other_player_id()))
        round = board.num_tokens_on_board()

        for c in my_chains:
            score += (len(c) ** len(c)) * (2 * round)

        for d in opp_chains:
            score -= (len(d) ** len(d)) * (43 - round)

        for row in range(6):
            for col in range(7):
                # we want to favour lower positions if all else is equal
                # and we want to favour inner positions rather than outer
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3 - col)
                    score += 6 / (row + 1) * (43 - round) / float(43)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3 - col)
                    score -= 6 / (row + 1) * (43 - round) / float(43)

    return score


def does_extend_chain(row, col, chain):
    """
    loops through the set of chains and checks if a given row/cell extends it or not
    :return:
    """
    out = []
    for c in chain:
        # we need to check if the row/col is adjacent to a position, and then if it is, if its along the same vector
        vector_c = [c[0][0] - c[1][0], c[0][1] - c[1][1]]
        for pos in c:
            if pos[0] - row == 1 and pos[1] - col == 1:
                # is adjacent, now check the vector
                if (row + vector_c[0] == pos[0] and col + vector_c[1] == pos[1]) or (-(row + vector_c[0]) == pos[0] and -(col + vector_c[1] == pos[1])):
                    out.append(len(c) ** len(c))

    return out


def betterer_evaluate(board):
    """
    this evaluator prioritises maximising the number of chain making options and the number of chains
    :param board:
    :return:
    """
    score = 0
    if board.longest_chain(board.get_current_player_id()) >= 4:
        score = 100000 - board.num_tokens_on_board()

    elif board.longest_chain(board.get_other_player_id()) >= 4:
        score = -100000 + board.num_tokens_on_board()

    else:
        # maximise the length of existing chains
        my_chains = filter(lambda x: len(x) > 1, board.chain_cells(board.get_current_player_id()))
        opp_chains = filter(lambda x: len(x) > 1, board.chain_cells(board.get_other_player_id()))

        for c in my_chains:
            score += ((len(c) ** len(c)) * 10)

        for d in opp_chains:
            score -= (len(d) ** len(d)) * 5

        for col in range(7):
            row = board.get_height_of_column(col) - 1
            if row >= 0:
                ret = does_extend_chain(row, col, my_chains)
                score += (sum(ret) + board.num_tokens_on_board()) * 15

            score -= abs(3 - col) * 5  # add slight preference for middle of board.

    return score / 10


# Comment this line after you've fully implemented better_evaluate
# better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)
# betterer_evaluate = memoize(betterer_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = ((0, 0, 0, 0, 0, 0, 0),
                    (0, 0, 0, 0, 0, 0, 0),
                    (0, 0, 0, 0, 0, 0, 0),
                    (0, 2, 2, 1, 1, 2, 0),
                    (0, 2, 1, 2, 1, 2, 0),
                    (2, 1, 2, 1, 1, 1, 0),
                    )
    test_board_1 = ConnectFourBoard(board_array=board_tuples,
                                    current_player=1)
    test_board_2 = ConnectFourBoard(board_array=board_tuples,
                                    current_player=2)
    # better evaluate from player 1
    print "%s => %s" % (test_board_1, betterer_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" % (test_board_2, betterer_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=30)

your_negamax_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_negamax,
                                                eval_fn=better_evaluate,
                                                timeout=10)

# your_player_v2 = lambda board: run_search_function(board,
#                                                    search_fn=alpha_beta_search,
#                                                    eval_fn=betterer_evaluate,
#                                                    timeout=5)


# your_player = lambda board: alpha_beta_search(board, depth=8,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
# run_game(your_player, human_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
run_game(progressive_deepening_player, your_player)


## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])


def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])


## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)


## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (True)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "6"
WHAT_I_FOUND_INTERESTING = "ALL"
WHAT_I_FOUND_BORING = "NONE"
NAME = "Qichao Zhao"
EMAIL = "qczhao@gmail.com"
