import copy
#Board is a n*n character list of lists(2D list)
p1_symbol = 'X'
p2_symbol = 'O'
empty_symbol = 'e'


#Return the maximum difference for both players across all rows 
#i.e, if a row has full p2_symbols maximum abs diff is n, but we must return -n to differentiate it from row of p1_symbols 
def row_check_S(state):
    #ROW CHECK
    n= len(state)
    p1_diff = 0
    p2_diff = 0
    for i in range(n):
        p1_count = 0
        p2_count = 0
        for j in range(n):
            p1_count+=state[i][j]==p1_symbol
            p2_count+=state[i][j]==p2_symbol
        diff = p1_count - p2_count
        p1_diff = max(p1_diff, diff)
        p2_diff = max(p2_diff, -diff)
    return (p1_diff, p2_diff)
    

#Return the maximum difference for both players across all columns    
def column_check_S(state):
    n = len(state)
    #COLUMN CHECK
    p1_diff = 0
    p2_diff = 0
    for i in range(n):
        p1_count = 0
        p2_count = 0
        for j in range(n):
            p1_count+=state[j][i]==p1_symbol
            p2_count+=state[j][i]==p2_symbol
        diff = p1_count - p2_count
        p1_diff = max(p1_diff, diff)
        p2_diff = max(p2_diff, -diff)
    return (p1_diff, p2_diff)


#Return the maximum difference for both players across 2 key diags
def diagonal_check_S(state):
    #Diagonal Check(we only need to check the 2 principal diagonals as everything else won't give a sum of n)
    n = len(state)
    p2_count = 0
    p1_count = 0
    p1_diff = 0
    p2_diff = 0
    for j in range(n):
        p1_count+=state[j][j]==p1_symbol
        p2_count+=state[j][j]==p2_symbol
    diff = p1_count - p2_count
    p1_diff = max(p1_diff, diff)
    p2_diff = max(p2_diff, -diff)
    p1_count = 0
    p2_count = 0
    for j in range(n):
        p1_count+=state[-1-j][j]==p1_symbol
        p2_count+=state[-1-j][j]==p2_symbol
    diff = p1_count - p2_count
    p1_diff = max(p1_diff, diff)
    p2_diff = max(p2_diff, -diff)
    return (p1_diff, p2_diff)


#Assumption: RETURN +1 if p1 wins, -1 if p2 wins and 0 if no one has one yet
# (based on this plus the number of e's in board we can figure out if its a draw)
def check_gameover_S(state):
    n = len(state)
    #ROW CHECK
    ret1, ret2 = row_check_S(state)
    if ret1==n:
        return 1
    if ret2==n:
        return -1
    #Column Check
    ret1, ret2 = column_check_S(state)
    if ret1==n:
        return 1
    if ret2==n:
        return -1
    #Diagonal Check
    ret1, ret2 = diagonal_check_S(state)
    if ret1==n:
        return 1
    if ret2==n:
        return -1
    return 0
    #If none of the three are matched, we return 0 to indicate no one has won(yet)


def static_eval_fn_D(state):
    max1 = -2
    max2 = 2
    ret1, ret2 = row_check_S(state)
    max1 = max(max1, ret1)
    max2 = max(max2, ret2)
    ret1, ret2 = column_check_S(state)
    max1 = max(max1, ret1)
    max2 = max(max2, ret2)
    ret1, ret2 = diagonal_check_S(state)
    max1 = max(max1, ret1)
    max2 = max(max2, ret2)
    return (max1,max2)

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



#is_over : minimax value, minimax: path/child to be chosen
class state_D():

    def __init__(self, state,is_max):
        self.is_over=check_gameover_S(state)
        self.state = state
        self.children = []
        self.minimax= None
        self.is_max= is_max

    def add_children(self, children):
        self.children= children



def build_tree_D(root,depth,is_max):
    n = len(root.state)
    q = [root]
    cur_depth = 0
    keep_going = True
    while(cur_depth < depth and keep_going):
        size=len(q)
        print("Size of queue: ", size,"    Is p1:", is_max,"    Current Depth: ",  cur_depth)
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
        cur_depth+=1
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


#Helper function to sefd
def eval_D(is_max, max1,max2):
    if is_max:
        if(max1>=max2):
            return 1
        elif max1 == max2 - 1:
            return 0
        return -1
    if(max1>max2):
        return 1
    elif max1 == max2:
        return 0
    return -1

#K-depth approximation to the minimax approach using a static evaluation function
def K_depth_S(root,depth,k):
    if len(root.children)==0: 
        # root.minimax = root.is_over ##We have changed the meaning of minimax, now it represents the path
        # print(root.state, root.is_over)
        # if(root.is_over==-1):
        #     print(root.is_over)
        return root
    if depth==k:
        max1, max2 = static_eval_fn_D(root.state)
        root.is_over = eval_D(root.is_max,max1,max2)
        return root
    mini=root.children[0]
    maxi=root.children[0]
    for child in root.children:
        v = K_depth_S(child,depth+1, k)
        # print(type(v))
        if(mini.is_over > v.is_over):
            mini = v
        if(maxi.is_over < v.is_over):
            maxi = v
    if root.is_max:
        root.minimax=maxi
        root.is_over = maxi.is_over
        # print(root.state, root.minimax, p1_symbol)
        return root
    root.minimax=mini
    root.is_over = mini.is_over
    # print(root.state, root.minimax, p2_symbol)
    return root

def tuple_it_D(state):
    return tuple(map(tuple, state))

def print_board(state):
    n = len(state)
    print("")
    for i in range(n):
        print(state[i])
    print("")


if __name__=='__main__':
    depth = int(input("Enter max depth upto which u wanna search/build tree: "))
    n = int(input("Enter the size of the tic tac toe board(n): "))
    start = state_init_S(n)
    # start = [['O', 'e', 'e'], ['e','e','e'],  ['e','e','e']]
    s0 = state_D(start, True)
    counte = 0
    s_map = {tuple_it_D(start): s0}
    root = build_tree_D(s0,depth, is_max=True)
    K_depth_S(root,0,depth)
    # print("Minimax result for p1: ", minimax_S(root),"   Number of duplicate nodes avoided:", counte,"   Number of nodes in map:",len(s_map))
    print("K depth result is: ", root.is_over,"   Number of duplicate nodes avoided:", counte,"   Number of nodes in map:",len(s_map))
    it = root
    while(it.minimax is not None):
        print_board(it.state)
        print("")
        it = it.minimax
