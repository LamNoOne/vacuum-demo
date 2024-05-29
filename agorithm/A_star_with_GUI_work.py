import heapq
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import font
from PIL import Image, ImageTk
from collections import deque
import random
import time
result = None
dust_positon = None
table_frame = None  # Biến toàn cục để lưu trữ frame chứa bảng


def heuristic(a, b):
    """ Tính toán khoảng cách Manhattan giữa hai điểm a và b """
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(matrix, start, goal):
    """ Thuật toán A* tìm đường đi ngắn nhất từ start đến goal """
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Các hướng di chuyển (phải,xuống,trái,trên)
    
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))
    
    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + 1

            if 0 <= neighbor[0] < len(matrix):
                if 0 <= neighbor[1] < len(matrix[0]):
                    if matrix[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # Nằm ngoài phạm vi bản đồ
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
    """ Tìm goal gần nhất với vị trí hiện tại """
    closest_goal = None
    min_distance = float('inf')
    for goal in goals:
        # print("Current Position:", current_position, "Goal:", goal)
        # print("goals"+str(goals))
        distance = heuristic(current_position, goal)
        if distance < min_distance:
            closest_goal = goal
            min_distance = distance
    return closest_goal

def find_path_to_closest_goal(matrix, start, goals):
    """ Tìm đường đi đến goal gần nhất """
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
            # Nếu không tìm thấy đường đến goal gần nhất, hãy chọn một goal khác
            goals.remove(closest_goal)

    return path

def random_matrix (num_rows, num_cols,num_obs,num_dust):
    
    arr = [0 for i in range(num_rows*num_cols)]
    
    obs_position = random.sample(range(num_rows*num_cols),num_obs)
    for pos in obs_position:
        arr[pos] = 1        #1 đại diện cho vật cản
    
    empty_positions = [i for i, x in enumerate(arr) if x == 0]

    dust_and_vacuum_positions = random.sample(empty_positions, num_dust + 1)
    vacuum_position = dust_and_vacuum_positions.pop()  # Lấy vị trí cuối cùng cho máy hút bụi
    for pos in dust_and_vacuum_positions:
        arr[pos] = 2

    start_position = (vacuum_position // num_cols , vacuum_position % num_cols)

    matrix = [arr[i * num_cols:(i + 1) * num_cols] for i in range(num_rows)]

    return {
        'matrix': matrix,
        'start_position': start_position
    }

def create_table():
    global num_cols,num_rows,num_obs,num_dust,table_frame,result,vacuum_pos,dust_positions
    num_rows = int(row_entry.get())
    num_cols = int(column_entry.get())
    num_obs = int(obstacle_entry.get())  # Số lượng vật cản
    num_dust = int(dust_entry.get())  # Số lượng bụi
    
    
    result = random_matrix(num_rows, num_cols, num_obs, num_dust)
    obstacle_positions = {(i, j) for i in range(num_rows) for j in range(num_cols) if result['matrix'][i][j] == 1}
    dust_positions = {(i, j) for i in range(num_rows) for j in range(num_cols) if result['matrix'][i][j] == 2}
    vacuum_pos = result['start_position']  # Vị trí của máy hút bụi
    #print("vi tri bat dau"+str(result['start_position']))
    if table_frame:
        clear_table()

    table_frame = tk.Frame(window)
    table_frame.grid(row=0, column=1, columnspan=2)

    global vacuum_image, bg_image, dust_image, wall_image

    vacuum_image = ImageTk.PhotoImage(Image.open("vacuum.png").resize((50, 50), Image.LANCZOS))
    bg_image = ImageTk.PhotoImage(Image.open("rac.png").resize((30, 30), Image.LANCZOS))
    dust_image = ImageTk.PhotoImage(Image.open("virus.jpg").resize((50, 50), Image.LANCZOS))
    wall_image = ImageTk.PhotoImage(Image.open("wall.jpg").resize((50, 50), Image.LANCZOS))
    
    for i in range(num_rows):
        for j in range(num_cols):
            if (i, j) == vacuum_pos:
                image = vacuum_image
            elif (i, j) in obstacle_positions:
                image = wall_image
            elif (i, j) in dust_positions:
                image = dust_image
            else:
                image = bg_image

            cell_label = tk.Label(table_frame, image=image, borderwidth=0.5, relief='groove', width=50, height=50, bg='lightblue')
            cell_label.image = image
            cell_label.grid(row=i, column=j, padx=5, pady=5)
            
def update_cell(row, col, image):
    # Tìm widget Label tương ứng và cập nhật hình ảnh
    cell_label = table_frame.grid_slaves(row=row, column=col)[0]
    cell_label.config(image=image)
    cell_label.image = image
    
def move_vacuum(old_x, old_y, new_x, new_y):
    global vacuum_pos
    # Cập nhật vị trí máy hút bụi mới
    # vacuum_pos[0] = new_x
    # vacuum_pos[1] = new_y
    vacuum_pos = (new_x, new_y)
    # Cập nhật giao diện người dùng
    update_cell(old_x, old_y, bg_image)  # Đặt lại ô cũ thành nền
    update_cell(new_x, new_y, vacuum_image)  # Đặt máy hút bụi vào ô mới
    
def clear_table():
    global table_frame
    # Kiểm tra nếu table_frame đã được tạo, sau đó xóa các widget trong Frame
    if table_frame:
        for widget in table_frame.winfo_children():
            if widget != submit_button:
                widget.destroy()
                
def clean_grid():
    global vacuum_pos, num_rows, num_cols, result, table_frame
    dust_positions = [(i, j) for i in range(num_rows) for j in range(num_cols) if result['matrix'][i][j] == 2]
    
    # Vòng lặp qua từng điểm bụi
    for dust in dust_positions:
        # Tính toán đường đi bằng A*
        #start_pos_tuple = tuple(vacuum_pos.values())
        vacuum_pos = result['start_position']
        path = find_path_to_closest_goal(result['matrix'],vacuum_pos  , dust_positions)

        # Di chuyển qua từng bước trên đường đi
        for step in path:
            move_vacuum(vacuum_pos[0], vacuum_pos[1], step[0], step[1])
            window.update()
            time.sleep(0.5)
        
        # Dọn bụi tại vị trí hiện tại
        result['matrix'][dust[0]][dust[1]] = 0
        update_cell(dust[0], dust[1], bg_image)
    
    # Cập nhật vị trí máy hút bụi cuối cùng
    vacuum_pos = {'x': path[-1][1], 'y': path[-1][0]}
    
    
def start_cleaning():
    # Bắt đầu quá trình dọn dẹp
    clean_grid()
    
    
# Tạo một cửa sổ giao diện
window = tk.Tk()
window.title("Thông tin")

# Tạo một LabelFrame với tiêu đề "Nhập thông tin"
info_frame = tk.LabelFrame(window, text="Nhập thông tin", font=("Arial", 12, "bold"), padx=20, pady=20)
#info_frame.pack(pady=20)
info_frame.grid(row=0, column=0, padx=20, pady=20)

# Tạo các Label và Entry box
label_font = font.Font(family="Arial", size=10)

column_label = tk.Label(info_frame, text="Nhập số cột:", font=label_font)
column_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
column_entry = tk.Entry(info_frame, font=label_font)
column_entry.grid(row=0, column=1, padx=10, pady=5)

row_label = tk.Label(info_frame, text="Nhập số hàng:", font=label_font)
row_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
row_entry = tk.Entry(info_frame, font=label_font)
row_entry.grid(row=1, column=1, padx=10, pady=5)

obstacle_label = tk.Label(info_frame, text="Nhập số vật cản:", font=label_font)
obstacle_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
obstacle_entry = tk.Entry(info_frame, font=label_font)
obstacle_entry.grid(row=2, column=1, padx=10, pady=5)

dust_row_label = tk.Label(info_frame, text="Nhập số bụi:", font=label_font)
dust_row_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
dust_entry = tk.Entry(info_frame, font=label_font)
dust_entry.grid(row=3, column=1, padx=10, pady=5)
# Tạo nút "Submit"
submit_button = tk.Button(window, text="Submit", font=("Arial", 12), bg="#4CAF50", fg="white", relief=tk.RAISED,
                          command=create_table)
#submit_button.pack(pady=10)
submit_button.grid(row=6, column=0, columnspan=2, pady=10)

start_cleaning_button = tk.Button(window, text="Start Cleaning",command=start_cleaning)
start_cleaning_button.grid(row=7, column=0, columnspan=2, pady=10)


window.mainloop()
