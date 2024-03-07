import copy
#Board is a 3*3 character list
p1_symbol = 'X'
p2_symbol = 'O'
empty_symbol = 'e'
def check_gameover_S(state):
    #ROW CHECK
    n= len(state)
    for i in range(n):
        p1_count = 0
        p2_count = 0
        for j in range(n):
            p1_count+=state[i][j]==p1_symbol
            p2_count+=state[i][j]==p2_symbol
        if p2_count==(n):
            return -1
        if p1_count==(n):
            return 1
        #COLUMN CHECK
    for i in range(n):
        p1_count = 0
        p2_count = 0
        for j in range(n):
            p1_count+=state[j][i]==p1_symbol
            p2_count+=state[j][i]==p2_symbol
        if p2_count==n:
            return -1
        if p1_count==n:
            return 1
    p1_count=0
    p2_count=0
    for j in range(n):
            p1_count+=state[j][j]==p1_symbol
            p2_count+=state[j][j]==p2_symbol
            if p2_count==n:
                return -1
            if p1_count==n:
                return 1
    p1_count = 0
    p2_count = 0
    for j in range(n):
            p1_count+=state[n-1-j][j]==p1_symbol
            p2_count+=state[n-1-j][j]==p2_symbol
            if p2_count==n:
                return -1
            if p1_count==n:
                return 1
    return 0

def state_init_S(n):
    state=[]
    for i in range(n):
        row = []
        for j in range(n):
            row.append(empty_symbol)
        state.append(row)
    return state

def next_states_S(pres_state, is_max):
    next_states=[]
    n=len(pres_state)
    symbol=empty_symbol
    if is_max:
        symbol=p1_symbol
    else:
        symbol=p2_symbol
    
    for i in range(n):
        for j in range(n):
            if pres_state[i][j]==empty_symbol:
                pres_state[i][j]=symbol
                # print(pres_state)
                dup = copy.deepcopy(pres_state)
                next_states.append(state_D(dup, is_max))
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
    while(depth < n*n):
        size=len(q)
        print(size, is_max)
        for i in range(size):
            node=q[0]
            # print("start " , node.state)
            if node.is_over==0:
                children = next_states_S(node.state,is_max)
                node.add_children(children)
                for child in children:
                    # print(child.state)
                    q.append(child)
                q.pop(0)
        depth+=1
        is_max = not is_max
    return root

def minimax_S(root):
    if len(root.children)==0:
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
    if root.is_max:
        root.minimax=maxi
        return maxi
    root.minimax=mini
    return mini


if __name__=='__main__':
    start = state_init_S(3)
    s0 = state_D(start, True)
    root = build_tree_D(s0,depth=0, is_max=True)
    print(minimax_S(root))