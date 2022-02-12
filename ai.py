import model
import pickle
from time import perf_counter_ns

NANO_TO_SEC = 1000000000
INF = 100000
groups = []
patternDbDict = []

def init(boardSize):
    global groups
    global patternDbDict
    print("Initializing pattern DB...")
    with open("patternDb_"+str(boardSize)+".dat", "rb") as patternDbFile:
        groups = pickle.load(patternDbFile)
        patternDbDict = pickle.load(patternDbFile)
        for i in range(len(patternDbDict)):
            print("Group {}: {}, {:,} entries.".format(i,groups[i],len(patternDbDict[i])))

def idaStar(puzzle):
    if  puzzle.checkWin():
        return []
    if not patternDbDict:
        init(puzzle.boardSize)

    t1 = perf_counter_ns()
    bound = hScore(puzzle)
    path = [puzzle]
    dirs = []
    while True:
        rem = search(path, 0, bound, dirs)
        if rem == True:
            tDelta = (perf_counter_ns()-t1)/NANO_TO_SEC
            print("Took {} seconds to find a solution of {} moves".format(tDelta, len(dirs)))
            return dirs
        elif rem == INF:
            return None
        bound = rem
def search(path, g, bound, dirs):
    cur = path[-1]
    f = g + hScore(cur)

    if f > bound:
        return f

    if cur.checkWin():
        return True
    min = INF

    for dir in cur.DIRECTIONS:
        if dirs and (-dir[0], -dir[1]) == dirs[-1]:
            continue
        validMove, simPuzzle = cur.simulateMove(dir)

        if not validMove or simPuzzle in path:
            continue

        path.append(simPuzzle)
        dirs.append(dir)

        t = search(path, g + 1, bound, dirs)
        if t == True:
            return True
        if t < min:
            min = t

        path.pop()
        dirs.pop()

    return min

def hScore(puzzle):
    h = 0
    for g in range(len(groups)):
        group = groups[g]
        hashString = puzzle.hash(group)
        if hashString in patternDbDict[g]:
            h += patternDbDict[g][hashString]
        else:
            print("No pattern found in DB, using manhattan dist")
            for i in range(puzzle.boardSize):
                for j in range(puzzle.boardSize):
                    if puzzle[i][j] != 0 and puzzle[i][j] in group:
                        destPos = ((puzzle[i][j] - 1) // puzzle.boardSize,
                                     (puzzle[i][j] - 1) % puzzle.boardSize)
                        h += abs(destPos[0] - i)
                        h += abs(destPos[1] - j)

    return h
