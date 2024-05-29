import time

def check(r, c):
    global table, num_cols, num_rows
    if(r < 0 or r == num_rows or c < 0 or c == num_cols):
        return False
    if(table[r][c] == '.'):
        return True
    else:
        return False

def ste():
    global step, que
    # print(que)
    step.append([que[-1][0], que[-1][1]])
    k = que[-1][2]
    while(k != -1):
        step.append([que[k][0], que[k][1]])
        k = que[k][2]
    

def move():
    global que, dus, table, near
    p = 0
    k = 0
    while(p <= k):
        a = [que[p][0], que[p][1]]
        for i in near:
            if(check(a[0] + i[0], a[1] + i[1])):
                k += 1
                que.append([a[0] + i[0], a[1] + i[1], p])
                table[a[0] + i[0]][a[1] + i[1]] = 'S'
                if(que[k][0] == dus[0] and que[k][1] == dus[1]):
                    ste()
                    return None
        p += 1
        
      
def initialize_bfs(ta, st, dust):
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
    que.append([row, col, -1])
    move()
    # print_table()
    step.reverse()
    # for i in range(len(step),0,-1):
    #     step.append(step[i-1])
    # print
    return step