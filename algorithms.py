import random
from operator import itemgetter

def is_game_over(game, player):
    return game.is_loser(player) or game.is_winner(player)


def max_value(player, game, depth, maxDepth, calculate_score):
    printIndent = (depth+1)*' '
    print(printIndent, '[max_value] depth:', depth)
    score = calculate_score(game, player)

    if is_game_over(game, player):
        print(printIndent,'[max_value] game-over! score:', score)
        return score
    elif depth == maxDepth:
        print(printIndent, '[max_value] max-depth! score:', score)
        return score
    else:
        legalMoves = game.get_legal_moves()
        # scores = []
        movesAndScores = []
        print(printIndent, '[max_value] legal_moves', legalMoves)
        for candidateMove in legalMoves:
            # add a tuple of (move, score)
            candidateScore = min_value(player, game.forecast_move(candidateMove), depth+1, maxDepth, calculate_score)
            # scores.append(candidateScore)
            movesAndScores.append((candidateMove, candidateScore))

        pair = max(movesAndScores, key=itemgetter(1))
        print(printIndent, '[max_value] (move, score):', pair)
        return pair[1]


def min_value(player, game, depth, maxDepth, calculate_score):
    printIndent = (depth+1)*' '
    print(printIndent, '[min_value] depth:', depth)
    score = calculate_score(game, player)

    if is_game_over(game, player):
        print(printIndent, '[min_value] game-over! score:', score)
        return score
    elif depth == maxDepth:
        print(printIndent, '[min_value] max-depth, score:', score)
        return score
    else:
        legalMoves = game.get_legal_moves()
        print(printIndent, '[min_value] legal_moves', legalMoves)
        # scores = []
        movesAndScores = []
        for candidateMove in legalMoves:
            # add a tuple of (move, score)
            candidateScore = max_value(player, game.forecast_move(candidateMove), depth+1, maxDepth, calculate_score)
            # scores.append(candidateScore)
            movesAndScores.append((candidateMove, candidateScore))

        pair = min(movesAndScores, key=itemgetter(1))
        print(printIndent, '[min_value] (move, score):', pair)
        return pair[1]


def plain_minimax(player, game, depth, isMax, calculate_score):
    print('Plain minimax!')
    return max_value(player, game, 0, 3, calculate_score)
