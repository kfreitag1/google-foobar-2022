
def triangular_number(n):
  """Bottom row of triangle: value at index n is n more than the previous"""
  n = n + 1  # Start at index = 1 not 0
  return n * (n - 1) / 2

def solution(x, y):
  # Find triangle number at bottom, and subtract the offset. ex:
  # .
  # . . 
  # . . .
  # . O . .
  # . . \ . .
  # . . . * . . 
  #       |
  #       Triangle number at bottom, decrease by 2 to get the ID
  bunny_ID = triangular_number(x + y - 1) - (y - 1)
  return str(bunny_ID)