# To Do: Implement copy(another_board)
from cdkkGamePiece import GamePiece

class Board:
    default_symbols = {0:" ", 1:"X", -1:"?"}
    directions = {
        "N"  :( 0, 1),  "S" :( 0,-1)
        ,"E" :( 1, 0),  "W" :(-1, 0)
        ,"NE":( 1, 1),  "SW":(-1,-1)
        ,"SE":( 1,-1),  "NW":(-1, 1)
        }

    def __init__(self, xsize:int = 0, ysize:int = 0, symbol_dict: dict = {}):
        self._board_ok = False
        self._board: list[list[GamePiece]] = [[]]
        self.symbols(Board.default_symbols)
        self.symbols(symbol_dict)
        self.resize(xsize, ysize)

    def create_piece(self, code: int = 0, value: int = -1) -> GamePiece:
        return GamePiece(code, value, symbol_dict=self._symbols)
        
    def resize(self, xsize:int, ysize:int = 0) -> bool:
        self._board_ok = (xsize > 0)
        if ysize <= 0:
            ysize = xsize
        if xsize <= 0:
            return False
        self._board = [ [self.create_piece()]*xsize for i in range(ysize) ]
        return True

    @property
    def board_ok(self) -> bool:
        return (self._board_ok)

    @property
    def xsize(self) -> int:
        if self.board_ok:
            return (len(self._board[0]))
        else:
            return 0

    @property
    def ysize(self) -> int:
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

    # def to_symbol(self, value: int) -> str:
    #     default_sym = self._symbols.get(-1, "?")
    #     return self._symbols.get(value, default_sym)

    def from_symbol(self, sym: str) -> int:
        return self._inv_symbols.get(sym, -1)

    def get(self, x:int, y:int) -> int:
        piece = self.get_piece(x, y)
        return piece.value

    def get_piece(self, x:int, y:int) -> GamePiece:
        if (not self.board_ok) or x<0 or y<0 or x>=self.xsize or y>=self.ysize:
            piece = self.create_piece(-1)
        else:
            piece = self._board[y][x]
        return piece

    def filter_pieces(self, filter:dict) -> list[GamePiece]:
        pieces: list[GamePiece] = []
        for r in range(self.ysize):
            for c in range(self.xsize):
                piece = self._board[r][c]
                common = {k: filter[k] for k in filter if k in piece.context and filter[k] == piece.context[k]}
                if len(common) == len(filter):
                    pieces.append(piece)
        return pieces

    def set(self, x:int, y:int, code:int = 0, overwrite_ok:bool = True, piece:GamePiece|None = None) -> bool:
        existing = int(self.get(x, y))
        if code < 0 or existing < 0 or (existing > 0 and not overwrite_ok):
            return False
        if piece is not None:
            self._board[y][x] = piece
        else:
            self._board[y][x] = self.create_piece(code)
        return True

    def clear(self, x:int, y:int) -> bool:
        existing = int(self.get(x, y))
        if existing < 0:
            return False
        self._board[y][x] = self.create_piece()
        return True

    def clear_all(self):
        self._board = [ [self.create_piece()]*self.xsize for i in range(self.ysize) ]

    def strings(self, digits:int = 1, padding:str = " ") -> list[str]:
        piece_xcols = self._board[0][0].str_xcols
        piece_yrows = self._board[0][0].str_yrows
        total_xcols = piece_xcols * self.xsize + len(padding) * (self.xsize-1)
        total_yrows = piece_yrows * self.ysize
        strs = [ "#" * total_xcols for i in range(total_yrows) ]

        for r in range(self.ysize):
            for c in range(self.xsize):
                piece = self._board[r][c]
                piece_strs = piece.strings()
                for pr in range(piece_yrows):
                    for pc in range(piece_xcols):
                        x = c*(piece_xcols + len(padding)) + pc
                        y = (self.ysize * piece_yrows - 1) - (r * piece_yrows) - (piece_yrows - 1) + pr
                        strs[y] = strs[y][:x] + piece_strs[pr][pc] + strs[y][x+1:]

        for r in range(len(strs)):
            for c in range(self.xsize-1):
                for pc in range(len(padding)):
                    x = piece_xcols + c*(piece_xcols + len(padding)) + pc
                    strs[r] = strs[r][:x] + padding[pc] + strs[r][x+1:]

        return (strs)

    def frequency(self) -> dict:
        freq = {}
        for row in self._board: 
            for cell in row:
                freq[cell.code] = freq.get(cell.code, 0) + 1
        return freq

    def in_a_row(self, xrow: int, ycol: int) -> dict:
        counts = { "N":0, "NE":0, "E":0, "SE":0, "S":0, "SW":0, "W":0, "NW":0 }

        for dir in counts:
            counts[dir] = self._in_a_row_dir(xrow, ycol, dir)

        counts["value"] = self.get(xrow, ycol)
        counts["piece"] = self.get_piece(xrow, ycol)
        counts["NS"] = max(counts["N"] + counts["S"] - 1, 0)
        counts["EW"] = max(counts["E"] + counts["W"] - 1, 0)
        counts["NESW"] = max(counts["NE"] + counts["SW"] - 1, 0)
        counts["SENW"] = max(counts["SE"] + counts["NW"] - 1, 0)
        counts["max"] = max(counts["NS"], counts["EW"], counts["NESW"], counts["SENW"])

        return counts

    def _in_a_row_dir(self, xrow: int, ycol: int, dir: str) -> int:
        count = 0
        x, y = (xrow, ycol)
        cell = curr_cell = int(self.get(xrow, ycol))
        dx, dy = Board.directions.get(dir, (0,0))

        if cell < 0 or (dx == 0 and dy == 0):
            return count

        while curr_cell == cell:
            count += 1
            x += dx
            y += dy
            curr_cell = int(self.get(x, y))
        return count

    def split_turn(self, turn: str, start_at_1: bool = True) -> tuple:
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

        if self.get(x, y) == -1:
            return invalid

        return (x, y, command)

#----------------------------------------

if __name__ == '__main__':
    board = Board(6, 5, {0:".", 1:"A", 2:"B", 3:"C", 4:"D", 5:"E", -1:"?"})
    board.set(0, 0, 1)
    board.set(1, 1, 2)
    board.set(1, 2, 3)
    board.set(3, 3, 4)
    board.set(4, 4, 5)
    print("\n".join(board.strings()))
    print()
    print(f"(0,0) ... {board.in_a_row(0,0)}")
    print(f"(1,4) ... {board.in_a_row(1,4)}")

# TO DO: Fix board.strings()
