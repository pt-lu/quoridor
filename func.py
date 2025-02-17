from collections import deque
WINCON = [490, 10]
WIDTH = 9

WINCON_IND = []
WINCON1 = []
WINCON2 = []
for i in range(9):
    WINCON1.append(i)
    WINCON2.append(WIDTH ** 2 - 1 - i)
WINCON_IND.append(WINCON1)
WINCON_IND.append(WINCON2)

"""
Function check_wincon
checks if player has reached winning condition
input:
    .pos - player's position
    .player - player's index
output:
    .win or not
"""
def check_wincon(pos, player):
    if player == 0:
        return pos[1] == WINCON[0]
    else:
        return pos[1] == WINCON[1]
    
def pos_to_ind(pos):
    func = lambda x: (x-10)//60
    return [func(x) for x in pos[:2]]
    
def wall_to_ind(wall, V):
    func = lambda x: (x-65)//60
    func1 = lambda x: (x-15)//60
    if V:
        return (func(wall[0]), func1(wall[1]))
    else:
        return (func1(wall[0]), func(wall[1]))
    
def to1D(pos):
    return pos[1] * WIDTH + pos[0]

def update_graph(graph, wall, V, player, turn):
    ind = to1D(wall)
    if V:
        graph[ind].remove(ind + 1)
        graph[ind + WIDTH].remove(ind + WIDTH + 1)
        graph[ind + 1].remove(ind)
        graph[ind + WIDTH + 1].remove(ind + WIDTH)
    else:
        graph[ind].remove(ind + WIDTH)
        graph[ind + 1].remove(ind + WIDTH + 1)
        graph[ind + WIDTH].remove(ind)
        graph[ind + WIDTH + 1].remove(ind + 1)


    if wall_block(graph, player, turn):
        if V:
            graph[ind].append(ind + 1)
            graph[ind + WIDTH].append(ind + WIDTH + 1)
            graph[ind + 1].append(ind)
            graph[ind + WIDTH + 1].append(ind + WIDTH)
        else:
            graph[ind].append(ind + WIDTH)
            graph[ind + 1].append(ind + WIDTH + 1)
            graph[ind + WIDTH].append(ind)
            graph[ind + WIDTH + 1].append(ind + 1)
        return False
    return True

def wall_block(graph, players, turn):
    p = to1D(players)
    visited = [False] * (WIDTH**2)
    

    dq = deque()

    dq.append(p)
    while dq:
        temp = dq.popleft()
        visited[temp] = True
        for i in graph[temp]:
            if not visited[i]:
                dq.append(i)
    for i in WINCON_IND[turn]:
        if visited[i]:
            return False
    return True

"""
Function convert2D
convert linear index to 2D array pair
input:
    .num - linear index
    .width - board's width/length
output:
    .2D array pair
"""
def to2D(num, width):
    return ((num-1)//width,(num-1)%width)

"""
Function convertL
convert 2D array pair to linear index
input:
    .num - 2D array pair
    .width - board's width/length
output:
    .linear index
"""
def toL(num, width):
    return num[0] * width + num[1]

"""
Function BFS
runs BFS to check if player has a path to winning condition
input:
    .adjlist - adjacency list for current board state
    .origin - player box
    .targets - top/bottom row depending on player
output:
    .whether player can reach winnin condition
"""
def BFS(adjlist, origin, targets):
    queue = []
    visited = [origin]
    queue.append(origin)
    while queue:
        temp = queue.pop(0)
        for i in adjlist[temp]:
            if i not in visited:
                queue.append(i)
                visited.append(i)
    for i in targets:
        if i not in visited: return False
    return True

"""
Function createBoardList
creates adjacency list for boards starting state
assmes board is square
input:
    .width - board's width/length
output:
    .adjacency list for board's starting state
"""
def createBoardList(width):
    total = width**2
    adjList = [[]] * (total)
    """
    3 cases:
    .node on side:
        . first (width) nodes, last (width) nodes, multiples of (width), multiples of (width) - 1
        . 3 edges
    .node on corner
        . 0, (width)-1, width^2-1, width^2-width
        . 2 edges
    .other nodes
        . 4edges
    """
    corners = [0, width-1, total-1, total-width]
    cornerCase = [[1,width],[width-2,width*2-1],[total-2,total-width-1],[total-width+1,total-width*2]]
    for i in range(len(adjList)):
        edges = [i-width, i-1, i+1, i+width]
        if i in corners:
            adjList[i] = cornerCase[corners.index(i)]
        elif i < width:
            adjList[i] = edges[1:4]
        elif i > total-width:
            adjList[i] = edges[0:3]
        elif i % width == 0:
            edges.pop(1)
            adjList[i] = edges
        elif i % width == width-1:
            edges.pop(2)
            adjList[i] = edges
        else:
            adjList[i] = edges
    return adjList

"""
Function cell
calculates cell number in player's pos or next to wall
input:
    .V - wall's orientation
    .x - wall's / player's x
    .y - wall's / player's y
output:
    cell next to wall
"""
def cell(x, y):
    return ((x-10)//60, (y-10)//60)
    
"""
Function showMoves
shows player's available moves
input:
    .G - adjacency list graph
    .x - player's x
    .y - player's y
output:
    list of available cells
"""
def showMoves(G, x, y, width):
    out = []
    for i in G[cell(x,y)]:
        out.append(to2D(i, width))
    return out

def outOfBounds(pos, min, max):
    for i in pos:
        if i < min or i > max: return True
    return False