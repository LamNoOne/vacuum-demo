import time

def check(r, c):
    global table, num_cols, num_rows, que
    if(r < 0 or r == num_rows or c < 0 or c == num_cols):
        return False
    if(table[r][c] == '.'):
        return True
    else:
        return False

def move(r, c):       
    global que, dus, table, near
    if(r == dus[0] and c == dus[1]):
        que[r][c] = [-1, -1, 0]
        return None
    for i in near:
        if(check(r + i[0], c + i[1])):
            table[r + i[0]][c + i[1]] = 'S'     
            move(r + i[0], c + i[1])
        if(r + i[0] >= 0 and r + i[0] < num_rows and c + i[1] >= 0 and c + i[1] < num_cols):
            if(que[r + i[0]][c + i[1]][2] < que[r][c][2]):
                que[r][c] = [r + i[0], c + i[1], que[r+i[0]][c+i[1]][2] + 1]
        
      
def initialize_dfs1(ta, st, dust):
    global row, col, num_cols, num_rows, table, step, near, que, dus
    dus = dust
    row = st[0]
    col = st[1]
    num_rows = len(ta)
    num_cols = len(ta[0])
    step = []
    near = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    table = []
    que = []
    for i in ta:
        tmp = []
        tmp1 = []
        for j in i:
            tmp1.append([-1, -1, 100000])
            if(j == 1):
                tmp.append('X')
            else:
                tmp.append('.')
        table.append(tmp)
        que.append(tmp1)
    step.append([row, col])
    move(row, col)
    k = [row, col, 1]
    while k[2] != 0:
        step.append([k[0], k[1]])
        k = que[k[0]][k[1]]
    # print_table()
    # step.reverse()
    return step