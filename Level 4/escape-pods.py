from operator import add

def maximum_bunnies_rescuable(corridors):
  """Returns the maximum number of bunnies that can travel from a starting node (first index) 
  and an ending node (last index) in an array of corridor sizes

  Based on the Ford-Fulkerson and Edmonds-Karp algorithms to determine the maximum flow
  through a graph network from a source to a sink node

  Note: The Edmonds-Karp algorithm is a specific implementation of the Ford-Fulkerson search
        where nodes are selected through a breadth-first-search. This is important for this
        challenge because the maximum number of bunnies (2,000,000) is significantly greater
        than the maximum number of rooms (50), and so would have a significant performance
        advantage.

  Args:
    corridors (List(List(int))): Matrix of max corridor sizes from a room to another room

  Returns:
    int: The number of bunnies that can travel to the escape pods
  """

  num_rooms = len(corridors)
  escape_pods_room = num_rooms - 1

  # The current traffic of bunnies, or "flow" as defined in the Ford-Fulkerson algorithm
  bunny_traffic = [[0 for _ in range(num_rooms)] for _ in range(num_rooms)]

  while True:
    # Only continue if there is a path that has available space for bunnies
    path_with_capacity = find_bunny_path(corridors, bunny_traffic)
    if path_with_capacity is None: break

    previous_room = None
    bottleneck_traffic_through_path = float('Inf')
    
    # Generate the bottleneck capacity for the given path
    # i.e. equal to the minimum cooridor along the path, becuase only that many bunnies 
    #      can fit through
    for room_index, room in enumerate(path_with_capacity):
      if room_index > 0:
        capacity = corridors[previous_room][room] - bunny_traffic[previous_room][room]
        bottleneck_traffic_through_path = min(bottleneck_traffic_through_path, capacity)
      previous_room = room

    # Add the number of bottleneck bunnies to the path and subtract that number from the
    # reverse direction (as defined in the FF algorithm to help fine the global maximum value)
    for room_index, room in enumerate(path_with_capacity):
      if room_index > 0:
        bunny_traffic[previous_room][room] += bottleneck_traffic_through_path
        bunny_traffic[room][previous_room] -= bottleneck_traffic_through_path
      previous_room = room

  # The number of bunnes that escaped is equal to the sum of all traffic entering the
  # final escape pods node
  num_escaped_bunnies = sum(bunny_traffic[room][escape_pods_room] for room in range(num_rooms))
  return num_escaped_bunnies


def find_bunny_path(corridors, bunny_traffic):
  """Finds a path along the cooridoors that has available capacity for bunny traffic.
  Involves a breadth first search of the rooms in the cooridors graph.

  Args:
    corridors (List(List(int))): Matrix describing the corridors from room to room
    bunny_traffic (List(List(int))): Matrix describing the bunnies currently flowing 
      through the cooridors

  Returns:
    List(int)/None: The path of room indices or None if no path exists with available capacity
  """

  bunny_start_room = 0
  escape_pods_room = len(corridors) - 1

  # Queue of paths for the breadth first search, start with the bunny starting room
  # List(List(int)) - List of paths that will be searched next
  pathes_to_search = [[bunny_start_room]]

  while len(pathes_to_search) > 0:
    current_path = pathes_to_search.pop(0)
    current_room = current_path[-1]

    # Found the end successfully! Return this path
    if current_room == escape_pods_room:
      return current_path

    # Loop through neighbouring nodes to see if there is a possible connection
    for new_room in range(len(corridors)):
      if new_room in current_path: continue

      # Only proceed if there is available capacity of the new segment (room -> room) 
      # i.e. proceed if the total capacity - current bunny traffic is positive
      bunny_capacity = corridors[current_room][new_room] - \
        bunny_traffic[current_room][new_room]
      if bunny_capacity <= 0: continue

      # The new room is a valid one to search! 
      # Add a new path to the queue with this room at the end
      pathes_to_search.append(current_path + [new_room])


def removed_indices(matrix, indices):
  """Returns a new square matrix that has the rows and columns at the specified incides removed.

  Args:
      matrix (List(List(int))): Original square matrix
      indices (List(int)): Indices of rows/columns to remove

  Returns:
      List(List(int)): The new square matrix
  """
  length = len(matrix)

  return [ 
    [ matrix[row][col] for col in range(length) if col not in indices ] 
    for row in range(length) if row not in indices 
  ]


def compressed_paths(entrances, exits, path):
  """Transforms the path matrix by compressing all the entrances into one row, and all the exits
  into one column and row. This is a necessary transformation as an input to the Ford-Fulkerson
  max flow algorithm, which requires a single source (entrance) and sink (exit) node.

  Also returns the number of bunnies that can be rescued immediately. i.e. The bunnies that
  directly flow from an entrance to an exit.

  Args:
      entrances (List(int)): Indices of entrances
      exits (List(int)): Indices of exits
      path (List(List(int))): Matrix of coridoor sizes between rooms

  Returns:
      int, List(List(int)): Number of bunnies immediately rescued, The transformed matrix
  """

  # Starting bunnies row is simply the row-wise sum of the entrances
  starting_bunnies = [0] * len(path)
  for entrance in entrances:
    starting_bunnies = map(add, starting_bunnies, path[entrance])

  # The bunnies that directly go from an entrance to an exit!
  bunnies_rescued_immediately = sum(
    [bunnies for index, bunnies in enumerate(starting_bunnies) if index in exits]
  )

  # Escape pod row is the column-wise sum of all the rooms leading to the exits
  escape_pods = [0] * len(path)
  for index in range(len(path)):
    pointing_to_escape_pod = [path[index][exit_index] for exit_index in exits]
    escape_pods[index] = sum(pointing_to_escape_pod)

  # Shorten the starting bunnies row and escape pods column to fit the new matrix
  # when the extra indices are removed/rearranged
  starting_bunnies = [starting_bunnies[i] for i in range(len(path)) if i not in entrances + exits]
  escape_pods = [escape_pods[i] for i in range(len(path)) if i not in entrances + exits]
  
  # Remove all the old entrances and exits
  new_path = removed_indices(path, entrances + exits)

  # Add the column leading to the combined escape pod
  new_path = [[0] + row + [escape_pods[i]] for i, row in enumerate(new_path)]

  new_path.insert(0, [0] + starting_bunnies + [0]) # Add the combined starting bunny row
  new_path.append([0] * len(new_path[0]))          # Finally, add the escape pod row

  return bunnies_rescued_immediately, new_path


def solution(entrances, exits, path):
  bunnies_rescued_immediately, compressed_path = compressed_paths(entrances, exits, path)
  return bunnies_rescued_immediately + maximum_bunnies_rescuable(compressed_path)
