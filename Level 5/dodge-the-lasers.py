from decimal import Decimal, getcontext

# Need reaaallly good precision for large inputs
getcontext().prec = 110
sqrt_two = Decimal(2).sqrt()

def sequence_sum_floor_i_root_two(i):
  """Recursively finds the sum of f(n) = floor(n * sqrt 2) for n=1 -> i.
  Based on the idea that f(n) has an (evil) twin counterpart, s(n), which when joined together
  list all the natural numbers greater than 1 with NO intersections. 
  
  Therefore, for finding the sum of f(n) from n=1 to i, you can generate an expression 
  sum_natural_numbers = sum(f(n)) + sum(s(n)). The sum of natural numbers from 1 -> i is simply
  i(i+1)/2. After inserting, and doing some magic to rearrange the expression, yields a self-
  refferential expression which allows for the sum to be found. This process is effecient as the
  recursion steps down to ~41% ([sqrt 2] - 1) of the previous value of i each time. Therefore, even
  from a starting value of 10^100, the recursion quickly approaches a value of i = 0.

  Args:
      i (int): Index of final value to sum to

  Returns:
      int: Sum of f(n) = floor(n * sqrt 2) for n=1 -> i.
  """
  if i == 0: return 0

  i_prime = int((sqrt_two - 1) * i)
  sub_sequence = sequence_sum_floor_i_root_two(i_prime)

  return i * i_prime + i * (i + 1) / 2 - i_prime * (i_prime + 1) / 2 - sub_sequence

def solution(n):
  # Solve the problem by finding the sum of the Beatty sequence as described in 
  # https://math.stackexchange.com/questions/2052179/how-to-find-sum-i-1n-left-lfloor-i-sqrt2-right-rfloor-a001951-a-beatty-s
  #
  # (The number #1 Google search result for "sum of floor n sqrt 2"! How convenient!)
  return str(sequence_sum_floor_i_root_two(int(n)))

