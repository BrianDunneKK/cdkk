# To Do: Implement copy(another_board)

class Board:
    default_symbols = {0:" ", 1:"X", -1:"?"}
    directions = {
        "N"  :( 0, 1),  "S" :( 0,-1)
        ,"E" :( 1, 0),  "W" :(-1, 0)
        ,"NE":( 1, 1),  "SW":(-1,-1)
        ,"SE":( 1,-1),  "NW":(-1, 1)
        }

    def __init__(self, xsize:int = 0, ysize:int = 0):
        self._board = [[]]
        self.symbols(Board.default_symbols)
        self.resize(xsize, ysize)

    def resize(self, xsize:int, ysize:int = 0):
        if ysize <= 0:
            ysize = xsize
        if xsize <= 0:
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

    def symbols(self, sym:dict[int, str] = {}):
        if len(sym) > 0:
            self._symbols = sym
        else:
            self._symbols = Board.default_symbols
        self._inv_symbols = {v: k for k, v in self._symbols.items()}

    def to_symbol(self, value: int):
        default_sym = self._symbols.get(-1, "?")
        return self._symbols.get(value, default_sym)

    def from_symbol(self, sym: str):
        return self._inv_symbols.get(sym, -1)

    def get(self, x:int, y:int, as_symbol: bool = True):
        if (not self.board_ok) or x<0 or y<0 or x>=self.xsize or y>=self.ysize:
            value = -1
        else:
            value = self._board[y][x]
        return self.to_symbol(value) if as_symbol else value

    def set(self, x:int, y:int, piece:int, overwrite_ok:bool = True):
        existing = int(self.get(x, y, False))
        if piece < 0 or existing < 0 or (not existing == 0 and not overwrite_ok):
            return False
        self._board[y][x] = piece
        return True

    def clear(self, x:int, y:int):
        existing = int(self.get(x, y, False))
        if existing < 0:
            return False
        self._board[y][x] = 0
        return True

    def clear_all(self):
        self._board = [ [0]*self.xsize for i in range(self.ysize) ]

    def strings(self, digits:int = 1, sep:str = " ", as_symbol: bool = True):
        strs = []
        if as_symbol:
            default_sym = self._symbols.get(-1, "?")
            for row in reversed(self._board):
                row_list = []
                for cell in row:
                    row_list.append(self.to_symbol(cell))
                strs.append(sep.join(row_list))
        else:
            fmt = f"{{:0{digits}d}}"
            for row in reversed(self._board):
                row_str = [fmt.format(x) for x in row]
                strs.append(sep.join(row_str))
        return strs

    def frequency(self):
        freq = {}
        for row in self._board: 
            for cell in row:
                freq[cell] = freq.get(cell, 0) + 1
        return freq

    def in_a_row(self, xrow: int, ycol: int, as_symbol: bool = True):
        counts = { "N":0, "NE":0, "E":0, "SE":0, "S":0, "SW":0, "W":0, "NW":0 }

        for dir in counts:
            counts[dir] = self._in_a_row_dir(xrow, ycol, dir)

        counts["cell"] = self.get(xrow, ycol, as_symbol)
        counts["NS"] = max(counts["N"] + counts["S"] - 1, 0)
        counts["EW"] = max(counts["E"] + counts["W"] - 1, 0)
        counts["NESW"] = max(counts["NE"] + counts["SW"] - 1, 0)
        counts["SENW"] = max(counts["SE"] + counts["NW"] - 1, 0)
        counts["max"] = max(counts["NS"], counts["EW"], counts["NESW"], counts["SENW"])

        return counts

    def _in_a_row_dir(self, xrow: int, ycol: int, dir: str):
        count = 0
        x, y = (xrow, ycol)
        cell = curr_cell = int(self.get(xrow, ycol, False))
        dx, dy = Board.directions.get(dir, (0,0))

        if cell < 0 or (dx == 0 and dy == 0):
            return count

        while curr_cell == cell:
            count += 1
            x += dx
            y += dy
            curr_cell = int(self.get(x, y, False))
        return count

    def split_turn(self, turn: str, start_at_1: bool = True):
        # Split the turn command based on the format: xcol,yrow[,command]
        # start_at_1 = True ... The first row and column is 1
        # Return x=y=-1 if invalid format

        invalid = (-1, -1, turn)
        xyc_list = turn.split(sep = ",")
        if len(xyc_list) < 2:
            return invalid
        
        if not (xyc_list[0].isnumeric() and xyc_list[0].isnumeric()):
            return invalid

        x = int(xyc_list[0])
        y = int(xyc_list[1])
        command = ",".join(xyc_list[2:])
        if start_at_1:
            x -= 1
            y -= 1

        if self.get(x, y, as_symbol=False) == -1:
            return invalid

        return (x, y, command)

#----------------------------------------

if __name__ == '__main__':
    board = Board(6, 5)
    board.set(1, 2, 9)
    board.set(5, 4, 9)
    board.symbols({0:".", 9:"X", -1:"?"})
    print("\n".join(board.strings()))
    print()
    print(f"(0,0) ... {board.in_a_row(0,0)}")
    print(f"(1,4) ... {board.in_a_row(1,4)}")
