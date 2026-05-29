"""
mcts.py
-------
Monte-Carlo Tree Search (MCTS)
Author: Student Submission

MCTS is a heuristic search algorithm used in decision-making problems.
Unlike Minimax, it does NOT need an evaluation function. Instead, it
simulates random games (rollouts) and uses statistics to guide search.

The 4 phases of MCTS:
  1. SELECTION   — traverse the tree using UCB1 formula
  2. EXPANSION   — add a new child node
  3. SIMULATION  — play out a random game from that node
  4. BACKPROP    — update win/visit counts up the tree

UCB1 formula (Upper Confidence Bound):
  UCB1 = (wins / visits) + C * sqrt(ln(parent_visits) / visits)

  C is the exploration constant (typically sqrt(2)).
  High UCB1 → node is either promising or underexplored.
"""

import math
import random
import sys
sys.path.insert(0, '.')
from minimax import ttt_winner, ttt_is_terminal, print_board


class MCTSNode:
    """Represents a single node in the MCTS tree."""

    def __init__(self, state, parent=None, move=None):
        """
        Parameters
        ----------
        state  : (board, player) tuple
        parent : parent MCTSNode, or None for root
        move   : (row, col) that led to this state from parent
        """
        self.state = state
        self.parent = parent
        self.move = move

        self.children = []
        self.visits = 0
        self.wins = 0.0

        # All possible moves not yet expanded
        board, player = state
        self.untried_moves = [
            (i, j)
            for i in range(3)
            for j in range(3)
            if board[i][j] == 0
        ]

    def is_fully_expanded(self):
        """True if every legal move has been expanded into a child."""
        return len(self.untried_moves) == 0

    def is_terminal(self):
        """True if no moves remain or someone has won."""
        board, _ = self.state
        return ttt_is_terminal(board)

    def ucb1(self, exploration_constant=math.sqrt(2)):
        """
        UCB1 score for this node.
        Higher = more worth visiting next.
        """
        if self.visits == 0:
            return float('inf')   # Unvisited nodes are highest priority
        exploitation = self.wins / self.visits
        exploration = exploration_constant * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )
        return exploitation + exploration

    def best_child(self, exploration_constant=math.sqrt(2)):
        """Returns the child with the highest UCB1 score."""
        return max(self.children, key=lambda c: c.ucb1(exploration_constant))

    def expand(self):
        """
        Picks one untried move, creates a child node for it,
        and returns that child.
        """
        move = self.untried_moves.pop()  # pick and remove one untried move
        board, player = self.state

        new_board = [row[:] for row in board]
        new_board[move[0]][move[1]] = player

        child_state = (new_board, -player)  # switch player
        child = MCTSNode(child_state, parent=self, move=move)
        self.children.append(child)
        return child

    def rollout(self):
        """
        Simulate a random game from this state until terminal.
        Returns:
           1  if the player who just moved (at this node) wins
           0  for draw
          -1  if opponent wins
        """
        board = [row[:] for row in self.state[0]]
        current_player = self.state[1]

        while not ttt_is_terminal(board):
            empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == 0]
            if not empty:
                break
            move = random.choice(empty)
            board[move[0]][move[1]] = current_player
            current_player = -current_player

        winner = ttt_winner(board)
        # Result from the perspective of the ROOT player (player 1 = X)
        if winner == 1:
            return 1
        elif winner == -1:
            return -1
        else:
            return 0

    def backpropagate(self, result):
        """
        Walk up to root, updating visits and wins.
        Result is from X's perspective: 1 = X wins, -1 = O wins, 0 = draw.
        """
        self.visits += 1
        # Add win credit based on whose turn it is at this node
        # (the player who JUST MOVED is the opposite of state's current player)
        node_player = -self.state[1]  # player who made the move to reach this node
        if result == node_player:
            self.wins += 1
        elif result == 0:
            self.wins += 0.5   # draw = half credit
        self.parent and self.parent.backpropagate(result)


def mcts(root_state, num_simulations=1000):
    """
    Run MCTS for num_simulations iterations and return the best move.

    Parameters
    ----------
    root_state       : (board, player) starting state
    num_simulations  : number of rollout iterations

    Returns
    -------
    best_move  : (row, col) of the recommended move
    best_child : the child node of that move
    """
    root = MCTSNode(root_state)

    for _ in range(num_simulations):
        # ── Phase 1: SELECTION ────────────────────────────────────────────
        node = root
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.best_child()

        # ── Phase 2: EXPANSION ────────────────────────────────────────────
        if not node.is_terminal() and not node.is_fully_expanded():
            node = node.expand()

        # ── Phase 3: SIMULATION (Rollout) ─────────────────────────────────
        result = node.rollout()

        # ── Phase 4: BACKPROPAGATION ──────────────────────────────────────
        node.backpropagate(result)

    # Choose the child with the most visits (most reliable estimate)
    best = max(root.children, key=lambda c: c.visits)
    return best.move, best


# ─── Quick demo ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Monte-Carlo Tree Search Demo ===\n")
    random.seed(42)

    empty_board = [[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]
    state = (empty_board, 1)   # X goes first

    move, best_child_node = mcts(state, num_simulations=500)
    print(f"MCTS recommends move: row={move[0]}, col={move[1]}")
    print(f"Visits: {best_child_node.visits}, Wins: {best_child_node.wins:.1f}")
    print("\nResulting board:")
    print_board(best_child_node.state[0])

    # Test 2: near-win for X
    # X . X
    # . O .
    # . O .
    near_win = [[1,  0,  1],
                [0, -1,  0],
                [0, -1,  0]]
    state2 = (near_win, 1)

    move2, node2 = mcts(state2, num_simulations=300)
    print(f"\nNear-win board — MCTS recommends: row={move2[0]}, col={move2[1]}")
    print("Resulting board:")
    print_board(node2.state[0])
