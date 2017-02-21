"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
from operator import itemgetter
from exceptions import Timeout


def should_update_score(bestScore, candidateScore, isMaximizing):
    if bestScore is None:
        return True
    elif isMaximizing and candidateScore > bestScore:
        return True
    elif not isMaximizing and candidateScore < bestScore:
        return True
    else:
        return False


def should_prune(score, alpha, beta, isMaximizing):
    return (isMaximizing is True and score >= beta) or (isMaximizing is False and score <= alpha)


def get_random_move(legalMoves):
    return legalMoves[random.randint(0, len(legalMoves) - 1)]


def heuristic1(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    blocking_moves = [move for move in own_moves if move in opp_moves]
    return float(len(blocking_moves)*100 + len(own_moves) - len(opp_moves))


def heuristic2(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    blocking_moves = [move for move in own_moves if move in opp_moves]
    return float(len(blocking_moves)*100 + len(own_moves) - 2*len(opp_moves))


def heuristic3(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    blocking_moves = [move for move in own_moves if move in opp_moves]
    return float(len(blocking_moves)*100 - 4*len(opp_moves))


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    return heuristic1(game, player)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        # print(game.to_string())
        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        selectedMove = (-1, -1)
        if not legal_moves:
            return selectedMove
        # in case of timeout
        selectedMove = get_random_move(legal_moves)

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if(self.method == 'minimax'):
                if self.iterative:
                    depth = 1
                    while True:
                        _, selectedMove = self.minimax(game, depth)
                        depth += 1
                else:
                    _, selectedMove = self.minimax(game, self.search_depth)

            elif(self.method == 'alphabeta'):
                if self.iterative:
                    depth = 1
                    while True:
                        _, selectedMove = self.alphabeta(game, depth)
                        depth += 1
                else:
                    _, selectedMove = self.alphabeta(game, self.search_depth)
            else:
                pass

        except Timeout:
            pass
            # Handle any actions required at timeout, if necessary
            # print('[get_move] Timeout')

        # Return the best move from the last completed search iteration
        # print('selectedMove', selectedMove)
        return selectedMove


    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        selfLocation = game.get_player_location(self)

        # A) depth = 0 is equals to evaluating current score and current location
        if(depth == 0):
            return self.score(game, self), selfLocation

        legalMoves = game.get_legal_moves()

        # B) this is game over situation
        if not legalMoves:
            if maximizing_player:
                # lose
                return float('-inf'), selfLocation
            else:
                # win
                return float('inf'), selfLocation

        # C) we can continue
        bestScore = None
        bestMove = None
        for candidateMove in legalMoves:
            candidateScore, _ = self.minimax(game.forecast_move(candidateMove), depth-1, not maximizing_player)
            if should_update_score(bestScore, candidateScore, maximizing_player):
                bestScore = candidateScore
                bestMove = candidateMove

        return bestScore, bestMove



    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        selfLocation = game.get_player_location(self)

        # A) depth = 0 is equals to evaluating current score and current location
        if(depth == 0):
            return self.score(game, self), selfLocation

        legalMoves = game.get_legal_moves()

        # B) this is game over situation
        if not legalMoves:
            if maximizing_player:
                # lose
                return float('-inf'), selfLocation
            else:
                # win
                return float('inf'), selfLocation

        # C) we can continue
        bestScore = None
        bestMove = None
        for candidateMove in legalMoves:
            candidateScore, _ = self.alphabeta(game.forecast_move(candidateMove), depth-1, alpha, beta, not maximizing_player)

            if should_update_score(bestScore, candidateScore, maximizing_player):
                bestScore = candidateScore
                bestMove = candidateMove

            if should_prune(bestScore, alpha, beta, maximizing_player):
                break

            if maximizing_player is True and candidateScore > alpha:
                alpha = candidateScore

            if maximizing_player is False and candidateScore < beta:
                beta = candidateScore

        return bestScore, bestMove
