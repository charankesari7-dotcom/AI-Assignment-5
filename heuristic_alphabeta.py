"""
heuristic_alphabeta.py
----------------------
Heuristic Alpha-Beta Search
Author: Student Submission

In games with very large search trees (like Chess), we cannot search to
the terminal state in reasonable time. Instead, we:
  1. Limit search depth (depth cutoff).
  2. Use a HEURISTIC evaluation function that estimates how good a
     non-terminal position is for the MAX player.

This makes the algorithm practical for real games at the cost of
potentially missing optimal moves deep in the tree.

Heuristic used here for Tic-Tac-Toe:
  - Count lines where only X exists (weighted by length)
  - Count lines where only O exists (weighted by length)
  - Score = (X-lines score) - (O-lines score)
"""

import sys
sys.path.insert(0, '.')
from minimax import (
    ttt_get_children, ttt_is_terminal_state,
    ttt_winner, print_board
)


def heuristic_evaluate(state):
    """
    Heuristic evaluation function for Tic-Tac-Toe.

    Assigns a score to a NON-TERMINAL board position.
    Uses line analysis: a line with only X marks scores positively,
    only O marks scores negatively.

    Score per line:
      2 marks of same player in a line (3rd empty) → ±10
      1 mark of same player in a line (2,3 empty)  → ±1
      Mixed line (both players present)             → 0

    Terminal states override: +100 / -100 / 0.
    """
    board, _ = state
    winner = ttt_winner(board)

    # Terminal override
    if winner == 1:
        return 100
    if winner == -1:
        return -100
    if winner == 0:
        return 0

    # Build all lines (rows, columns, diagonals)
    lines = []
    for i in range(3):
        lines.append([board[i][j] for j in range(3)])   # row
        lines.append([board[j][i] for j in range(3)])   # column
    lines.append([board[i][i] for i in range(3)])        # main diagonal
    lines.append([board[i][2 - i] for i in range(3)])    # anti diagonal

    score = 0
    for line in lines:
        x_count = line.count(1)
        o_count = line.count(-1)

        # Only score a line if it's not blocked (no mixed marks)
        if x_count > 0 and o_count == 0:
            score += 10 ** x_count   # 1 mark → 10, 2 marks → 100
        elif o_count > 0 and x_count == 0:
            score -= 10 ** o_count

    return score


def heuristic_alphabeta(state, depth, alpha, beta, is_maximizing,
                         get_children, evaluate, is_terminal):
    """
    Alpha-Beta with heuristic evaluation at depth cutoff.

    Same structure as standard alpha-beta, but stops at depth=0
    and calls the heuristic evaluate function (not just terminal check).
    """
    # Stop at depth limit OR terminal — both call evaluate
    if depth == 0 or is_terminal(state):
        return evaluate(state)

    children = get_children(state)
    if not children:
        return evaluate(state)

    if is_maximizing:
        value = float('-inf')
        for child in children:
            child_value = heuristic_alphabeta(
                child, depth - 1, alpha, beta,
                False, get_children, evaluate, is_terminal
            )
            value = max(value, child_value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break  # beta cut-off
        return value
    else:
        value = float('inf')
        for child in children:
            child_value = heuristic_alphabeta(
                child, depth - 1, alpha, beta,
                True, get_children, evaluate, is_terminal
            )
            value = min(value, child_value)
            beta = min(beta, value)
            if beta <= alpha:
                break  # alpha cut-off
        return value


def heuristic_best_move(state, depth, get_children, evaluate, is_terminal):
    """
    Returns the best move using heuristic alpha-beta at given depth.
    """
    alpha = float('-inf')
    beta = float('inf')
    best_value = float('-inf')
    best_child = None

    for child in get_children(state):
        value = heuristic_alphabeta(
            child, depth - 1, alpha, beta,
            False, get_children, evaluate, is_terminal
        )
        if value > best_value:
            best_value = value
            best_child = child
        alpha = max(alpha, best_value)

    return best_child, best_value


# ─── Quick demo ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Heuristic Alpha-Beta Demo ===\n")

    # Test with limited depth (3 instead of full 9)
    empty_board = [[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]
    start_state = (empty_board, 1)

    for depth in [2, 4, 9]:
        best_child, best_val = heuristic_best_move(
            start_state,
            depth=depth,
            get_children=ttt_get_children,
            evaluate=heuristic_evaluate,
            is_terminal=ttt_is_terminal_state
        )
        print(f"Depth = {depth}, Heuristic value = {best_val}")
        print_board(best_child[0])

    # Mid-game board
    # X O .
    # . X .
    # O . .
    mid_game = [[1,  -1, 0],
                [0,   1, 0],
                [-1,  0, 0]]
    state_mid = (mid_game, 1)

    best_child2, best_val2 = heuristic_best_move(
        state_mid,
        depth=4,
        get_children=ttt_get_children,
        evaluate=heuristic_evaluate,
        is_terminal=ttt_is_terminal_state
    )
    print("Mid-game best move (depth=4):")
    print_board(best_child2[0])
    print(f"Heuristic value: {best_val2}")
