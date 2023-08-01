import copy
from math import sqrt, floor

class BoardPosition:
  """Representation of a position on a chess board"""

  def __init__(self, numerical_representation = None, position = None):
    """Initilizes BoardPosition

    Args:
        numerical_representation (int): Chess board position as described in challenge (0-63)
        position (x, y) (Tuple(int, int), optional): Alternate position value for direct assignment. 
    """

    # Set position directly if provided with it 
    if position is not None:
      self.position = position
      return

    if numerical_representation is None:
      raise Exception("Need to initialize board with at least one method")

    # Otherwise generate position tuple (x: 0-8, y: 0-8) from numerical representation
    horizontal_position = numerical_representation % 8
    vertical_position = int(floor(numerical_representation / 8))

    self.position = (horizontal_position, vertical_position)

  def __eq__(self, other):
    return self.position == other.position

  def straight_distance_to(self, second_board_position):
    """Returns the straight line distance between self and another point using Pythagoras"""

    horizontal_distance = self.position[0] - second_board_position.position[0]
    vertical_distance = self.position[1] - second_board_position.position[1]
    return sqrt(horizontal_distance ** 2 + vertical_distance ** 2)

  def knight_moves(self):
    """Returns a list of all valid positions a knight's move away from the current position"""

    # All possible moves (x, y) as position offsets
    moves_to_try = [
      (1, 2), (1, -2), (-1, 2), (-1, -2),
      (2, 1), (2, -1), (-2, 1), (-2, -1),
      ]

    def is_valid(pos):
      """Checks to see if position offset would be on the chessboard"""
      valid_horizontal = self.position[0] + pos[0] in range(0, 8)
      valid_vertical = self.position[1] + pos[1] in range(0, 8)
      return valid_horizontal and valid_vertical

    valid_move_offsets = filter(is_valid, moves_to_try)

    # List of all valid knight's move positions as BoardPosition objects
    move_positions = [
      BoardPosition(position = (self.position[0] + offset[0], self.position[1] + offset[1])) 
      for offset in valid_move_offsets
    ]

    return move_positions

def best_path(src_position, dest_position, current_route = None, current_best_num_moves = 1000):
  """Recursively finds the shortest possible path between two chessboard positions 
  using knights moves

  Args:
      src_position (BoardPosition): Starting position on chessboard
      dest_position (BoardPosition): Ending position on chessboard
      current_route (List(BoardPosition), optional): List of the current path taken. Defaults to None.
      current_best_num_moves (int, optional): The smallest possible number of moves to reach the 
        destination obtained so far. Initialized as a very high, unexceedable integer.

  Returns:
      int: Smallest possible number of moves from src to dest
  """

  if current_route is None: current_route = [src_position]

  # Return 0 moves if src is the same as dest
  if src_position == dest_position: return 0
  
  # All the straight line distances of the knights moves from the src to dest positions
  # Represented as list of (position, distance)
  move_distances = [(move, move.straight_distance_to(dest_position)) for move in src_position.knight_moves()]
  move_distances.sort(key = lambda elem: elem[1])  # Sorted in increasing order of distance

  # Iterate through all possible knight moves, starting with the closest ones
  for move_position, distance in move_distances:

    if distance == 0.0:  # One move away from destination! Return total number of moves in route
      return len(current_route)

    if len(current_route) + 1 >= current_best_num_moves:
      continue  # Skip if exceding the number of moves in the best route so far
    
    if move_position in current_route:
      continue  # Skip if this new position has already been seen, no backtracking!
    
    # Create a new route list with the current move position at the end
    new_route = copy.deepcopy(current_route)
    new_route.append(move_position)

    num_moves = best_path(move_position, dest_position, new_route, current_best_num_moves)

    # Update the current best moves if new route is quicker
    if num_moves < current_best_num_moves:
      current_best_num_moves = num_moves

  return current_best_num_moves

def solution(src, dest):
  return best_path(BoardPosition(src), BoardPosition(dest))