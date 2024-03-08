import copy
#Board is a n*n character list of lists(2D list)
p1_symbol = 'X'
p2_symbol = 'O'
empty_symbol = 'e'

# def row_check_S(state):
#     #ROW CHECK
#     n= len(state)
#     for i in range(n):
#         p1_count = 0
#         p2_count = 0
#         for j in range(n):
#             p1_count+=state[i][j]==p1_symbol
#             p2_count+=state[i][j]==p2_symbol
#         if p2_count==(n):
#             return -1
#         if p1_count==(n):
#             return 1
#     return 0
    
# def column_check_S(state):
#     n = len(state)
#     #COLUMN CHECK
#     for i in range(n):
#         p1_count = 0
#         p2_count = 0
#         for j in range(n):
#             p1_count+=state[j][i]==p1_symbol
#             p2_count+=state[j][i]==p2_symbol
#         if p2_count==n:
#             return -1
#         if p1_count==n:
#             return 1
#     return 0

# def diagonal_check_S(state):
#     #Diagonal Check(we only need to check the 2 principal diagonals as everything else won't give a sum of n)
#     n = len(state)
#     p2_count = 0
#     p1_count = 0
#     for j in range(n):
#             p1_count+=state[j][j]==p1_symbol
#             p2_count+=state[j][j]==p2_symbol
#     if p2_count==n:
#         return -1
#     if p1_count==n:
#         return 1
#     p1_count = 0
#     p2_count = 0
#     for j in range(n):
#             p1_count+=state[-1-j][j]==p1_symbol
#             p2_count+=state[-1-j][j]==p2_symbol
#     if p2_count==n:
#         return -1
#     if p1_count==n:
#         return 1
#     return 0
# def check_gameover_S(state):
#     #ROW CHECK
#     ret = row_check_S(state)
#     if ret:
#         return ret
#     #Column Check
#     ret = column_check_S(state)
#     if ret:
#         return ret
#     #Diagonal Check
#     return diagonal_check_S(state)
#     #If none of the three are matched, we return 0 to indicate no one has won(yet)


#Return the actual difference of the maximum absolute difference b/w p1_symbols and p2_symbols across all rows 
#i.e, if a row has full p2_symbols maximum abs diff is n, but we must return -n to differentiate it from row of p1_symbols 
def row_check_S(state):
    #ROW CHECK
    n= len(state)
    diff = 0
    for i in range(n):
        p1_count = 0
        p2_count = 0
        for j in range(n):
            p1_count+=state[i][j]==p1_symbol
            p2_count+=state[i][j]==p2_symbol
        if(abs(p1_count-p2_count) > abs(diff)):
            diff = p1_count - p2_count
        if abs(diff)==(n):
            return diff
    return diff
    

#Return the actual diff of maximum absolute difference b/w p1_symbols and p2_symbols across all columns    
def column_check_S(state):
    n = len(state)
    #COLUMN CHECK
    diff = 0
    for i in range(n):
        p1_count = 0
        p2_count = 0
        for j in range(n):
            p1_count+=state[j][i]==p1_symbol
            p2_count+=state[j][i]==p2_symbol
        if(abs(p1_count-p2_count) > abs(diff)):
            diff = p1_count - p2_count
        if abs(diff)==(n):
            return diff
    return diff


#Return the actual diff of maximum absolute difference b/w p1_symbols and p2_symbols across 2 key diags
def diagonal_check_S(state):
    #Diagonal Check(we only need to check the 2 principal diagonals as everything else won't give a sum of n)
    n = len(state)
    p2_count = 0
    p1_count = 0
    diff = 0
    for j in range(n):
        p1_count+=state[j][j]==p1_symbol
        p2_count+=state[j][j]==p2_symbol
    if(abs(p1_count-p2_count) > abs(diff)):
        diff = p1_count - p2_count
    if abs(diff)==(n):
        return diff
    p1_count = 0
    p2_count = 0
    for j in range(n):
        p1_count+=state[-1-j][j]==p1_symbol
        p2_count+=state[-1-j][j]==p2_symbol
    if(abs(p1_count-p2_count) > abs(diff)):
        diff = p1_count - p2_count
    if abs(diff)==(n):
        return diff
    return diff


#Assumption: RETURN +1 if p1 wins, -1 if p2 wins and 0 if no one has one yet
# (based on this plus the number of e's in board we can figure out if its a draw)
def check_gameover_S(state):
    n = len(state)
    #ROW CHECK
    ret = row_check_S(state)
    if abs(ret)==n:
        return ret//abs(ret)
    #Column Check
    ret = column_check_S(state)
    if abs(ret)==n:
        return ret//abs(ret)
    #Diagonal Check
    ret = diagonal_check_S(state)
    if abs(ret)==n:
        return ret//abs(ret)
    return 0
    #If none of the three are matched, we return 0 to indicate no one has won(yet)

def state_init_S(n):
    state=[]
    for i in range(n):
        row = []
        for j in range(n):
            row.append(empty_symbol)
        state.append(row)
    return state

#Now we're updating it to ensure multiple nodes are not created for the same state by adding a dictionary
def next_states_S(pres_state, is_max):
    next_states=[]
    n=len(pres_state)
    symbol=empty_symbol
    if is_max:
        symbol=p1_symbol
    else:
        symbol=p2_symbol
    children_player = not is_max
    for i in range(n):
        for j in range(n):
            if pres_state[i][j]==empty_symbol:
                pres_state[i][j]=symbol
                # print(pres_state)
                dup = copy.deepcopy(pres_state)
                dup_tup = tuple_it_D(dup)
                if dup_tup in s_map:
                    global counte
                    counte+=1
                    # print(1)
                    next_states.append(s_map[dup_tup])
                else:
                    child=  state_D(dup, children_player)
                    s_map[dup_tup] = child
                    next_states.append(child)
                # print(" after: ", pres_state)
                pres_state[i][j]=empty_symbol
    return next_states




class state_D():

    def __init__(self, state,is_max):
        self.is_over=check_gameover_S(state)
        self.state = state
        self.children = []
        self.minimax=6
        self.is_max= is_max

    def add_children(self, children):
        self.children= children



def build_tree_D(root,depth, is_max):
    n = len(root.state)
    q = [root]
    keep_going = True
    while(depth < n*n and keep_going):
        size=len(q)
        print(size, is_max, depth)
        keep_going = False
        for i in range(size):
            node=q[0]
            q.pop(0)
            # print("start " , node.state)
            if node.is_over==0:
                keep_going = True
                children = next_states_S(node.state, is_max)
                node.add_children(children)
                for child in children:
                    # print(child.state, child.is_max)
                    q.append(child)
        depth+=1
        is_max = not is_max
    return root

def minimax_S(root):
    if len(root.children)==0:
        root.minimax = root.is_over
        # print(root.state, root.is_over)
        # if(root.is_over==-1):
        #     print(root.is_over)
        return root.is_over
    mini=10
    maxi=-3
    for child in root.children:
        v = minimax_S(child)
        # print(type(v))
        if(mini > v):
            mini = v
        if(maxi < v):
            maxi = v
    if root.is_max ==True:
        root.minimax=maxi
        # print(root.state, root.minimax, p1_symbol)
        return maxi
    root.minimax=mini
    # print(root.state, root.minimax, p2_symbol)
    return mini

def tuple_it_D(state):
    return tuple(map(tuple, state))
if __name__=='__main__':
    start = state_init_S(3)
    # start = [['O', 'e', 'e'], ['e','e','e'],  ['e','e','e']]
    s0 = state_D(start, True)
    counte = 0
    s_map = {tuple_it_D(start): s0}
    root = build_tree_D(s0,depth=0, is_max=True)
    print(minimax_S(root), counte)
