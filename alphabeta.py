"""
alphabeta.py
------------
Alpha-Beta Pruning Search Algorithm
Author: Student Submission

Alpha-Beta pruning is an optimization of the Minimax algorithm.
It prunes (skips) branches that cannot possibly affect the final decision,
which dramatically reduces the number of nodes evaluated.

Key idea:
  alpha = best value MAX can guarantee so far (starts at -inf)
  beta  = best value MIN can guarantee so far (starts at +inf)

If at any point beta <= alpha, we prune — no need to explore further.
"""

from minimax import (
    ttt_get_children, ttt_evaluate_state,
    ttt_is_terminal_state, print_board
)


def alphabeta(state, depth, alpha, beta, is_maximizing,
              get_children, evaluate, is_terminal):
    """
    Alpha-Beta pruning recursive function.

    Parameters
    ----------
    state          : current game state
    depth          : remaining search depth
    alpha          : best guaranteed score for MAX player (-inf to start)
    beta           : best guaranteed score for MIN player (+inf to start)
    is_maximizing  : True if it's MAX player's turn
    get_children   : function(state) -> list of child states
    evaluate       : function(state) -> numeric score
    is_terminal    : function(state) -> bool

    Returns
    -------
    value : int/float — the alpha-beta value of this state
    """

    # Base case
    if depth == 0 or is_terminal(state):
        return evaluate(state)

    children = get_children(state)
    if not children:
        return evaluate(state)

    if is_maximizing:
        value = float('-inf')
        for child in children:
            # Evaluate child from MIN's perspective
            child_value = alphabeta(child, depth - 1, alpha, beta,
                                    False, get_children, evaluate, is_terminal)
            value = max(value, child_value)
            alpha = max(alpha, value)

            # Prune: MIN would never allow this path
            # because MAX has already found something better
            if beta <= alpha:
                break  # ← Beta cut-off

        return value

    else:  # Minimizing
        value = float('inf')
        for child in children:
            # Evaluate child from MAX's perspective
            child_value = alphabeta(child, depth - 1, alpha, beta,
                                    True, get_children, evaluate, is_terminal)
            value = min(value, child_value)
            beta = min(beta, value)

            # Prune: MAX would never allow this path
            # because MIN has already found something better
            if beta <= alpha:
                break  # ← Alpha cut-off

        return value


def alphabeta_best_move(state, depth, get_children, evaluate, is_terminal):
    """
    Returns the best move for MAX using Alpha-Beta pruning.

    Returns
    -------
    best_child : state after the best move
    best_value : alpha-beta value of that move
    """
    alpha = float('-inf')
    beta = float('inf')
    best_value = float('-inf')
    best_child = None

    for child in get_children(state):
        value = alphabeta(child, depth - 1, alpha, beta,
                          False, get_children, evaluate, is_terminal)
        if value > best_value:
            best_value = value
            best_child = child
        alpha = max(alpha, best_value)

    return best_child, best_value


# ─── Quick demo ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Alpha-Beta Pruning Demo: Tic-Tac-Toe ===\n")

    # Test 1: Empty board — X moves first
    empty_board = [[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]
    start_state = (empty_board, 1)

    best_child, best_val = alphabeta_best_move(
        start_state,
        depth=9,
        get_children=ttt_get_children,
        evaluate=ttt_evaluate_state,
        is_terminal=ttt_is_terminal_state
    )
    print("Best first move board for X:")
    print_board(best_child[0])
    print(f"Alpha-Beta value: {best_val}\n")

    # Test 2: Near-end board — X can win in one move
    # X . X
    # . O .
    # . O .
    near_end = [[1,  0,  1],
                [0, -1,  0],
                [0, -1,  0]]
    state2 = (near_end, 1)

    best_child2, best_val2 = alphabeta_best_move(
        state2,
        depth=9,
        get_children=ttt_get_children,
        evaluate=ttt_evaluate_state,
        is_terminal=ttt_is_terminal_state
    )
    print("X can win — best move:")
    print_board(best_child2[0])
    print(f"Alpha-Beta value: {best_val2}")
