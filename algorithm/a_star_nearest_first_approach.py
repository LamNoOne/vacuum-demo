import heapq


def heuristic(a, b):
    # Calculate the Manhattan distance between two points
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(matrix, start, goal):
    # A* search algorithm to find the shortest path between two points
    # # Define the possible movements: right, down, left, up
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    # Sets for closed nodes and nodes to be evaluated
    close_set = set()
    oheap = []
    # Dictionary to keep track of the path
    # came_from contains path from begin position to current position, Ex: (0, 2): (1, 2)
    # means we must came to (0, 2) from (1, 2)
    came_from = {}
    # Dictionaries to keep track of the cost from start and the total cost (start to goal)
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    # Push the starting node into the priority queue
    # The priority queue is a heap that stores the nodes with the lowest fscore on top
    heapq.heappush(oheap, (fscore[start], start))
    while oheap:
        # Get the current coordinates from the priority queue
        print("oheap", oheap)
        current = heapq.heappop(oheap)[1]
        print("current", current)
        print("oheap popped", oheap)
        # If the goal is reached, reconstruct and return the path
        if current == goal:
            data = []
            while current in came_from:
                print("current in came_from", current)
                data.append(current)
                current = came_from[current]
            # Return reversed path
            print("data", data)
            return data[::-1]
        
        close_set.add(current)

        for i, j in neighbors:
            # Calculate the neighbor's coordinates and the tentative gscore
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + 1
            # Check if the neighbor is within bounds and not an obstacle
            if 0 <= neighbor[0] < len(matrix):
                if 0 <= neighbor[1] < len(matrix[0]):
                    if matrix[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # Out of bounds
                    continue
            else:
                # Out of bounds
                continue
            # If the neighbor is already in the closed set and has a higher gscore, skip it
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
            # If the neighbor is not in the open set or has a lower gscore, update the scores and path
            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                print("came_from", came_from)
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
    return False # Return False if no path is found


def find_closest_goal(current_position, goals):
    # Find the closest goal from the current position
    closest_goal = None
    min_distance = float("inf")
    for goal in goals:
        distance = heuristic(current_position, goal)
        if distance < min_distance:
            closest_goal = goal
            min_distance = distance
    return closest_goal


def find_path_to_closest_goal(matrix, start, goals):
    # Find the path to the closest goal from the current position
    path = []
    current_position = start
    while goals:
        closest_goal = find_closest_goal(current_position, goals)
        path_to_goal = a_star_search(matrix, current_position, closest_goal)
        if path_to_goal:
            path.extend(path_to_goal)
            current_position = closest_goal
            goals.remove(closest_goal)
        else:
            # If the path to the closest goal is not found, choose another goal
            goals.remove(closest_goal)
    return path


# Usage example:

matrix = [[0, 0, 0, 0, 0, 0],
          [0, 1, 0, 0, 0, 0],
          [0, 0, 0, 0, 1, 0],
          [0, 0, 0, 0, 1, 0],
          [0, 0, 1, 1, 0, 0],
          [0, 0, 0, 0, 0, 0]]

start = (2, 2)
goals = [(0, 0), (0, 2), (2, 5), (5,3)]
path_to_goals = find_path_to_closest_goal(matrix, start, goals)

print("Result:", path_to_goals)

# Result:
# [(1, 0), (2, 0), (2, 1), (2, 2), (2, 1), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
