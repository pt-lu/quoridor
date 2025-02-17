path = "/Users/peterlu/Downloads/"

def BFS(adjlist, origin):
    queue = []
    visited = [origin]
    queue.append(origin)
    while queue:
        temp = queue.pop(0)
        for i in adjlist[temp]:
            if i not in visited:
                queue.append(i)
                visited.append(i)
    return visited
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

#kinda useless just do simple conversion
def hashBoard(width):
    board = {}
    temp = 0
    for i in range(width):
        for j in range(width):
            board[(i,j)] = temp
            temp += 1
    return board
#x = createBoardList(3)
#print(x)
#print(BFS(x, 0))


x = {}
x[1] = [1,2,4]
x[1].remove(4)
#print(x[1])

def PatternCount(input, pattern):
    ans = 0
    for i in range(len(input) - len(pattern) + 1):
        if input[i:i+len(pattern)] == pattern:
            ans += 1
    return ans

a = ""
b = "TGGCATATG"

def MakeMap(text, k):
    ans = {}
    for i in range(len(text) - k + 1):
        a = text[i:i+k]
        if ans.get(a) == None:
            ans[a] = 1
        else: 
            ans[a] += 1
    return ans

def GetMax(m):
    arr = m.values()
    ans = float('-inf')
    for i in arr:
        if i > ans: ans = i
    return ans

def FrequentWords(text, k):
    WordMap = MakeMap(text, k)
    ans = []
    MaxF = GetMax(WordMap)
    for i in WordMap:
        if WordMap[i] == MaxF: ans.append(i)
    return ans

a = ""
b = 14
#print(FrequentWords(a, b))

def Complement(N):
    if N == 'A': return 'T'
    if N == 'C': return 'G'
    if N == 'T': return 'A'
    if N == 'G': return 'C'

def ReverseComplement(text):
    ans = ""
    for i in range(1, len(text) + 1):
        if text[-i] == None: continue
        ans += Complement(text[-i])
    return ans
    
def FindIndex(text, pattern):
    ans = []
    for i in range(len(text) - len(pattern) + 1):
        if text[i:i+len(pattern)] == pattern:
            ans.append(i)
    return ans

a = "TGCTCCGTG"
b = ""
#print(FindIndex(b,a))



def FindClumps(text, k, L, t):
    ans = []
    for i in range(len(text)-L+1):
        window = text[i:i+L]
        mapu = MakeMap(window, k)
        for j in mapu:
            if mapu[j] >= t:
                ans.append(j)
    return set(ans)

a = ""
#print(FindClumps(a, 8, 24, 3))

def MinSkew(text):
    ans = []
    skew = [0]
    mini = 0
    for i in range(len(text)):
        temp = skew[i]
        if temp < mini: mini = temp
        if text[i] == 'C':
            skew.append(temp-1)
        elif text[i] == 'G':
            skew.append(temp+1)
        else:
            skew.append(temp)
    for i in range(len(skew)):
        if skew[i] == mini: ans.append(i)
    return ans

a = ""
#print(MinSkew(a))

def HammingDistance(p, q):
    ans = 0
    for i in range(len(p)):
        if p[i] != q[i]: ans += 1
    return ans

a = ""
b = ""
a = "t"
b = "t"
#print(HammingDistance(a,b))

def ApproxPattern(pattern, text, mismatch):
    ans = []
    for i in range(len(text)-len(pattern)+1):
        if HammingDistance(pattern, text[i:i+len(pattern)]) <= mismatch:
            ans.append(i)
    return ans

a = "CATGTGAGA"
b = ""
#print(ApproxPattern(a, b, 4))

a = "AAAAA"
b = "AACAAGCTGATAAACATTTAAAGAG"
#print(len(ApproxPattern(a, b, 2)))

def ApproxPatternCount(pattern, text, mismatch):
    ans = 0
    for i in range(len(text)-len(pattern)+1):
        if HammingDistance(pattern, text[i:i+len(pattern)]) <= mismatch:
            ans += 1
    return ans

a = "TCCGA"
b = ""
#print(ApproxPattern(a, b, 2))



def Neighbors(text, d):
    nuc = ["A", "C", "G", "T"]
    FirstSymbol = text[0]
    if d == 0: return text
    if len(text) == 1: return ["A", "C", "G", "T"]
    #nuc.remove(FirstSymbol)
    neighborhood = []
    SuffixNeighbors = Neighbors(text[1:], d)
    for i in SuffixNeighbors:
        if HammingDistance(text[1:], i) < d:
            for j in nuc:
                neighborhood.append(j + i)
        else:
            neighborhood.append(FirstSymbol + i)
    #neighborhood.append(text)
    return neighborhood


#print(Neighbors('AAA', 2))

def BetterFrequentWords(text, k, d):
    patterns = []
    freqMap = {}
    for i in range(len(text)-k):
        pattern = text[i:i+k]
        neighborhood = Neighbors(pattern, d)
        for j in neighborhood:
            if freqMap.get(j) == None:
                freqMap[j] = 1
            else: freqMap[j] += 1
    m = GetMax(freqMap)
    for i in freqMap:
        if freqMap[i] == m:
            patterns.append(i)
    return patterns

a = ""
#print(BetterFrequentWords(a, 7, 2))


TempPath = path + "aa.txt"
file1 = open(TempPath, "r")
file1.readline()
genome = file1.read()
genome = genome[:-1]
genome = genome.replace("\n", "")
nuc = ["A","C","G","T"]
#print(BetterFrequentWords(genome, 9, 3))


def SCPatternCount(input, pattern, overlap):
    ans = 0
    InPattern = False
    count = len(pattern) - overlap
    for i in range(len(input) - len(pattern) + 1):
        if InPattern == True: count -= 1
        if count == 0: 
            InPattern = False
            count = len(pattern) - overlap
        if input[i:i+len(pattern)] == pattern and not InPattern:
            InPattern = True
            ans += 1
    return ans

a = "GCGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAACGGAAGGAAGGAAGGAAGGAAGGGAAGGAAGGAAGGAAGGAAGGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAACGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAAGGAAGGAAGGAAGGAAGGAACGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAATGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGTGGAAGGAAGGAAGGAAGGAACAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAATATGCGAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAACTGGAAGGAAGGAAGGAAGGAACAGGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAAGGAACTGGAAGGAAGGAAGGAAGGAA"
b = "GGAAGGAAGGAAGGAAGGAA"
c = 3
print(SCPatternCount(a,b,c))