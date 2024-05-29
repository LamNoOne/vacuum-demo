import time

def check(r, c):
    global table, num_cols, num_rows
    if(r < 0 or r == num_rows or c < 0 or c == num_cols):
        return False
    if(table[r][c] == '.'):
        return True
    else:
        return False
    

def print_table():
    global table
    print()
    for i in table:
        print(*i)

def move(r, c):
    global near, table, mark, step
    step.append([r, c])
    j = 0
    for i in near:
        if(check(r + i[0], c + i[1])):
            table[r + i[0]][c + i[1]] = mark[j]
            move(r + i[0], c + i[1])
            table[r + i[0]][c + i[1]] = mark[(j + 2) % 4]

            step.append([r, c])
        j += 1
      
def initialize_D(ta, st):
    global row, col, num_cols, num_rows, table, step, near, mark
    row = st[0]
    col = st[1]
    num_rows = len(ta)
    num_cols = len(ta[0])
    step = []
    near = [[1, 0], [0, 1], [-1, 0], [0, -1]]
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
        
    move(row, col)
    # print_table()
    return step