from itertools import permutations, product

class TimeGainLoopException(Exception):
  """Raised when a cycle is detected that could lead to an infinite time gain"""
  pass

def find_shortest_time(from_location, to_location, times, shortest_times = None):
  """Finds the path with the shortest time duration between one location and another

  Args:
      from_location (int): Index of the starting location
      to_location (int): Index of the final location
      times (List(List(int))): Matrix for times between locations
      shortest_times (List(List(int/None)), optional): Precomputed optimal times to use 
        to speed up the calculation. Defaults to None.
  """
  
  def search(path, current_time = 0, best_time = 10000):
    """Resursively searches for the best path

    Args:
        path (List(int)): Current path as a list of indices
        current_time (int, optional): Current travel time for the path.
        best_time (int, optional): Best time among all paths.

    Returns:
        int: The best time among all the paths
    """
    current_location = path[-1]
    num_locations = len(times)
    indices_to_search = [i for i in range(num_locations) if i not in path]
    
    for new_location in indices_to_search:
      
      # Use the precomputed table values if they are found for the given location pairs
      if shortest_times is not None and shortest_times[current_location][new_location] is not None:
        time = current_time + shortest_times[current_location][new_location]
        if new_location == to_location:
          best_time = min(time, best_time)
          continue
      
      # Otherwise, use the default location time values
      time = current_time + times[current_location][new_location]

      # Got to the final location! Update the best time if it is faster
      if new_location == to_location:
        best_time = min(time, best_time)
        continue
      
      # Recursively search down the path
      best_time = search(path + [new_location], time, best_time)

    return best_time

  return search([from_location])

def compute_shortest_times(times):
  """Computes the shortest path times for all the locations in the original time matrix

  Args:
      times (List(List(int))): Original matrix for the times between locations

  Raises:
      TimeGainLoopException: An infinfite time gain loop was detected!

  Returns:
      List(List(int)): Matrix for the shortest optimal times between locations
  """

  length = len(times)
  shortest_times = [[None for _ in range(length)] for _ in range(length)]

  # Start with all the negative times between locations to check for time gain loops
  for from_location, to_location in product(range(length), repeat=2):
    if times[from_location][to_location] >= 0:
      continue

    # Shortest time in the opposite direction as the negative path
    shortest_time = find_shortest_time(to_location, from_location, times, shortest_times)

    if times[from_location][to_location] + shortest_time < 0:
      raise TimeGainLoopException  # Found an infinite time loop cycle

    # Add shortest time to precomputed matrix
    shortest_times[to_location][from_location] = shortest_time

  # Loop through all the other locations to find the optimal times
  for from_location, to_location in product(range(length), repeat=2):
    if from_location == to_location:
      shortest_times[from_location][to_location] = 0
    else:
      shortest_times[from_location][to_location] = find_shortest_time(from_location, to_location, times, shortest_times)

  return shortest_times


def solution(times, time_limit):
  num_bunnies = len(times) - 2
  end_index = len(times) - 1

  try:
    shortest_times = compute_shortest_times(times)
  except TimeGainLoopException:
    # Found an infinite time loop in the matrix somewhere
    # Therefore, can rescue all the bunnies, yay!!!
    return [i for i in range(num_bunnies)]

  # Loop through all possible numbers of bunnies to save, starting with the most
  for num_bunnies_to_save in range(num_bunnies, 0, -1):

    # All permutations of the bunny locations for the given number of bunnies to save
    bunny_order_permutations = list(permutations([i for i in range(num_bunnies)], num_bunnies_to_save))

    # Check the path to see if it is doable in the time limit
    # i.e. starting location -> bunny permutations -> bulkhead
    for bunny_order in bunny_order_permutations:
      locations_to_visit = [bunny + 1 for bunny in bunny_order]
      locations_to_visit.append(end_index)

      # Compute the total time to traverse the path
      travel_time = 0
      for index in range(num_bunnies_to_save + 1):
        from_location = 0 if index == 0 else locations_to_visit[index - 1]
        to_location = locations_to_visit[index]
        travel_time += shortest_times[from_location][to_location]

        if travel_time > time_limit: continue

      # The travel time is doable within the time limit! Return the number of bunnies saved
      if travel_time <= time_limit:
        return sorted(list(bunny_order))

  # Can't save any bunnies (sad), or there are no bunnies to save!
  return []
