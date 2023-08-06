from __init__.py import isvalidchessboard




board1 = {'1a': 'wking', '1b': 'wpawn', '1c': 'wknight', '1d': 'wbishop', '1e': 'rook', '1f': 'wqueen', '1g': 'wpawn', '1h': 'wbishop', #correct board
         '1b': 'wpawn', '2b': 'wrook', '2c': 'wpawn', '2d': 'wknight', '2e': 'wbishop', '2f': 'wpawn', '2g': 'wknight', '2h': 'wrook',
         '3a': ' ', '3b': ' ', '3c': ' ', '3d': ' ', '3e': ' ', '3f': ' ', '3g': ' ', '3h': ' ',
         '4a': ' ', '4b': ' ', '4c': ' ', '4d': ' ', '4e': ' ', '4f': ' ', '4g': ' ', '4h': ' ',
         '5a': ' ', '5b': ' ', '5c': ' ', '5d': ' ', '5e': ' ', '5f': ' ', '5g': ' ', '5h': ' ',
         '6a': ' ', '6b': ' ', '6c': ' ', '6d': ' ', '6e': ' ', '6f': ' ', '6g': ' ', '6h': ' ',
         '7a': 'bpawn', '7b': 'brook', '7c': ' bbishop', '7d': ' bpawn', '7e': 'bknight', '7f': 'brook', '7g': 'wknight', '7h': ' brook',
         '8a': 'bknight', '8b': 'bpawn', '8c': 'bqueen', '8d': 'bknight', '8e': 'bknight', '8f': 'bpawn', '8g': 'brook', '8h': 'bking'}
board2 = {'1a': 'wking', '1b': 'wpawn', '1c': 'wknight', '1d': 'wbishop', '1e': 'rook', '1f': 'wqueen', '1g': 'wpawn', '1h': 'wbishop', #may work
         '1b': 'wpawn', '2b': 'wrook', '2c': 'wpawn', '2d': 'wknight', '2e': 'wbishop', '2f': 'wpawn', '2g': 'wknight', '2h': 'wrook',
         '3a': ' ', '3b': ' ', '3c': ' ', '3d': ' ', '3e': ' ', '3f': ' ', '3g': ' ', '3h': ' ',
         '4a': ' ', '4b': ' ', '4c': ' ', '4d': ' ', '4e': ' ', '4f': ' ', '4g': ' ', '4h': ' ',
         '5a': ' ', '5b': ' ', '5c': ' ', '5d': ' ', '5e': ' ', '5f': ' ', '5g': ' ', '5h': ' ',
         '6a': ' ', '6b': ' ', '6c': 'bpawn', '6d': 'bpawn', '6e': 'bpawn', '6f': 'bpawn', '6g': 'bpawn', '6h': 'bpawn',
         '7a': 'bpawn', '7b': ' ', '7c': '  ', '7d': ' bpawn', '7e': ' ', '7f': 'brook', '7g': 'wknight', '7h': ' brook',
         '8a': 'bknight', '8b': 'bpawn', '8c': 'bqueen', '8d': 'bknight', '8e': 'bknight', '8f': 'bpawn', '8g': 'brook', '8h': 'bking'}

board3 = {'1a': 'wking', '1b': 'wpawn', '1c': 'wknight', '1d': 'wbishop', '1e': 'rook', '1f': 'wqueen', '1g': 'wpawn', '1h': 'wbishop', # will give false result
         '1b': 'wpawn', '2b': 'wrook', '2c': 'wpawn', '2d': 'wknight', '2e': 'wbishop', '2f': 'wpawn', '2g': 'wknight', '2h': 'wrook',
         '3a': ' ', '3b': ' ', '3c': ' ', '3d': ' ', '3e': ' ', '3f': ' ', '3g': ' ', '3h': ' ',
         '4a': ' ', '4b': ' ', '4c': ' ', '4d': ' ', '4e': ' ', '4f': ' ', '4g': ' ', '4h': ' ',
         '5a': ' ', '5b': ' ', '5c': ' ', '5d': ' ', '5e': ' ', '5f': ' ', '5g': ' ', '5h': ' ',
         '6a': ' ', '6b': ' ', '6c': ' ', '6d': 'bpawn', '6e': 'bpawn', '6f': 'bpawn', '6g': 'bpawn', '6h': 'bpawn',
         '7a': 'bpawn', '7b': ' ', '7c': '  ', '7d': ' bpawn', '7e': ' ', '7f': 'brook', '7g': 'wknight', '7h': ' brook',
         '8a': 'bknight', '8b': 'bpawn', '8c': 'bqueen', '8d': 'bknight', '8e': 'bknight', '8f': 'bpawn', '8g': 'brook', '8h': 'bking',
         '7z': 'brook'}


isvalidchessboard(board3)
