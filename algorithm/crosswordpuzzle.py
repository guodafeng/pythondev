#!/bin/python3

import math
import os
import random
import re
import sys
import copy

#
# Complete the 'crosswordPuzzle' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts following parameters:
#  1. STRING_ARRAY crossword
#  2. STRING words
#

def crosswordPuzzle(crossword, words):
    # Write your code here
    # orgnize words
    boards = [crossword]
    words = words.split(';')
    for w in words:
        print(w)
        print(boards)
        nextBoards = []
        for crossword in boards:
            nextBoards.extend(fillWordByRow(crossword, w))
            nextBoards.extend(fillWordByCol(crossword, w))
            
        boards = nextBoards
        
    return boards[0] if boards else []

    
def fillWordByRow(crossword, w):
    l = len(w)
    ws = [w, w[::-1]] # reversed string of w need check as well
    boards = [] # possible states of crossword after put w

    for i, row in enumerate(crossword):

        delms = row.split('+')
        for j, delm in enumerate(delms):
            for w in ws:
                if len(delm) == l and all((w[i] == delm[i] or delm[i] == '-' for i in range(l))):
                    delms[j] = w
                    b = copy.deepcopy(crossword)
                    b[i] = '+'.join(delms)
                    boards.append(b)
                    
    return boards
                
def fillWordByCol(crossword, w):
    # rotate crossword
    r = zip(*crossword)
    r = [''.join(row) for row in r]
    boards = fillWordByRow(r, w)
    # revert back
    boards = [zip(*b) for b in boards]
    return [[''.join(row) for row in b] for b in boards ]
    
                


if __name__ == '__main__':
    fptr = open(r'd:/test.txt', 'w')

    crossword = []

    for _ in range(10):
        crossword_item = input()
        crossword.append(crossword_item)

    words = input()

    result = crosswordPuzzle(crossword, words)

    fptr.write('\n'.join(result))
    fptr.write('\n')

    fptr.close()
