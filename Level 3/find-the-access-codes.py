

def solution(integers):
  length = len(integers)

  # Edge case when less than three numbers, cannot have triplet
  if length < 3: return 0

  # Order the list from "largest to smallest" 
  integers.reverse()

  # Represents the total number of matches when checking multiples at the index
  # ex. [0, 0, 0, 2 ...] means that the 4th number in the (reversed) list is a
  #     divisor of two previous (not specified) numbers
  num_multiple_matches = [0 for _ in range(length)]
  num_triplets = 0

  # Iterate through reversed list to find all numbers which divide into the 
  # current "main integer"
  for main_index, main_integer in enumerate(integers[:-1]):

    # Go through all numbers after the "main integer," termed "comp(arison) 
    # integers," in the list to see if they divide into the "main integer"
    for comp_index, comp_integer in enumerate(integers[main_index + 1:]):

      if main_integer % comp_integer == 0:  # Found divisor!
        
        # Update the multiple matches array with one match added to the index 
        # for "comp integer"
        num_multiple_matches[comp_index + main_index + 1] += 1

        # If the number of matches for the "main integer" is a number greater than
        # zero, that means that new triplets were found!
        #
        # i.e. in increasing order, the triplet will be of the form:
        #      (comp_integer, main_integer, x), where x is any number of previous
        #                                       numbers which were a multiple of
        #                                       main_integer
        # 
        num_triplets += num_multiple_matches[main_index]

  return num_triplets