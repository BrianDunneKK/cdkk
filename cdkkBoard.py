# To Do: Implement resize(keep_existing=True)
# To Do: Implement copy(another_board)

class Board:
    default_symbols = {0:" ", -1:"█"}

    def __init__(self, xsize:int = 0, ysize:int = 0):
        self._board = [[]]
        self._symbols = Board.default_symbols

        self.resize(xsize, ysize, False)

    def resize(self, xsize:int, ysize:int = 0, keep_existing:bool = False):
        if ysize <= 0:
            ysize = xsize
        if xsize <= 0:
            return False
        if keep_existing and self.board_ok:
            # To Do: Not implemented yet
            return False
        self._board = [ [0]*xsize for i in range(ysize) ]
        return True

    @property
    def board_ok(self):
        return (not (len(self._board[0]) == 0))

    @property
    def xsize(self):
        if self.board_ok:
            return (len(self._board[0]))
        else:
            return 0

    @property
    def ysize(self):
        if self.board_ok:
            return (len(self._board))
        else:
            return 0

    def get(self, x:int, y:int):
        if (not self.board_ok) or x<0 or y<0 or x>=self.xsize or y>=self.ysize:
            return -1
        return self._board[y][x]

    def set(self, x:int, y:int, piece:int, overwrite_ok:bool = True):
        existing = self.get(x, y)
        if piece < 0 or existing < 0 or (not existing == 0 and not overwrite_ok):
            return False
        self._board[y][x] = piece
        return True

    def clear(self, x:int, y:int):
        existing = self.get(x, y)
        if existing < 0:
            return False
        self._board[y][x] = 0
        return True

    def clear_all(self):
        self._board = [ [0]*self.xsize for i in range(self.ysize) ]

    def symbols(self, sym:dict[int, str] = {}):
        if len(sym) > 0:
            self._symbols = sym

    def strings(self, digits:int = 1, sep:str = " ", as_int:bool = False):
        strs = []

        if as_int:
            fmt = f"{{:0{digits}d}}"
            for row in self._board:
                row_str = [fmt.format(x) for x in row]
                strs.append(sep.join(row_str))

        else:
            default_sym = self._symbols.get(-1, " ")
            for row in self._board:
                row_list = []
                for cell in row:
                    row_list.append(self._symbols.get(cell, default_sym))
                strs.append(sep.join(row_list))

        return strs

    def frequency(self):
        freq = {}
        for row in self._board:
            for cell in row:
                freq[cell] = freq.get(cell, 0) + 1
        return freq


#----------------------------------------

if __name__ == '__main__':
    board = Board(6, 5)
    board.set(5, 4, 9)
    board.symbols({0:".", 9:"X", -1:"?"})
    print("\n".join(board.strings()))
