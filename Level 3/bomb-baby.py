
def solution(M, F):
  bombs = [int(M), int(F)]
  
  final_num_cycles = None
  current_num_cycles = 0

  # Work backwards by continually subtracting off multiples of the smaller
  # bomb from the largest one until the starting condition of (1, 1) is reached
  while True:
    # Ensure that the second bomb is always the biggest (or equal in size)
    bombs.sort()

    # If one or both of the numbers are one, then the final answer is easily
    # reached! Because each cycle beyond this point would subtract 1 from the 
    # larger bomb, the total number of remaining cycles is simply the number of
    # the larger bomb (minus one)
    if bombs[0] == 1:
      final_num_cycles = current_num_cycles + bombs[1] - 1
      break

    # If the smaller bomb is a multiple of the larger bomb, then the problem is 
    # impossible because you would end up with having one of the numbers of bombs
    # being equal to 0, which is smaller than the known initial state of 1
    remainder = bombs[1] % bombs[0]
    if remainder == 0: break

    # Subtract the greatest number of multiples of the smaller bomb from the
    # largest bomb and add that many cycles.
    multiples = bombs[1] // bombs[0]
    current_num_cycles += multiples
    bombs[1] = bombs[1] - multiples * bombs[0]

  return str(final_num_cycles) if final_num_cycles is not None else "impossible"
