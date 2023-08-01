from fractions import Fraction, gcd

#######################
# OBJECTS
#######################

class Matrix:
  """Base matrix class, uses Fraction objects for each value to simpify calculations
  """

  def __init__(self, arr):
    self.values = [ [Fraction(value) for value in row] for row in arr ]

  def __repr__(self):
    """Debug string representation when using print"""
    str_ = ""
    for row in self.values:
      str_ += "["
      str_ += " ".join([str(value) for value in row])
      str_ += "]\n"
    return str_


class TransitionMatrix(Matrix):
  """Transition matrix in the form as descibed in the challenge
  Must be a square matrix of minimum size 2x2
  """

  def sorted_by_terminal_states(self):
    """Moves the terminal states at the bottom of the whole matrix"""
    indices_of_terminal_states = [ \
      index for index, row in enumerate(self.values) \
      if all(i == 0 for i in row) \
    ]

    for index in indices_of_terminal_states:
      # Put column at end
      for i in range(len(self.values)):
        self.values[i].append(self.values[i][index])

      # Put row at end
      self.values.append(self.values[index][:])

    # Remove previous rows
    self.values = [ \
      row for index, row in enumerate(self.values) \
      if index not in indices_of_terminal_states \
    ]
    # Remove previous columns
    for i in range(len(self.values)):
      self.values[i] = [ \
        val for index, val in enumerate(self.values[i]) \
        if index not in indices_of_terminal_states \
      ]


  def to_probabilities(self):
    """Converts the transition matrix from the form described in the challenge
    to one more typical of a stochastic transtion matrix

    i.e. all rows sum to one (100% probability), 
         terminal states have a probability of 1 to go to their own index (final state)
    """
    for index, row in enumerate(self.values):
      denominator = sum(row)

      if denominator == 0:  # Terminal state so probability = 1 (100%) to stay
        new_row = [0 for _ in row]
        new_row[index] = 1
        self.values[index] = new_row
      else:  # Divide values to get probability
        self.values[index] = [value / denominator for value in row]


class AugmentedMatrix(Matrix):
  """Augmented matrix in the form required to solve systems of linear equations
  using Gauss-Jordan elimination. Each row represents a linear equation where the
  values in the matrix are the coefficients of the variables on the left hand side of
  the equation and the last value is the constant on the right hand side.

  ex. for the linear equation: 3x + 0y + 2z = 7
      the row in the matrix would be [3, 0, 2, 7]
  """

  def swap_rows(self, i, j):
    """Swaps the two rows in the matrix

    Args:
        i, j (int): Indices of the rows
    """
    self.values[i], self.values[j] = self.values[j], self.values[i]

  def add_row(self, row_index, row_values):
    """Adds a set of values to the specified row

    Args:
        row_index (int): Index of the row to add values to
        row_values (List(Fraction/int/float)): List of values to add,
          Has to be the same length as the matrix, otherwise throw error
    """
    if len(row_values) != len(self.values[0]):
      raise Exception("Row values to add must be of the same length")

    self.values[row_index] = [ \
      value + row_value \
      for value, row_value in zip(self.values[row_index], row_values) \
    ]

  def multiple_of_row(self, row_index, constant):
    """Returns a constant multiple of the row as a set of values"""
    return [value * constant for value in self.values[row_index]]

  def multiply_row(self, row_index, constant):
    """Multiplies the specified row by a constant"""
    self.values[row_index] = self.multiple_of_row(row_index, constant)

#######################
# HELPER FUNCTIONS 
#######################

def find_linear_equation_solutions(matrix):
  """Solves the given set of linear equations using Gauss-Jordan elimination

  Args:
      matrix (AugmentedMatrix): The augmented matrix containing the equations

  Returns:
      AugmentedMatrix: The resulting matrix after Gauss-Jordan elimination representing
        the solutions to the equations. 
        
        e.g. the solution for a two variable matrix may
        look like: [1, 0, a]  where a and b represent the solutions to the first
                   [0, 1, b]  and second variables, respectively
  """

  # Try to reduce each row to have a value of 1 on the diagonal
  # e.g. at index 2: [0, 0, 1, 0, c] where c is the value of the variable
  #      represented at index 2
  for index in range(len(matrix.values)):

    # Swap current row with another that has a non-zero value to avoid a division
    # by zero error in the next step. Choose the row containing the largest value
    if matrix.values[index][index] == 0:
      column_values = [other_row[index] for other_row in matrix.values]
      row_index_to_swap = column_values.index(max(column_values))

      matrix.swap_rows(index, row_index_to_swap)
    
    # Divide the whole row by the coefficient on the diagonal to make it a 1
    matrix.multiply_row(index, 1 / matrix.values[index][index])

    # Add constant multiples of the current row to the other rows in order to make
    # the values at the same row index 0
    for other_index in range(len(matrix.values)):
      if other_index == index: continue

      row_to_add = matrix.multiple_of_row(index, -matrix.values[other_index][index])
      matrix.add_row(other_index, row_to_add)

  return matrix


def lowest_common_multiple(integer_list):
  """Takes a list of integers and returns the lowest number which can cleanly 
  divide all of the integers in the list"""
  return reduce(lambda x, y: x*y//gcd(x, y), integer_list)


#######################
# MAIN SOLUTION  
#######################     

def solution(m):

  # Edge case if there is only one state, the probability to go from
  # state 0 to state 0 would simply be 1
  if len(m) == 1: return [1, 1]

  matrix = TransitionMatrix(m)
  matrix.sorted_by_terminal_states()
  matrix.to_probabilities()

  # Linear equation arrays are of the form [c1, c2, ... cn, b]
  # where c1, c2, ... cn are coefficients of the variables on the LHS of the equation
  # and b is the constant on the RHS of the equation
  linear_equations_matrix = []
  
  # Generate equations for each row of the transition matrix based on the idea that
  # if you multiple the probailities of the final, steady state by the transition matrix
  # then you would get back the same probabilities. i.e. states * transition_matrix = states
  for index, row in enumerate(matrix.values):
    # Rearrange equation from:  c1 * x0 + c2 * x1 + ... +    ci    * xi + ... + cn * z = xi
    # into gaussian form:       c1 * x0 + c2 * x1 + ... + (ci - 1) * xi + ... + cn * z = 0
    gaussian_linear_equation = row
    gaussian_linear_equation[index] -= 1
    gaussian_linear_equation.append(0)

    if all(value == 0 for value in row):
      continue  # Terminal state, skip
    
    linear_equations_matrix.append(gaussian_linear_equation)

  augmented__linear_equations_matrix = AugmentedMatrix(linear_equations_matrix)
  linear_solution_matrix = find_linear_equation_solutions(augmented__linear_equations_matrix)

  # The resulting solution matrix is not completely solved because the terminal states don't
  # provide any helpful linear equations to help solve for the final probabilities. In essence,
  # there are more variables than equations to use, therefore the Gauss-Jordan elimination
  # process returns an infinite family of solutions.

  # However, not all is lost! Careful observation of the coefficients in the first row,
  # representing the solution to the transition states going from the initial s0 state, show
  # the final probabilities for all of the terminal states.
  #
  # e.g. for the sample case in readme.txt, the first row in the solution matrix is:
  #      [1, 0, 0, -3/14, -1/7, -9/14]
  #      rearranging, this shows that:  s0 = 0 s2 + 3/14 s3 + 1/7 s4 + 9/14 s5  (the solutions!)
  #

  num_non_terminal_states = len(linear_solution_matrix.values)

  terminal_probabilities = linear_solution_matrix.values[0][num_non_terminal_states:-1]
  terminal_probabilities = [-p for p in terminal_probabilities]

  # Convert the fractional properties into the [numerators, denominator] form
  # required as a return value to the solution

  denominators = [p.denominator for p in terminal_probabilities]
  common_denominator = lowest_common_multiple(denominators)

  formatted_probabilities = [ \
    p.numerator * (common_denominator / p.denominator) \
    for p in terminal_probabilities \
  ]
  formatted_probabilities.append(common_denominator)
  
  return formatted_probabilities
