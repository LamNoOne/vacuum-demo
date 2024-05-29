import heapq


def heuristic(a, b):
    """Tính toán khoảng cách Manhattan giữa hai điểm a và b"""
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(matrix, start, goal):
    """Thuật toán A* tìm đường đi ngắn nhất từ start đến goal"""
    neighbors = [
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    ]  # Các hướng di chuyển (phải,xuống,trái,trên)

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    print("heuristic: ", heuristic(start, goal))
    fscore = {start: heuristic(start, goal)}
    oheap = []

    print("start: ", start)
    print("fscore: ", fscore[start])

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]
        print("current in heap: ", current)

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            print("neighbor: ", neighbor)
            tentative_g_score = gscore[current] + 1

            if 0 <= neighbor[0] < len(matrix) and 0 <= neighbor[1] < len(matrix[0]):
                if matrix[neighbor[0]][neighbor[1]] == 1:
                    continue
            else:
                # Nằm ngoài phạm vi bản đồ
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
            
            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False


def find_closest_goal(current_position, goals):
    """Tìm goal gần nhất với vị trí hiện tại"""
    closest_goal = None
    min_distance = float("inf")
    for goal in goals:
        distance = heuristic(current_position, goal)
        if distance < min_distance:
            closest_goal = goal
            min_distance = distance
    return closest_goal


def find_path_to_closest_goal(matrix, start, goals):
    """Tìm đường đi đến goal gần nhất"""
    path = []
    current_position = start

    while goals:
        print("current_position: ", current_position)
        closest_goal = find_closest_goal(current_position, goals)
        print("closest_goal: ", closest_goal)
        path_to_goal = a_star_search(matrix, current_position, closest_goal)
        print("path_to_goal: ", path_to_goal)
        if path_to_goal:
            path.extend(path_to_goal)
            current_position = closest_goal
            goals.remove(closest_goal)
        else:
            # Nếu không tìm thấy đường đến goal gần nhất, hãy chọn một goal khác
            goals.remove(closest_goal)

    return path


# Sử dụng:
# goals = [(4, 4), (2, 2), (3, 3)]  # Danh sách các vị trí hạt bụi


# Ví dụ sử dụng:
# matrix = [[0, 0, 0, 0, 0],  # 0 là đường đi, 1 là vật cản
#           [0, 1, 1, 1, 0],
#           [0, 0, 0, 0, 0],
#           [0, 1, 1, 1, 0],
#           [0, 0, 0, 0, 0]]

# start = (0, 0)  # Vị trí xuất phát
# goals = [(4, 4), (2, 2), (4, 1)]   # Vị trí đích
# path_to_goals = find_path_to_closest_goal(matrix, start, goals)
# print(path_to_goals)
