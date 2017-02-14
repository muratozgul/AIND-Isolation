import random
from operator import itemgetter
import math


def is_game_over(game, player):
    return game.is_loser(player) or game.is_winner(player)


def max_value(player, game, depth, maxDepth, calculate_score, update_reached_depth):
    printIndent = (depth+1)*' '
    # print(printIndent, '[max_value] depth:', depth)
    score = calculate_score(game, player)

    if is_game_over(game, player):
        # print(printIndent,'[max_value] game-over! score:', score)
        update_reached_depth(depth, 'game over')
        return score
    elif depth == maxDepth:
        # print(printIndent, '[max_value] max-depth! score:', score)
        update_reached_depth(depth, 'max depth')
        return score
    else:
        legalMoves = game.get_legal_moves()
        scores = []
        # print(printIndent, '[max_value] legal_moves', legalMoves)
        for candidateMove in legalMoves:
            # add a tuple of (move, score)
            candidateScore = min_value(player, game.forecast_move(candidateMove), depth+1, maxDepth, calculate_score, update_reached_depth)
            scores.append(candidateScore)

        # print(printIndent, '[max_value] score:', max(scores))
        return max(scores)


def min_value(player, game, depth, maxDepth, calculate_score, update_reached_depth):
    printIndent = (depth+1)*' '
    # print(printIndent, '[min_value] depth:', depth)
    score = calculate_score(game, player)

    if is_game_over(game, player):
        # print(printIndent, '[min_value] game-over! score:', score)
        update_reached_depth(depth, 'game over')
        return score
    elif depth == maxDepth:
        # print(printIndent, '[min_value] max-depth, score:', score)
        update_reached_depth(depth, 'max depth')
        return score
    else:
        legalMoves = game.get_legal_moves()
        # print(printIndent, '[min_value] legal_moves', legalMoves)
        scores = []
        for candidateMove in legalMoves:
            # add a tuple of (move, score)
            candidateScore = max_value(player, game.forecast_move(candidateMove), depth+1, maxDepth, calculate_score, update_reached_depth)
            scores.append(candidateScore)

        # print(printIndent, '[min_value] score:', min(scores))
        return min(scores)


def iterative_deepening_minimax(player, game, legal_moves, custom_score, update_move):
    selectedMove = (-1, -1)
    if not legal_moves:
        return selectedMove
    else:
        selectedMove = legal_moves[random.randint(0, len(legal_moves) - 1)]

    currentMaxDepth = 0
    reachedDepth = 0

    def update_reached_depth(d, msg):
        # print('Updating reached depth:', d, '(', msg, ')')
        nonlocal reachedDepth
        if (d > reachedDepth):
            reachedDepth = d

    while True:
        print('[iterative_deepening_minimax] depth:', currentMaxDepth)
        movesAndScores = []
        for candidateMove in legal_moves:
            # add a tuple of (move, score)
            # movesAndScores.append((candidateMove, minimax(game.forecast_move(candidateMove), currentMaxDepth, True)))
            movesAndScores.append((candidateMove, max_value(player, game.forecast_move(candidateMove), 0, currentMaxDepth, custom_score, update_reached_depth)))
        selectedMove = max(movesAndScores, key=itemgetter(1))[0]
        # save the best move found so far
        update_move(selectedMove)

        # print('utility: ', game.forecast_move(selectedMove).utility(player))
        # print('====VVVV===')
        # print(game.to_string())
        # print('b4 is game over:', is_game_over(game, player))
        # print(game.forecast_move(selectedMove).to_string())
        # print('after is game over:', is_game_over(game.forecast_move(selectedMove), player))
        # print('selectedMove:', selectedMove)
        # print('currentMaxDepth:', currentMaxDepth, ' , reachedDepth:', reachedDepth)
        # print('====^^^^===')

        if(is_game_over(game.forecast_move(selectedMove), player)):
            # game is over
            break;
        if(reachedDepth < currentMaxDepth):
            # the problem does not have more depth to explore at this point
            break;
        if(selectedMove[0] == -1 and selectedMove[1] == -1):
            # illegal move
            break;
        # update the max depth counter
        currentMaxDepth+=1
        reachedDepth = 0
