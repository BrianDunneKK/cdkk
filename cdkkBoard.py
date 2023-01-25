from typing import cast, Iterable
from rich.text import Text
from string import ascii_lowercase, hexdigits
from cdkkGamePiece import GamePiece, GamePieceSet, Card, CardDeck

class Board:
    default_symbols = {0:" ", 1:"X", -1:"?"}
    directions = {
        "N"  :( 0, 1),  "S" :( 0,-1)
        ,"E" :( 1, 0),  "W" :(-1, 0)
        ,"NE":( 1, 1),  "SW":(-1,-1)
        ,"SE":( 1,-1),  "NW":(-1, 1)
        ,"U" :( 0, 1),  "D" :( 0,-1)
        ,"R" :( 1, 0),  "L" :(-1, 0)
        }

    def __init__(self, xsize:int = 0, ysize:int = 0, symbol_dict: dict = {}):
        self._board_ok = False
        self._board: list[list[GamePiece]] = [[]]
        self.symbols(Board.default_symbols)
        self.symbols(symbol_dict)
        self.resize(xsize, ysize)
        self.piece_size = (1,1)

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

    def validate_xy(self, x:int, y:int) -> tuple:
        if x<0 or y<0 or x>=self.xsize or y>=self.ysize:
            x = -1
            y = -1
        return (x, y)

    def offset(self, x:int, y:int, dir:str, count:int) -> tuple:
        dx, dy = Board.directions.get(dir, (0,0))
        x2 = x + dx * count
        y2 = y + dy * count
        return self.validate_xy(x2, y2)

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

    def get_offset(self, x:int, y:int, dir:str, count:int) -> int:
        x, y = self.offset(x, y, dir, count)
        return self.get(x, y)

    def filter_by_code(self, code:int) -> list[tuple[int, int]]:
        pieces: list[tuple[int, int]] = []
        for r in range(self.ysize):
            for c in range(self.xsize):
                piece = self._board[r][c]
                if piece.code == code:
                    pieces.append((c, r))
        return pieces

    def filter_by_context(self, context:dict) -> list[tuple[int, int]]:
        pieces: list[tuple[int, int]] = []
        for r in range(self.ysize):
            for c in range(self.xsize):
                piece = self._board[r][c]
                common = {k: context[k] for k in context if k in piece.context and context[k] == piece.context[k]}
                if len(common) == len(context):
                    pieces.append((c, r))
        return pieces

    def set(self, x:int, y:int, code:int = 0, overwrite_ok:bool = True, piece:GamePiece|None = None) -> bool:
        existing = self.get(x, y)
        if code < 0 or existing < 0 or (existing > 0 and not overwrite_ok):
            return False
        if piece is not None:
            self._board[y][x] = piece
        else:
            self._board[y][x] = self.create_piece(code)
        self.piece_size = (self._board[y][x].str_xcols, self._board[y][x].str_yrows)
        return True

    def set_unused(self, x:int, y:int) -> bool:
        existing = int(self.get(x, y))
        if existing >= 0:
            self._board[y][x] = self.create_piece(-1)
        return True

    def set_unused_mask(self, mask:list[list[int]]) -> bool:
        for yrow in range(len(mask)):
            for xcol in range(len(mask[0])):
                if mask[self.ysize-yrow-1][xcol] == 0:
                    self.set_unused(xcol, yrow)
        return True

    def clear(self, x:int, y:int) -> bool:
        existing = int(self.get(x, y))
        if existing < 0:
            return False
        self._board[y][x] = self.create_piece()
        return True

    def clear_all(self):
        for r in range(self.ysize):
            for c in range(self.xsize):
                self.clear(c, r)
        # Need to iterate to respect unused cells
        # self._board = [ [self.create_piece()]*self.xsize for i in range(self.ysize) ]

    def fill(self, code:int = 0, overwrite_ok:bool = True) -> bool:
        for r in range(self.ysize):
            for c in range(self.xsize):
                self.set(x=c, y=r, code=code, overwrite_ok=overwrite_ok)
        return True

    def move(self, x:int, y:int, dir:str, count:int, overwrite_ok:bool = True) -> int:
        tx, ty = self.offset(x, y, dir, count)
        from_code = self.get(x, y)
        to_code = self.get(tx, ty)
        if tx < 0 or ty < 0 or from_code <= 0 or to_code < 0 or (to_code > 0 and not overwrite_ok):
            return -1
        
        self.set(tx, ty, piece = self.get_piece(x, y))
        self.clear(x, y)
        return to_code

    def jump(self, x:int, y:int, dir:str, just_check:bool = False) -> int:
        x1, y1 = self.offset(x, y, dir, 1)
        x2, y2 = self.offset(x, y, dir, 2)
        x0, y0 = self.validate_xy(x, y)
        x1, y1 = self.validate_xy(x1, y1)
        x2, y2 = self.validate_xy(x2, y2)

        if x0 < 0 or x1 < 0 or x2 < 0 or y0 < 0 or y1 < 0 or y2 < 0:
            return -1

        c0 = self.get(x0, y0)
        c1 = self.get(x1, y1)
        c2 = self.get(x2, y2)

        if c0 <= 0 or c1 <= 0 or c2 != 0:
            return -1

        if not just_check:
            self.move(x0, y0, dir, 2)
            self.clear(x1, y1)

        return c1

    def strings(self, padding:str = " ") -> list[str]:
        total_xcols = self.piece_size[0] * self.xsize + len(padding) * (self.xsize-1)
        total_yrows = self.piece_size[1] * self.ysize
        strs = [ "#" * total_xcols for i in range(total_yrows) ]

        for r in range(self.ysize):
            for c in range(self.xsize):
                piece = self._board[r][c]
                piece_strs = piece.strings()
                for pr in range(self.piece_size[1]):
                    for pc in range(self.piece_size[0]):
                        x = c*(self.piece_size[0] + len(padding)) + pc
                        y = (self.ysize * self.piece_size[1] - 1) - (r * self.piece_size[1]) - (self.piece_size[1] - 1) + pr
                        strs[y] = strs[y][:x] + piece_strs[pr][pc] + strs[y][x+1:]

        for r in range(len(strs)):
            for c in range(self.xsize-1):
                for pc in range(len(padding)):
                    x = self.piece_size[0] + c*(self.piece_size[0] + len(padding)) + pc
                    strs[r] = strs[r][:x] + padding[pc] + strs[r][x+1:]

        return (strs)

    # Border on all sides; single line
    borders_single1 = {'─':Text('─'), '│':Text(' │ '), '┌':Text(' ┌─'), '┐':Text('─┐ '), '└':Text(' └─') \
        ,'┘':Text('─┘ '), '├':Text(' ├─'), '┤':Text('─┤ '), '┬':Text('─┬─'), '┴':Text('─┴─'), '┼':Text('─┼─') }
    borders_single2 = {'─':Text('─'), '│':Text('  │  '), '┌':Text('  ┌──'), '┐':Text('──┐  '), '└':Text('  └──') \
        ,'┘':Text('──┘  '), '├':Text('  ├──'), '┤':Text('──┤  '), '┬':Text('──┬──'), '┴':Text('──┴──'), '┼':Text('──┼──') }

    # Border on all sides; double line
    borders_double1 = {'─':Text('═'), '│':Text(' ║ '), '┌':Text(' ╔═'), '┐':Text('═╗ '), '└':Text(' ╚═') \
        ,'┘':Text('═╝ '), '├':Text(' ╠═'), '┤':Text('═╣ '), '┬':Text('═╦═'), '┴':Text('═╩═'), '┼':Text('═╬═') }

    # Space as horizontal border (padding); no top/bottom/middle lines
    borders_sph1 = {'│':Text(' '), '┬':Text(' '), '┴':Text(' '), \
        '─':Text(''), '┌':Text(''), '┐':Text(''), '└':Text(''), '┘':Text(''), '├':Text(''), '┤':Text(''), '┼':Text('') }
    borders_sph2 = {'│':Text('  '), '┬':Text('  '), '┴':Text('  '), \
        '─':Text(''), '┌':Text(''), '┐':Text(''), '└':Text(''), '┘':Text(''), '├':Text(''), '┤':Text(''), '┼':Text('') }

    def richtext(self, padding: list[Text] = [], \
        borders: dict[str,Text] = {x:Text(x) for x in [*'─│┌┐└┘├┤┬┴┼']}, \
        unused: Text = Text('█', style = "white"), \
        gridref: str|None = None) -> list[Text]:

        if len(borders) == 0:
            borders = {x:Text('') for x in [*'─│┌┐└┘├┤┬┴┼']}

        total_xcols = self.piece_size[0] * self.xsize + len(borders['─']) * (self.xsize-1) + len(borders['┌']) + len(borders['┐'])
        total_yrows = self.piece_size[1] * self.ysize + (len(borders['┼']) > 0) * (self.ysize-1) + (len(borders['┌']) > 0) + (len(borders['└']) > 0)
        blank = Text('')
        blank.pad_left(total_xcols, '#')
        strs = [ blank for i in range(total_yrows) ]

        horizstrs = []
        for i in range(self.piece_size[0]):
            horizstrs.append(borders['─'])
        horizborder = Text('').join(horizstrs)

        # Top border
        yrow = 0
        if len(borders['┌']) > 0:
            rowstrs = [borders['┌']]
            for i in range(self.xsize-1):
                rowstrs.append(horizborder)
                rowstrs.append(borders["┬"])
            rowstrs.append(horizborder)
            rowstrs.append(borders["┐"])
            strs[yrow] = Text('').join(rowstrs)
            yrow += 1

        # Middle rows
        middle_str = Text('')
        if len(borders['┼']) > 0:
            rowstrs = [borders['├']]
            for i in range(self.xsize-1):
                rowstrs.append(horizborder)
                rowstrs.append(borders["┼"])
            rowstrs.append(horizborder)
            rowstrs.append(borders["┤"])
            middle_str = Text('').join(rowstrs)

        # Each game piece row
        for r in range(self.ysize):

            row_piece_strs = []
            for c in range(self.xsize):
                piece = self._board[self.ysize - r - 1][c]
                if piece.code >= 0:
                    piece_rt = piece.richtext()
                else:
                    unused_str = unused.copy()
                    if piece.str_xcols > 1:
                        unused_str.pad_left(piece.str_xcols-1, unused.plain)
                    piece_rt = [ unused_str for i in range(piece.str_yrows) ]
                row_piece_strs.append(piece_rt)

            # Each row of the game piece
            for pr in range(self.piece_size[1]):
                rowstrs = [borders["│"]]

                # Each game piece column
                for c in range(self.xsize):
                    rowstrs.append(row_piece_strs[c][pr])
                    rowstrs.append(borders["│"])

                strs[yrow] = Text('').join(rowstrs)
                yrow += 1

            if len(borders['┼']) > 0:
                strs[yrow] = middle_str
                yrow += 1

        # Bottom border
        if len(borders['└']) > 0:
            rowstrs = [borders['└']]
            for i in range(self.xsize-1):
                rowstrs.append(horizborder)
                rowstrs.append(borders["┴"])
            rowstrs.append(horizborder)
            rowstrs.append(borders["┘"])
            strs[total_yrows-1] = Text('').join(rowstrs)

                    # for pc in range(self.piece_size[0]):
                    #     x = c*(self.piece_size[0] + len(padding)) + pc
                    #     y = (self.ysize * self.piece_size[1] - 1) - (r * self.piece_size[1]) - (self.piece_size[1] - 1) + pr
                    #     strs[yrow+y] = Text.assemble(strs[y][:x], piece_strs[pr][pc], strs[y][x+1:])

        for r in range(len(strs)):
            for c in range(self.xsize-1):
                for pc in range(len(padding)):
                    x = self.piece_size[0] + c*(self.piece_size[0] + len(padding)) + pc
                    strs[yrow+r] = strs[r][:x] + padding[pc] + strs[r][x+1:]

        if gridref is not None:
            for i in range(self.xsize):
                ch = Text(ascii_lowercase[i], style = gridref)
                x = len(borders['┌']) + i * (self.piece_size[0] + len(borders['┬'])) + self.piece_size[0]//2 
                strs[0] = strs[0][:x] + ch + strs[0][x+1:]
            for i in range(self.ysize):
                ch = Text(str(i+1), style = gridref)
                x = len(borders['┌']) // 2
                y = 1 + i * (self.piece_size[1] + 1) + self.piece_size[1]//2
                strs[y] = strs[y][:x] + ch + strs[y][x+1:]

        return (strs)

    def rt_stylise(self, st_dict: dict[str,Text], style: str) -> dict[str,Text]:
        for item in st_dict.items():
            item[1].stylize(style)
        return st_dict

    def frequency(self) -> dict:
        freq = {}
        for row in self._board: 
            for cell in row:
                freq[cell.code] = freq.get(cell.code, 0) + 1
        return freq

    def in_a_row(self, xrow: int, ycol: int) -> dict[str, int]:
        counts = { "N":0, "NE":0, "E":0, "SE":0, "S":0, "SW":0, "W":0, "NW":0 }

        for dir in counts:
            counts[dir] = self._in_a_row_dir(xrow, ycol, dir)

        counts["value"] = self.get(xrow, ycol)
        # counts["piece"] = self.get_piece(xrow, ycol)
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

    def from_gridref(self, turn: str) -> tuple:
        x = ord(turn.upper()[0]) - ord('A')
        y = self.ysize - int(turn[1])
        x, y = self.validate_xy(x, y)
        return (x, y, turn[2:])

    def to_gridref(self, x:int, y:int) -> str:
        xs = ascii_lowercase[x]
        ys = hexdigits[self.ysize - y]
        return f"{xs}{ys}"

# ----------------------------------------

class GamePieceSetMgr(GamePieceSet):
    def __init__(self \
        ,pieces: list[GamePiece] = [] \
        ,board: Board = Board(), board_origin: tuple[int,int] = (0,0) \
        ,board_dir: tuple[int,int] = (1,0), board_wrap: tuple[int,int] = (0,-1)) -> None:

        super().__init__(pieces)
        self._board = board
        self._board_origin = board_origin
        self._board_dir = board_dir
        self._board_wrap = board_wrap

    def set_game_piece_bank(self, bank: GamePieceSet) -> None:
        self._bank = bank

    def take_from_bank(self, count: int, context: dict = {}) -> None:
        self.extend(self._bank.popN(count, context))

    def place_on_board(self, wrap = (0, -1)) -> None:
        cell_offset = wrap_offset = 0
        for piece in self:
            x = self._board_origin[0] + cell_offset * self._board_dir[0] + wrap_offset * self._board_wrap[0]
            y = self._board_origin[1] + cell_offset * self._board_dir[1] + wrap_offset * self._board_wrap[1]
            if self._board.set(x, y, piece = piece):
                cell_offset += 1
            else:
                cell_offset = 0
                wrap_offset += 1
                x = self._board_origin[0] + cell_offset * self._board_dir[0] + wrap_offset * self._board_wrap[0]
                y = self._board_origin[1] + cell_offset * self._board_dir[1] + wrap_offset * self._board_wrap[1]
                if self._board.set(x, y, piece = piece):
                    cell_offset += 1
                else:
                    break

# ----------------------------------------
                                                                                                           
class CardTable(Board):
    def create_piece(self, code: int = 0, value: int = -1):
        return Card(code)

class CardPlayer(GamePieceSetMgr):
    def __init__(self, cards: Iterable[Card] = [], table: CardTable = CardTable(), deck: CardDeck = CardDeck() \
        ,first_card: tuple[int, int] = (0, 0), cards_dir: tuple[int, int] = (1, 0), cards_wrap: tuple[int, int] = (0, -1)) -> None:

        super().__init__(pieces=cast(list[GamePiece],cards), board = table \
            ,board_origin=first_card, board_dir=cards_dir, board_wrap=cards_wrap)
        self.set_deck(deck)

    def set_deck(self, deck: CardDeck) -> None:
        return super().set_game_piece_bank(deck)

    def deal(self, count: int, context: dict = {}) -> None:
        return super().take_from_bank(count, context)

    def place_on_table(self, wrap=(0, -1)) -> None:
        return super().place_on_board(wrap)

# ----------------------------------------

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

    p1 = GamePiece(3)
    p2 = GamePiece(6)
    p3 = GamePiece(9)
    board2 = Board(2,5)
    gps1 = GamePieceSetMgr([p1, p2, p3], board = board2, board_origin=(0,2))
    gps1.place_on_board()
    print("\n".join(board2.strings(padding='')))

