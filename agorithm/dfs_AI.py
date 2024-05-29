import time

def check(r, c):
    global table, num_cols, num_rows
    if(r < 0 or r == num_rows or c < 0 or c == num_cols):
        return False
    if(table[r][c] == '.'):
        return True
    else:
        return False

def move(r, c):       
    global que, dus, table, near
    if(r == dus[0] and c == dus[1]):
        step.append([r, c])
        return True
    for i in near:
        if(check(r + i[0], c + i[1])):
            table[r + i[0]][c + i[1]] = 'S'     
            if(move(r + i[0], c + i[1])):
                step.append([r, c])
                return True
    return False
        
      
def initialize_dfs(ta, st, dust):
    global row, col, num_cols, num_rows, table, step, near, mark, que, dus
    dus = dust
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
    que = []
    # que.append([row, col, -1])
    move(row, col)
    # print_table()
    step.reverse()
    return step