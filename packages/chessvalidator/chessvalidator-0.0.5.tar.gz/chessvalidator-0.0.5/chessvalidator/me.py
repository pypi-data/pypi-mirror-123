def isvalidchessboard(board):
    while True:
        bpieces = 0
        wpieces = 0
        wpawn = 0
        bpawn = 0
        iftrue = 0
        ft = ' '
        caracterpieces = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}
        if 'bking' not in board.values():
            print('black king does not exsist')
            ft = 'false'
            print('false')
            iftrue += 1
            break
        if 'wking' not in board.values():
            print('white king does not exsist')
            ft = 'false'
            print('false')
            iftrue += 1
            break
        for i in board.values():
            if i[0] == 'b':
                bpieces = bpieces + 1
            if i[0] == 'w':
                wpieces = wpieces + 1
            if wpieces > 16:
                print('More than 16 white pieces')
                ft = 'false'
                print('false')
                iftrue += 1
                break
            if bpieces > 16:
                print('More than 16 black pieces')
                ft = 'false'
                print('false')
                iftrue += 1
                break
                
            if i[0] == 'bpawn':
                bpawn = bpwan + 1
            if i[0] == 'wpawn':
                wpawn = wpawn + 1
            if bpawn > 8:
                print('More than 8 black pawns')
                ft = 'fales'
                print('false')
                iftrue += 1
                break
            if wpawn > 8:
                print('More than 8 white pawns')
                ft = 'false'
                print('false')
                iftrue += 1
                break
            
        for i in board.keys():
            if int(i[0]) > 8:
                print('y-axis error')
                ft = 'false'
                iftrue += 1
                print('false')
            if i[1] not in caracterpieces:
                print('x-axis error')
                ft = 'false'
                print('false')
                iftrue += 1
                break

        if iftrue == 0:
            ft = 'true'
            print('true')
            return ft
            break

        if iftrue != 0:
            return ft
            break