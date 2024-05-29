import time

def check(r, c):
    global table, num_cols, num_rows
    if(r < 0 or r == num_rows or c < 0 or c == num_cols):
        return False
    if(table[r][c] == '.'):
        return True
    else:
        return False

def new_position(r, c):
    global row, col, table, stepp, prerow, precol
    prerow = row
    precol = col
    row = r
    col = c
    table[row][col] = 'S'
    if(prerow != row or precol != col):
        stepp.append([row, col])    

def bfs(step):
    global near, table, row, col, back, next
    sl = 0
    step1 = []
    for i in step:
        new_position(i[0], i[1])
        kt = 1
        for j in near:
            if(check(i[0] + j[0], i[1] + j[1])):
                new_position(i[0] + j[0], i[1] + j[1])
                sl += 1
                step1.append([row, col])
                kt = 1
            elif(kt == 1):
                # table[i[0] + j[0]][i[1] + j[1]] = 'S'
                new_position(i[0], i[1])
                step1.append([row, col])
                kt = 0
            new_position(i[0], i[1])
    # print(back + next)
    if(sl > 0):
        new_position(step1[0][0], step1[0][1])
        step1.append([step1[0][0], step1[0][1]])
        # print(step1)
        bfs(step1)
         

def initialize_B(ta, st):
    global row, col, num_cols, num_rows, table, step, near, mark, back, next, stepp, prerow, precol
    row = st[0]
    col = st[1]
    num_rows = len(ta)
    num_cols = len(ta[0])
    step = []
    # near = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    near = [[1, 0, 0], [1, 1, 1], [0, 1, 2], [-1, 1, 3], [-1, 0, 4], [-1, -1, 5], [0, -1, 6], [1, -1, 7]]
    mark = ['v', '>', '^', '<']
    table = []
    for i in ta:
        tmp = []
        for j in i:
            if(j == 1):
                tmp.append('X')
            else:
                tmp.append('.')
        table.append(tmp)
    step = [[row, col]]
    stepp = [[row, col]]
    back = []
    next = []
    next.append([step[0][0], step[0][1]])
    table[row][col] = 'S'
    bfs(step)
    return stepp

