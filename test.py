import  numpy as np

#Remove somemore for diagonal
def getNumberOfKrakenPos():
    possiblePos = set()
    board = [[0 for x in range(6)] for y in range(6)]
    for x in range(5):
        for y in range(5):
            board[x][y] = 1
            for x2 in range(5):
                for y2 in range(5):
                    if x is not x2 or y is not y2:
                        board[x2][y2] = 2
                        if 1 not in board[x2] and 1 not in [board[x3][y2] for x3 in range(6)] and not getDiagonal(board, x2, y2):
                            possiblePos.add(str(list(np.ravel(board))))
                        board[x2][y2] = 0
            board[x][y] = 0
    print(len(possiblePos))


def getDiagonal(board, x2, y2):
    for x in range(1 ,8):
        for y in range(1, 8):
            print(y)
            if x2 + x < 6 and y2 + y < 6 and board[x2+x][y2+y] == 1:
                return True
            elif x2 + x < 6 and y2 - y > 0 and board[x2+x][y2-y] == 1:
                return True
            elif x2 - x > 0 and y2 - y > 0 and board[x2-x][y2-y] == 1:
                return True
            elif x2 - x > 0 and y2 + y < 6 and board[x2 - x][y2 +y] == 1:
                return True
    return False

if __name__ == '__main__':
    getNumberOfKrakenPos()