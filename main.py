import customtkinter as ctk
import tkinter.messagebox as messagebox
from customtkinter import CTkFont
from PIL import Image
from customtkinter import CTkImage
from collections import deque
import random
import time
from algorithm.a_star_nearest_first_approach import *
# Global variables to store frame table container, vacuum position, dust positions, and the result matrix
result = None
dust_positon = None
table_frame = None

def random_matrix (num_rows, num_cols,num_obs,num_dust):

    arr = [0 for i in range(num_rows*num_cols)]

    obs_position = random.sample(range(num_rows*num_cols),num_obs)
    for pos in obs_position:
        # Present as an obstacle, value 1 in matrix will be ignore
        arr[pos] = 1

    empty_positions = [i for i, x in enumerate(arr) if x == 0]

    dust_and_vacuum_positions = random.sample(empty_positions, num_dust + 1)
    # Get the last position as the vacuum position
    vacuum_position = dust_and_vacuum_positions.pop()
    for pos in dust_and_vacuum_positions:
        arr[pos] = 2

    print("arr", arr)

    start_position = [vacuum_position // num_cols , vacuum_position % num_cols]

    matrix = [arr[i * num_cols:(i + 1) * num_cols] for i in range(num_rows)]

    return {
        'matrix': matrix,
        'start_position': start_position
    }

def create_table():
    global num_cols,num_rows,num_obs,num_dust,table_frame,result,vacuum_pos,dust_positions, kt
    kt = 0
    num_rows = row_entry.get()
    num_cols = column_entry.get()
    # Get the number of obstacles
    num_obs =  obstacle_entry.get()
    # Get the number of dust
    num_dust = dust_entry.get()

    if not num_rows or not num_cols or not num_obs or not num_dust:
        messagebox.showerror("Error message", "Please enter complete row, column, dust quantity and obstacle quantity information!")
        return
    num_rows = int(num_rows)
    num_cols = int(num_cols)
    num_obs = int(num_obs)
    num_dust = int(num_dust)

    result = random_matrix(num_rows, num_cols, num_obs, num_dust)
    print("result", result)
    obstacle_positions = {(i, j) for i in range(num_rows) for j in range(num_cols) if result['matrix'][i][j] == 1}
    dust_positions = {(i, j) for i in range(num_rows) for j in range(num_cols) if result['matrix'][i][j] == 2}
    # Get the vacuum position
    vacuum_pos = result['start_position']
    if table_frame:
        clear_table()

    table_frame = ctk.CTkFrame(window)
    table_frame.grid(row=0, column=2, columnspan=2)

    global vacuum_image, bg_image, dust_image, wall_image, visited_image
    global size_image
    screen_height = window.winfo_screenheight()
    screen_width = window.winfo_screenwidth()
    size_image = min(screen_height // num_rows, (screen_width / 2)  // num_cols)

    vacuum_image = CTkImage(light_image=Image.open("image\\vacuum.png"), dark_image=Image.open("image\\vacuum.png"), size=(size_image, size_image))
    bg_image = CTkImage(light_image=Image.open("image\\dust.jpg"), dark_image=Image.open("image\\dust.jpg"), size=(size_image, size_image))
    dust_image = CTkImage(light_image=Image.open("image\\virus.jpg"), dark_image=Image.open("image\\virus.jpg"), size=(size_image, size_image))
    wall_image = CTkImage(light_image=Image.open("image\\wall.jpg"), dark_image=Image.open("image\\wall.jpg"), size=(size_image, size_image))
    visited_image = CTkImage(light_image=Image.open("image\\clean.png"), dark_image=Image.open("image\\clean.png"), size=(size_image, size_image))

    for i in range(num_rows):
        for j in range(num_cols):
            if [i, j] == vacuum_pos:
                image = vacuum_image
            elif (i, j) in obstacle_positions:
                image = wall_image
            elif (i, j) in dust_positions:
                image = dust_image
            else:
                image = bg_image

            cell_label = ctk.CTkLabel(table_frame, image=image, width=size_image, height=size_image, bg_color='lightblue', text="")
            cell_label._image = image
            cell_label.grid(row=i, column=j, padx=1, pady=1)
            cell_label.bind('<Button-1>', lambda onRightClick, row=i, col=j: update_vacuum_position(row, col))
            cell_label.bind('<Button-2>', lambda onRightClick, row=i, col=j: up_wall(row, col))
            cell_label.bind('<Button-3>', lambda onRightClick, row=i, col=j: up_virus(row, col))

def update_cell(row, col, image):
    # Find the corresponding Label widget and update the image
    cell_label = table_frame.grid_slaves(row=row, column=col)[0]
    cell_label.configure(image=image)


def up_wall(r, c):
    global table_frame
    result['matrix'][r][c] = 1
    new_label = ctk.CTkLabel(table_frame, image=wall_image, width=size_image, height=size_image, bg_color='lightblue', text="")

    new_label.grid(row=r, column=c, padx=1, pady=1)

def up_virus(r, c):
    global table_frame, dust_image
    result['matrix'][r][c] = 2
    new_label = ctk.CTkLabel(table_frame, image=dust_image, width=size_image, height=size_image, bg_color='lightblue', text="")

    new_label.grid(row=r, column=c, padx=1, pady=1)

def update_vacuum_position(new_row, new_col):
    global  result
    update_cell( result['start_position'][0], result['start_position'][1], bg_image)
    result['start_position'][0] = new_row
    result['start_position'][1] = new_col
    # update the value of clean cell
    result['matrix'][new_row][new_col] = 0
    update_cell( result['start_position'][0], result['start_position'][1], vacuum_image)

def move_vacuum(old_x, old_y, new_x, new_y):
    global vacuum_pos

    vacuum_pos = (new_x, new_y)
    # Update the cell at the old position to the background image
    update_cell(old_x, old_y, visited_image)
    update_cell(new_x, new_y, vacuum_image)

def clear_table():
    global table_frame
    # Check if the table_frame has been created, then delete the widgets in the Frame
    if table_frame:
        for widget in table_frame.winfo_children():
            if widget != submit_button:
                widget.destroy()

def clean_grid():
    global vacuum_pos, num_rows, num_cols, result, table_frame, kt
    kt = 1
    dust_positions = [(i, j) for i in range(num_rows) for j in range(num_cols) if result['matrix'][i][j] == 2]
    print("dust_positions", dust_positions)

    num_speed = max(num_rows, num_cols)
    num_speed = num_speed ** 1.3

    vacuum_pos = result['start_position']
    path = find_path_to_closest_goal(result['matrix'], (vacuum_pos[0], vacuum_pos[1])  , dust_positions)
    print("path", path)
    # Follow the path to clean the dust
    for step in path:
        move_vacuum(vacuum_pos[0], vacuum_pos[1], step[0], step[1])
        window.update()
        time.sleep(2 / num_speed)
        if(kt == 0):
            return None
    # Update the last vacuum position
    # vacuum_pos = {'x': path[-1][0], 'y': path[-1][1]}
    # print("vacuum_pos", vacuum_pos)
    # Ensure the vacuum is at the last position
    # move_vacuum(vacuum_pos['x'], vacuum_pos['y'], vacuum_pos['x'], vacuum_pos['y'])



def start_cleaning_A_star():
    print("Start Cleaning A")
    clean_grid()


def run_application():
    print("Start Application")
    global row_entry, column_entry, obstacle_entry, dust_entry, window, submit_button, kt
    kt = 0
    
    window = ctk.CTk()
    window.title("Thông tin")


    window1 = ctk.CTkFrame(window)
    window1.grid(row=0, column=0, columnspan=2, ipadx=30, padx = 20, sticky="nsew")
    info_frame = ctk.CTkLabel(window1, text="", font=("Arial", 12, "bold"))
    info_frame.grid(row=0, column=1, pady = 20)

    label_font = CTkFont(family="Arial", size=14)

    column_label = ctk.CTkLabel(info_frame, text="Enter the number of column:", font=label_font)
    column_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    column_entry = ctk.CTkEntry(info_frame, font=label_font)
    column_entry.grid(row=0, column=1, padx=10, pady=10)

    row_label = ctk.CTkLabel(info_frame, text="Enter the number of row:", font=label_font)
    row_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    row_entry = ctk.CTkEntry(info_frame, font=label_font)
    row_entry.grid(row=1, column=1, padx=10, pady=10)

    obstacle_label = ctk.CTkLabel(info_frame, text="Enter the number of obstacle:", font=label_font)
    obstacle_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    obstacle_entry = ctk.CTkEntry(info_frame, font=label_font)
    obstacle_entry.grid(row=2, column=1, padx=10, pady=10)

    dust_row_label = ctk.CTkLabel(info_frame, text="Enter the number of dust:", font=label_font)
    dust_row_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    dust_entry = ctk.CTkEntry(info_frame, font=label_font)
    dust_entry.grid(row=3, column=1, padx=10, pady=10)

    submit_button = ctk.CTkButton(window1, text="Submit", font= label_font, command=create_table)
    #submit_button.pack(pady=10)
    # Set the weight for each row and column that contains a widget
    for i in range(12):  # Assuming have 12 rows
        window1.grid_rowconfigure(i, weight=1)
    for i in range(2):  # Assuming have 2 columns
        window1.grid_columnconfigure(i, weight=1)

    submit_button.grid(row=10, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
    start_cleaning_A_star_button = ctk.CTkButton(window1, text="Start Cleaning A*",command=start_cleaning_A_star, font=label_font)
    start_cleaning_A_star_button.grid(row=11, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

    window1.grid_rowconfigure(0, weight=1)
    window1.grid_rowconfigure(6, weight=1)

    window.mainloop()

run_application()