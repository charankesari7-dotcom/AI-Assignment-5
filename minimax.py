"""
minimax.py
----------
Minimax Search Algorithm Implementation
Author: Student Submission

The Minimax algorithm is a recursive decision-making algorithm used in
two-player zero-sum games. One player tries to MAXIMIZE the score
(called MAX), and the other tries to MINIMIZE it (called MIN).

The tree is searched to a terminal state or a given depth, and the
best move is selected based on the minimax value.
"""


def minimax(state, depth, is_maximizing, get_children, evaluate, is_terminal):
    """
    Minimax recursive function.

    Parameters
    ----------
    state          : current game state (any representation)
    depth          : how many more levels to search
    is_maximizing  : True if it's MAX player's turn, False for MIN
    get_children   : function(state) -> list of child states
    evaluate       : function(state) -> numeric score (higher = better for MAX)
    is_terminal    : function(state) -> bool (True if game over)

    Returns
    -------
    best_value : int/float — the minimax value of this state
    """

    # Base case: if we've hit depth limit or terminal state, evaluate
    if depth == 0 or is_terminal(state):
        return evaluate(state)

    children = get_children(state)

    # If no children exist, treat as terminal
    if not children:
        return evaluate(state)

    if is_maximizing:
        # MAX player wants the highest value
        best_value = float('-inf')
        for child in children:
            # Recurse: next turn is MIN's
            value = minimax(child, depth - 1, False, get_children, evaluate, is_terminal)
            best_value = max(best_value, value)
        return best_value
    else:
        # MIN player wants the lowest value
        best_value = float('inf')
        for child in children:
            # Recurse: next turn is MAX's
            value = minimax(child, depth - 1, True, get_children, evaluate, is_terminal)
            best_value = min(best_value, value)
        return best_value


def minimax_best_move(state, depth, get_children, evaluate, is_terminal):
    """
    Wrapper: returns the best child state for the MAX player.

    Parameters
    ----------
    Same as minimax(), minus is_maximizing (always starts as MAX).

    Returns
    -------
    best_child : the child state with the highest minimax value
    best_value : the minimax value of that child
    """
    best_value = float('-inf')
    best_child = None

    for child in get_children(state):
        # From child onwards, it's MIN's turn
        value = minimax(child, depth - 1, False, get_children, evaluate, is_terminal)
        if value > best_value:
            best_value = value
            best_child = child

    return best_child, best_value


# ─── Tic-Tac-Toe helper functions (used for testing) ──────────────────────────

def ttt_is_terminal(board):
    """Returns True if the Tic-Tac-Toe board is in a terminal state."""
    return ttt_winner(board) is not None or all(cell != 0 for row in board for cell in row)


def ttt_winner(board):
    """
    Checks all rows, columns, and diagonals.
    Returns 1 (X wins), -1 (O wins), 0 (draw), or None (game not over).
    """
    lines = []
    # Rows and columns
    for i in range(3):
        lines.append([board[i][j] for j in range(3)])
        lines.append([board[j][i] for j in range(3)])
    # Diagonals
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line == [1, 1, 1]:
            return 1   # X wins
        if line == [-1, -1, -1]:
            return -1  # O wins

    if all(cell != 0 for row in board for cell in row):
        return 0  # draw
    return None  # not finished


def ttt_evaluate(board):
    """
    Simple evaluation for Tic-Tac-Toe:
      +10  → X wins
      -10  → O wins
       0   → draw or in progress
    """
    winner = ttt_winner(board)
    if winner == 1:
        return 10
    if winner == -1:
        return -10
    return 0


def ttt_get_children(state):
    """
    Generates all possible next states.
    state = (board, current_player)
    current_player: 1 = X, -1 = O
    """
    board, player = state
    children = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:  # empty cell
                # Create a copy and place the player's mark
                new_board = [row[:] for row in board]
                new_board[i][j] = player
                children.append((new_board, -player))  # switch player
    return children


def ttt_is_terminal_state(state):
    board, _ = state
    return ttt_is_terminal(board)


def ttt_evaluate_state(state):
    board, _ = state
    return ttt_evaluate(board)


def print_board(board):
    symbols = {1: 'X', -1: 'O', 0: '.'}
    for row in board:
        print(' '.join(symbols[c] for c in row))
    print()


# ─── Quick demo ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Minimax Demo: Tic-Tac-Toe ===\n")

    # Empty board, X goes first (player=1)
    empty_board = [[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]
    start_state = (empty_board, 1)

    best_child, best_val = minimax_best_move(
        start_state,
        depth=9,
        get_children=ttt_get_children,
        evaluate=ttt_evaluate_state,
        is_terminal=ttt_is_terminal_state
    )
    print("Best first move board for X:")
    print_board(best_child[0])
    print(f"Minimax value of best move: {best_val}")
