from collections import Counter
import random
import math

random.seed()


def initBoard(empty=False):
    if not empty:
        initString = input('Enter cells: ').replace('_', ' ')
    else:
        initString = ' ' * 9
    board = [['']*3 for n in range(3)]
    symbolCounts = Counter(initString)

    for i in range(3):
        for j in range(3):
            board[i][j] = initString[i*3 + j]

    return board, symbolCounts


def printBoard(board):
    print('---------')
    for line in board:
        print('| {} |'.format(' '.join(line)))
    print('---------')


def getPlayerMove(board, symbolCounts):
    validMove = False
    while not validMove:
        tokens = input('Enter the coordinates: ').split()

        if False in [i.isdigit() for i in tokens]:
            print('You should enter numbers!')
        elif len(tokens) == 2:
            row = int(tokens[0]) - 1
            col = int(tokens[1]) - 1
            if 0 <= row <= 2 and 0 <= col <= 2:
                if board[row][col] == ' ':
                    validMove = True
                else:
                    print('This cell is occupied! Choose another one!')
            else:
                print('Coordinates should be from 1 to 3!')
        else:
            print("Error")
            continue

    nextSymbol = 'X' if symbolCounts['X'] == symbolCounts['O'] else 'O'
    board[row][col] = nextSymbol
    symbolCounts[nextSymbol] += 1
    symbolCounts[' '] -= 1

    return board, symbolCounts


# Returns False if the game is over, True if not
# Or returns 2 for draw, 1 for won, 0 for no result
def checkBoardState(board, symbolCounts, shouldPrint=True):
    lastSymbol = 'O' if symbolCounts['X'] == symbolCounts['O'] else 'X'

    if symbolCounts[' '] == 0:
        if shouldPrint:
            print('Draw')
            return False
        else:
            return 2

    for i in range(3):
        #Row check
        if Counter(board[i])[lastSymbol] == 3:
            if shouldPrint:
                print(f'{lastSymbol} wins')
                return False
            else:
                return 1

        #Col check
        if Counter([board[j][i] for j in range(3)])[lastSymbol] == 3:
            if shouldPrint:
                print(f'{lastSymbol} wins')
                return False
            else:
                return 1

    if Counter([board[i][i] for i in range(3)])[lastSymbol] == 3 or \
            Counter([board[i][2-i] for i in range(3)])[lastSymbol] == 3:
        if shouldPrint:
            print(f'{lastSymbol} wins')
            return False
        else:
            return 1

    return True if shouldPrint else 0


def findWinBlock(board, nextSymbol):
    #Find a win
    for i in range(3):
        #Row check
        if Counter(board[i])[nextSymbol] == 2 and ' ' in board[i]:
            return i, board[i].index(' ')

        #Col check
        thisCol = [board[j][i] for j in range(3)]
        if Counter(thisCol)[nextSymbol] == 2 and ' ' in thisCol:
            return thisCol.index(' '), i

    dia1 = [board[i][i] for i in range(3)]
    dia2 = [board[i][2-i] for i in range(3)]

    if Counter(dia1)[nextSymbol] == 2 and ' ' in dia1:
        return dia1.index(' '), dia1.index(' ')

    if Counter(dia2)[nextSymbol] == 2 and ' ' in dia2:
        return dia2.index(' '), 2-dia2.index(' ')

    #Find a block
    nextSymbol = 'O' if nextSymbol == 'X' else 'X'
    for i in range(3):
        #Row check
        if Counter(board[i])[nextSymbol] == 2 and ' ' in board[i]:
            return i, board[i].index(' ')

        #Col check
        thisCol = [board[j][i] for j in range(3)]
        if Counter(thisCol)[nextSymbol] == 2 and ' ' in thisCol:
            return thisCol.index(' '), i

    if Counter(dia1)[nextSymbol] == 2 and ' ' in dia1:
        return dia1.index(' '), dia1.index(' ')

    if Counter(dia2)[nextSymbol] == 2 and ' ' in dia2:
        return dia2.index(' '), 2-dia2.index(' ')

    return -1, -1


def minimax(board, maxingSymbol, isMaxTurn):
    options = [(row, col) for row in range(3) for col in range(3) if board[row][col] == ' ']
    symbolCounts = Counter(''.join(''.join(i) for i in board))
    lastSymbol = 'O' if symbolCounts['X'] == symbolCounts['O'] else 'X'
    nextSymbol = 'X' if symbolCounts['X'] == symbolCounts['O'] else 'O'

    state = checkBoardState(board,  symbolCounts, False)
    # Terminal state
    if state:
        if lastSymbol == maxingSymbol and state == 1:
            return 1 #win
        elif lastSymbol != maxingSymbol and state == 1:
            return -1 #loss
        else:
            return 0 #Draw

    scores = []
    for row, col in options:
        board[row][col] = nextSymbol
        scores.append(minimax(board, maxingSymbol, not isMaxTurn))
        board[row][col] = ' '

    return max(scores) if isMaxTurn else min(scores)


def getCompMove(board, symbolCounts, level):
    options = [(row, col) for row in range(3) for col in range(3) if board[row][col] == ' ']
    nextSymbol = 'X' if symbolCounts['X'] == symbolCounts['O'] else 'O'

    if level == 1:
        print('Making move level "easy"')
        row, col = random.choice(options)
        board[row][col] = nextSymbol
        symbolCounts[nextSymbol] += 1
        symbolCounts[' '] -= 1
    elif level == 2:
        print('Making move level "medium"')
        row, col = findWinBlock(board, nextSymbol)
        if row == -1:
            row, col = random.choice(options)

        board[row][col] = nextSymbol
        symbolCounts[nextSymbol] += 1
        symbolCounts[' '] -= 1
    elif level == 3:
        print('Making move level "hard"')
        row, col = findWinBlock(board, nextSymbol)
        if not row == -1:
            board[row][col] = nextSymbol
            symbolCounts[nextSymbol] += 1
            symbolCounts[' '] -= 1
        else:
            bestMove = None
            bestScore = -math.inf
            for row, col in options:
                board[row][col] = nextSymbol
                score = minimax(board, nextSymbol, False)
                board[row][col] = ' '
                if score > bestScore:
                    bestMove = (row, col)
                    bestScore = score
            row, col = bestMove
            board[row][col] = nextSymbol
            symbolCounts[nextSymbol] += 1
            symbolCounts[' '] -= 1

    return board, symbolCounts


def getMenuChoice():
    modes = {'user':0, 'easy':1, 'medium':2, 'hard':3}
    while True:
        comTokens = input('Input command: ').split()
        if len(comTokens) == 3:
            if comTokens[0] == 'start' and comTokens[1] in modes and comTokens[2] in modes:
                return modes[comTokens[1]], modes[comTokens[2]]
        elif len(comTokens) == 1:
            if comTokens[0] == 'exit':
                return -1, -1

        print('Bad parameters!')


# Main Code ###
while True:
    board, symbolCounts= initBoard(empty=True)

    xmode, omode = getMenuChoice()
    if xmode == -1:
        break

    printBoard(board)

    while checkBoardState(board, symbolCounts):

        board, symbolCounts = getPlayerMove(board, symbolCounts) if xmode == 0 \
                                                                else getCompMove(board, symbolCounts, xmode)

        printBoard(board)
        if not checkBoardState(board, symbolCounts):
            break

        board, symbolCounts = getPlayerMove(board, symbolCounts) if omode == 0 \
                                                                else getCompMove(board, symbolCounts, omode)

        printBoard(board)

