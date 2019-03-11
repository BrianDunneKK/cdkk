from cdkkSprite import *

### --------------------------------------------------

class Sprite_BoardGame_Board(Sprite_Shape):
    def __init__(self, name="Board"):
        super().__init__(name)
        self._rows = self._cols = 0
        self._cell0 = pygame.Rect(0,0,0,0)
        self._xsize = self._ysize = 0

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    def cell_rect(self, col, row):
        x = self.rect.left + col * self._cell0.width
        y = self.rect.top + row * self._cell0.height
        return pygame.Rect(x, y, self._cell0.width, self._cell0.height)

    def setup_grid(self, board_colours, xsize, cols, event_on_click, rows=None, ysize=None, line_width=2):
        if (len(board_colours) == 1):
            board_colours.append(None)
        if (len(board_colours) == 2):
            board_colours.append(board_colours[0])
        if (len(board_colours) == 3):
            board_colours.append("white")
        self.colours = board_colours
        self.line_width = line_width
        self.event_on_click = event_on_click
        if ysize == None:
            ysize = xsize
        self._xsize = xsize
        self._ysize = ysize
        if rows == None:
            rows = cols
        self.rect.width = xsize * cols
        self.rect.height = ysize * rows

        self.setup_shape(self.rect, [self._colour_fill])
        for i in range(0,cols):
            for j in range (0,rows):
                r = pygame.Rect(i * xsize, j * ysize, xsize, ysize)
                if (i+j)%2 == 0:
                    col = colours[self._colour_fill]
                else:
                    col = colours[self._colour_alt]
                pygame.draw.rect(self.image, col, r)
                if (self._colour_line != None):
                    pygame.draw.rect(self.image, colours[self._colour_line], r, self.line_width)
        self._draw_reqd = False
        self._cell0 = pygame.Rect(0, 0, xsize, ysize)

    def find_cell(self, x, y, allow_outside=False):
        col = (x - self.rect.left) // self._cell0.width
        row = (y - self.rect.top) // self._cell0.height
        if self.rect.collidepoint(x, y) or allow_outside:
            return (col, row)
        else:
            return (-1, -1)

    def highlight_cells(self, cell_list, highlight_on = True):
        for c in cell_list:
            r = pygame.Rect(c[0] * self._xsize, c[1] * self._ysize, self._xsize, self._ysize)
            if highlight_on:
                col = colours[self._colour_highlight]
            else:
                col = colours[self._colour_fill]
            pygame.draw.rect(self.image, col, r)
            if (self._colour_line != None):
                pygame.draw.rect(self.image, colours[self._colour_line], r, 2)

### --------------------------------------------------

class Sprite_BoardGame_Piece(Sprite_Shape):
    PIECE_CIRLCE = 1
    PIECE_SQUARE = 2

    def __init__(self, name, board, col=0, row=0):
        super().__init__(name)
        self._row = row
        self._col = col
        self._board = board
        self._piece_shape = Sprite_BoardGame_Piece.PIECE_CIRLCE
        self._cell = self._board.cell_rect(0,0)
        self._cell.topleft = (0,0)
        self.set_pos()

    def reduce_cell(self, percentage):
        r = self._cell
        r = self._cell.inflate(-int(r.width * (percentage/100.0)), -int(r.height * (percentage/100.0)))
        return r

    def setup_piece(self, piece_shape, piece_colours, no_flip=True):
        self.setup_shape()
        self.colours = piece_colours
        self._piece_shape = piece_shape
        self._draw_reqd = True
        if not no_flip:
            self.flip()

    def set_pos(self, col=None, row=None):
        if col is not None:
            self._col = col
        if row is not None:
            self._row = row
        r = self._board.cell_rect(self._col, self._row)
        self.rect.topleft = r.topleft
        self.rect.size = r.size

    def draw(self, force_draw=False):
        if self._draw_reqd or force_draw:
            self._draw_reqd = False
            if (self._piece_shape == Sprite_BoardGame_Piece.PIECE_CIRLCE):
                r = self.reduce_cell(20)
                pygame.draw.ellipse(self.image, colours[self._colour_fill], r)
                if (self._colour_line != None):
                    pygame.draw.ellipse(self.image, colours[self._colour_line], r, 3)
            if (self._piece_shape == Sprite_BoardGame_Piece.PIECE_SQUARE):
                r = self.reduce_cell(30)
                pygame.draw.rect(self.image, colours[self._colour_fill], r)
                if (self._colour_line != None):
                    pygame.draw.rect(self.image, colours[self._colour_line], r, 2)
            self.set_pos()

    def flip(self):
        self.swap_colours()

### --------------------------------------------------
