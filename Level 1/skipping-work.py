
def solution(x, y):

  # Search the longer list to find the unique ID
  search_list = x if len(x) > len(y) else y
  compare_list = y if len(x) > len(y) else x

  # Returns the element unique to both lists
  for id in search_list:
    if id not in compare_list: return id

  raise Exception("Found no unique IDs in longest list")

