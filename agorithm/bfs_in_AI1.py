import time

def check(r, c, tabl):
    global num_cols, num_rows
    if(r < 0 or r == num_rows or c < 0 or c == num_cols):
        return False
    if(tabl[r][c] == '.'):
        return True
    else:
        return False

def ste(que1):
    global step
    st = []
    # print(que)
    st.append([que1[-1][0], que1[-1][1]])
    k = que1[-1][2]
    while(k != -1):
        st.append([que1[k][0], que1[k][1]])
        k = que1[k][2]
    st.reverse()
    print(st)
    for i in st:
        step.append(i)
    

def move(sta, dus):
    global table, near
    tabl = []
    que1 = []
    que1.append([sta[0], sta[1], -1])
    for i in table:
        tmp = []
        for j in i:
            tmp.append(j)
        tabl.append(tmp)
    p = 0
    k = 0
    while(p <= k):
        a = [que1[p][0], que1[p][1]]
        for i in near:
            if(check(a[0] + i[0], a[1] + i[1], tabl)):
                k += 1
                que1.append([a[0] + i[0], a[1] + i[1], p])
                tabl[a[0] + i[0]][a[1] + i[1]] = 'S'
                if(que1[k][0] == dus[0] and que1[k][1] == dus[1]):
                    ste(que1)
                    return None
        p += 1
        
      
def initialize_B1(ta, st):
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
    for i in range(0, num_rows):
        for j in range(0, num_cols):
            print([i,j])
            if(table[i][j] != 'X'):
                move(st, [i, j])
                st = [i, j]
    # print_table()
    # step.reverse()
    # print(step)
    return step