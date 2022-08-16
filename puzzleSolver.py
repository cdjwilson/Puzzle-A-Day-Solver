from colorama import Fore, init, Back
init()
from copy import deepcopy
import time

def getEmptySpot(puzzleBoard, month, day, l):
    for i in range(len(puzzleBoard)):
        for j in range(len(puzzleBoard[i])):
            if isinstance(puzzleBoard[i][j], str) and puzzleBoard[i][j] != month and puzzleBoard[i][j] != day:
                l[0] = i
                l[1] = j
                return True
    return False

def rotatePiece(piece):
    """Rotates piece 90 degrees clockwise"""
    return [list(x) for x in list(zip(*piece[::-1]))]

def printPuzzle(puzzleBoard, month, day):
    """prints the puzzle board"""
    for i in range(len(puzzleBoard)):
        for j in range(len(puzzleBoard[i])):
            if (puzzleBoard[i][j] == month or puzzleBoard[i][j] == day):
                print(Back.BLACK + Fore.BLUE + str(puzzleBoard[i][j]), end="\t")
            elif (puzzleBoard[i][j] == 1):
                print(Back.BLACK + Fore.WHITE + str(puzzleBoard[i][j]), end="\t")
            elif (puzzleBoard[i][j] == 2):
                print(Back.BLACK + Fore.RED + str(puzzleBoard[i][j]), end="\t")
            elif (puzzleBoard[i][j] == 3):
                print(Back.BLACK + Fore.GREEN + str(puzzleBoard[i][j]), end="\t")
            elif (puzzleBoard[i][j] == 4):
                print(Back.BLACK + Fore.YELLOW + str(puzzleBoard[i][j]), end="\t")
            elif (puzzleBoard[i][j] == 5):
                print(Back.BLACK + Fore.MAGENTA + str(puzzleBoard[i][j]), end="\t")
            elif (puzzleBoard[i][j] == 6):
                print(Back.BLACK + Fore.CYAN + str(puzzleBoard[i][j]), end="\t")
            elif (puzzleBoard[i][j] == 7):
                print(Back.BLACK + Fore.LIGHTBLACK_EX + str(puzzleBoard[i][j]), end="\t")
            elif (puzzleBoard[i][j] == 8):
                print(Back.BLACK + Fore.LIGHTRED_EX + str(puzzleBoard[i][j]), end="\t")
            else: 
                print(puzzleBoard[i][j], end="\t")
        print('')

def getNextStart(piece, start):
    """gets next starting position of a piece if it exists"""
    if start == []:
        for i in range(len(piece)):
            for j in range(len(piece)):
                if piece[i][j] != 0:
                    start.append(i)
                    start.append(j)
                    return True
    
    iIndex = start[0]

    for i in range(iIndex, len(piece)):
        if i == start[0]:
            jstart = start[1]
        else:
            jstart = 0
        if (i == len(piece) - 1):
            return False
        for j in range(jstart + 1, len(piece[i])):
            if (piece[i][j] != 0):
                if (i == start[0] and j > start[1]):
                    start[0] = i
                    start[1] = j
                    return True
                elif (i > start[0]):
                    start[0] = i
                    start[1] = j
                    return True
    return False

def revertPlacedPiece(puzzleBoard, pieceNumber, l, piece):
    """takes a board and a piece and reverts any of the placed pieces on the puzzleboard"""
    for i in range(l[0], len(puzzleBoard)):
        if i == l[0]:
            jstart = l[1]
        else:
            jstart = 0
        for j in range(jstart, len(puzzleBoard[i])):
            piecelen = len(piece)
            if i >= l[0] + piecelen and j >= l[1] + piecelen:
                return False
            if puzzleBoard[i][j] == pieceNumber:
                puzzleBoard[i][j] = puzzle[i][j]
    return False

def safePlace(puzzleBoard, month, day, l, start, piece, pieceNumber):
    """place a piece with a given location in mind, check that the piece is placed in a way that makes the puzzle solvable"""
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] != 0:
                try:
                    if (i < start[0]):
                        return revertPlacedPiece(puzzleBoard, pieceNumber, l, piece)
                    elif (i > start[0]):
                        iIndex = l[0] + (abs(start[0] - i))
                    else:
                        iIndex = l[0]
                    if (j < start[1]):
                        jIndex = l[1] - (start[1] - j)
                    elif (j > start[1]):
                        jIndex = l[1] + (abs(start[1] - j))
                    else:
                        jIndex = l[1]
                    boardPiece = puzzleBoard[iIndex][jIndex]
                    if boardPiece == month or boardPiece == day or isinstance(boardPiece, int) or iIndex < 0 or jIndex < 0:
                        return revertPlacedPiece(puzzleBoard, pieceNumber, l, piece)
                    puzzleBoard[iIndex][jIndex] = piece[i][j]
                except:
                    return revertPlacedPiece(puzzleBoard, pieceNumber, l, piece)
    if hasHole(puzzleBoard, month, day, l, piece):
        return revertPlacedPiece(puzzleBoard, pieceNumber, l, piece)
    return puzzleBoard

def hasHole(puzzleBoard, month, day, l, piece):
    """Checks if there is a single square that would be impossible to fill"""
    for i in range(l[0], len(puzzleBoard)):
        if i == l[0]:
            jstart = l[1]
        else:
            jstart = 0
        for j in range(jstart, len(puzzleBoard[i])):
            piecelen = len(piece)
            if i >= l[0] + piecelen and j >= l[1] + piecelen:
                return False
            puzzlePiece = puzzleBoard[i][j]
            if isinstance(puzzlePiece, str) and puzzlePiece != month and puzzlePiece != day: 
                up, down, left, right, check = i - 1, i + 1, j - 1, j + 1, []
                try:
                    check.append(isinstance(puzzleBoard[i][left], int) or puzzleBoard[i][left] == month or puzzleBoard[i][left] == day)
                except:
                    pass
                try:
                    check.append(isinstance(puzzleBoard[i][right], int) or puzzleBoard[i][right] == month or puzzleBoard[i][right] == day)
                except:
                    pass
                try:
                    check.append(isinstance(puzzleBoard[up][j], int) or puzzleBoard[up][j] == month or puzzleBoard[up][j] == day)
                except:
                    pass
                try:
                    check.append(isinstance(puzzleBoard[down][j], int) or puzzleBoard[down][j] == month or puzzleBoard[down][j] == day)
                except:
                    pass
                if all(check):
                    return True
    return False

def solvePuzzle(puzzleBoard, month, day, pieces, pieceIndex):
    """solves a puzzle of the day for a given day and month"""
    l = [0, 0]
    # no empty spots left, puzzle is solved
    if not getEmptySpot(puzzleBoard, month, day, l) or pieces == []:
        return puzzleBoard

    for key, value in pieceIndex.items():
        for index in value:
            start = []
            while getNextStart(pieces[index-1], start):
                if safePlace(puzzleBoard, month, day, l, start, pieces[index-1], key):
                    new_pieceIndex = deepcopy(pieceIndex)
                    del new_pieceIndex[key]
                    solvedBoard = solvePuzzle(puzzleBoard, month, day, pieces, new_pieceIndex)
                    if solvedBoard != False:
                        return solvedBoard
    return False

if __name__ == '__main__':
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    puzzle = [["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
              ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
              ["1", "2", "3", "4", "5", "6", "7"],
              ["8", "9", "10", "11", "12", "13", "14"],
              ["15", "16", "17", "18", "19", "20", "21"],
              ["22", "23", "24", "25", "26", "27", "28"],
              ["29", "30", "31"]]

    piece1 = [[1, 1, 0, 0], 
              [1, 0, 0, 0], 
              [1, 0, 0, 0], 
              [1, 0, 0, 0]]

    mirrorPiece1 = [[0, 0, 1, 1], 
                    [0, 0, 0, 1], 
                    [0, 0, 0, 1], 
                    [0, 0, 0, 1]]

    piece2 = [[2, 0, 0, 0], 
              [2, 2, 0, 0], 
              [2, 0, 0, 0], 
              [2, 0, 0, 0]]

    mirrorPiece2 = [[0, 0, 0, 2], 
                    [0, 0, 2, 2], 
                    [0, 0, 0, 2], 
                    [0, 0, 0, 2]]

    piece3 = [[0, 0, 0], 
              [3, 0, 3], 
              [3, 3, 3]]

    piece4 = [[0, 0, 4], 
              [4, 4, 4], 
              [4, 0, 0]]

    mirrorPiece4 = [[4, 0, 0], 
                    [4, 4, 4], 
                    [0, 0, 4]]

    piece5 = [[5, 5, 5], 
              [5, 5, 5], 
              [0, 0, 0]]

    piece6 = [[6, 0, 0], 
              [6, 0, 0], 
              [6, 6, 6]]

    piece7 = [[0, 0, 0, 0], 
              [0, 0, 0, 0], 
              [0, 0, 7, 7], 
              [7, 7, 7, 0]]
    
    mirrorPiece7 = [[0, 0, 0, 0], 
                    [0, 0, 0, 0], 
                    [7, 7, 0, 0], 
                    [0, 7, 7, 7]]

    piece8 = [[8, 8, 8], 
              [0, 8, 8], 
              [0, 0, 0]]
    
    mirrorPiece8 = [[8, 8, 8], 
                    [8, 8, 0], 
                    [0, 0, 0]]

    pieces = [piece1, mirrorPiece1, piece2, mirrorPiece2, piece3, piece4, mirrorPiece4, piece5, piece6, piece7, mirrorPiece7, piece8, mirrorPiece8]
    pieceIndex = {1: [1,2,3,4,5,6,7,8], 2: [9,10,11,12,13,14,15,16], 3: [17,18,19,20], 4: [21,22,23,24], 5: [25,26], 6: [27,28,29,30], 7: [31,32,33,34,35,36,37,38], 8: [39,40,41,42,43,44,45,46]}
    beginSolve = False
    month, day = "", ""
    while (not beginSolve):
        while month not in months:
            month = input("Please enter a month: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec:\n").title()
        day = input("Please enter a day: 1 - 31:\n")
        if month in months and 1 <= int(day) <= 31:
            beginSolve = True
    
    new_puzzle = deepcopy(puzzle)
    l=[0,0]
    #getEmptySpot(new_puzzle, month, day, l)
    #safePlace(new_puzzle, month, day, l, [0,0], pieces[0])
    puzzle_pieces = []
    for i in range(len(pieces)):
        if i == 5 or i == 6 or i == 7:
            puzzle_pieces.append(pieces[i])
            puzzle_pieces.append(rotatePiece(pieces[i]))
        else:
            puzzle_pieces.append(pieces[i])
            puzzle_pieces.append(rotatePiece(pieces[i]))
            puzzle_pieces.append(rotatePiece(rotatePiece(pieces[i])))
            puzzle_pieces.append(rotatePiece(rotatePiece(rotatePiece(pieces[i]))))
    start = time.perf_counter()
    """
    failed = False
    for m in months:
        for d in range(1, 32):
            solvedPuzzle = solvePuzzle(deepcopy(puzzle), m, str(d), puzzle_pieces, pieceIndex)
            if solvedPuzzle != False:
                printPuzzle(solvedPuzzle, m, str(d))
            else:
                failed = True
                break
        if failed:
            print(f"failure on {m}, {d}")
            break
    """
    solvedPuzzle = solvePuzzle(deepcopy(puzzle), month, day, puzzle_pieces, pieceIndex)
    if solvedPuzzle != False:
        printPuzzle(solvedPuzzle, month, day)
    end = time.perf_counter()
    print(f"Time = {end - start:0.4f} seconds")