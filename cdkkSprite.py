# To Do: msecs_per_image not implemented

import pygame
import uuid
from cdkkUtils import *
from cdkkColours import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, name=""):
        super().__init__()
        self._desc = {}
        self.set_desc("name", name)
        self.set_desc("uuid", uuid.uuid4())
        self.rect = MovingRect()
        self._image = None
        self.event_on_click = None
        self.event_on_unclick = None
        self._draw_reqd = False

    def get_desc(self, attribute, no_value=None):
        if attribute in self._desc:
            return self._desc[attribute]
        else:
            return no_value

    def set_desc(self, attribute, value):
        self._desc[attribute] = value

    @property
    def name(self):
        return self.get_desc("name")

    @property
    def uuid(self):
        return self.get_desc("uuid")

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, new_image):
        self._image = new_image
        self._draw_reqd = True

    def _image_size_to_rect(self):
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height

    def _load_image_from_file(self, filename, crop=None):
        ret_image = image = pygame.image.load(filename).convert_alpha()
        if crop is not None:
            # Crop the imported image by ... crop[left, right, top, bottom]
            crop_rect = image.get_rect()
            crop_rect.width = crop_rect.width - crop[0] - crop[1]
            crop_rect.left = crop[0]
            crop_rect.height = crop_rect.height - crop[2] - crop[3]
            crop_rect.top = crop[2]
            ret_image = pygame.Surface(crop_rect.size, pygame.SRCALPHA)
            ret_image.blit(image, (0,0), crop_rect)
        return ret_image

    def load_image(self, filename, crop=None, create_mask=True):
        self.image = self._load_image_from_file(filename, crop)
        self._image_size_to_rect()
        if create_mask:
            self.create_mask()

    def create_surface(self, width, height, per_pixel_alpha=True):
        if per_pixel_alpha:
            return pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        else:
            return pygame.Surface((width, height)).convert()

    def add_image(self, image, dest=(0,0)):
        return self.image.blit(image, dest)

    def setup_mouse_events(self, event_on_click, event_on_unclick=None):
        if type(event_on_click).__name__ == "Event" or event_on_click == None:
            self.event_on_click = event_on_click
        else:
            logger.error("Sprite.setup_mouse_events(): event_on_click must be of type Event")
        if type(event_on_unclick).__name__ == "Event" or event_on_unclick == None:
            self.event_on_unclick = event_on_unclick
        else:
            logger.error("Sprite.setup_mouse_events(): event_on_unclick must be of type Event")
        self.event_on_unclick = event_on_unclick

    def draw(self, force_draw=False):
        pass

    def slow_update(self):
        pass

    def create_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def collide(self, sprite_group, collided=pygame.sprite.collide_mask):
        return pygame.sprite.spritecollide(self, sprite_group, dokill=False, collided=pygame.sprite.collide_mask)

### --------------------------------------------------

class Sprite_Animation(Sprite):
    def __init__(self, name=""):
        super().__init__(name)
        self._animations = {}
        self._anim_config = Animation_Counter()
        self._anim_name = None

    def load_animation(self, set_name, file_format, count, count_from=1, crop=None, create_mask=True):
        self._animations[set_name] = []
        for i in range(count_from, count_from + count):
            filename = file_format.format(i)
            self._animations[set_name].append(self._load_image_from_file(filename, crop))
        
        self.image = self._animations[set_name][0]
        self._image_size_to_rect()
        if create_mask:
            self.create_mask()

    def load_spritesheet(self, set_name, spritesheet_filename, cols, rows, create_mask=True):
        self._animations[set_name] = []
        spritesheet = self._load_image_from_file(spritesheet_filename)
        ss_width = spritesheet.get_rect().width
        ss_height = spritesheet.get_rect().height
        sprite_width = ss_width // cols
        sprite_height = ss_height // rows
        
        for i in range(rows):
            y = sprite_height * i
            for j in range(cols):
                x = sprite_width * j
                rect = pygame.Rect(x, y, sprite_width, sprite_height)
                image = self.create_surface(sprite_width, sprite_height)
                rect = image.blit(spritesheet, (0, 0), rect)
                self._animations[set_name].append(image)
        
        self.image = self._animations[set_name][0]
        self._image_size_to_rect()
        if create_mask:
            self.create_mask()

    def set_animation(self, new_animation, mode=ANIMATE_LOOP, loops_per_image=None):
        if self._anim_name != new_animation:
            self._anim_name = new_animation
            self._anim_config.setup(len(self._animations[new_animation]), mode, loops_per_image)
            self._draw_reqd = True

    def draw(self, force_draw=False):
        if self._draw_reqd or force_draw:
            anim_name = self._anim_name
            if (anim_name != ""):
                if self._anim_config.next_loop():
                    self.image = self._animations[anim_name][self._anim_config.current_image]

    def create_mask_anim(self, using_animation, using_frame):
        reset_animation = None
        reset_frame = None

        if self._anim_name != using_animation:
            reset_animation = self._anim_name
            reset_frame = self._anim_config.current_image
            self._anim_name = using_animation
            self._anim_config.current_image = using_frame
        elif using_frame != self._anim_config.index:
            reset_frame = self._anim_config.current_image
            self._anim_config.current_image = using_frame
        
        self.create_mask()

        if reset_animation is not None:
            self._anim_name = reset_animation
        if reset_frame is not None:
            self._anim_config.current_image = reset_frame

### --------------------------------------------------

class Sprite_Shape(Sprite):
    def __init__(self, name="", rect=None, shape_colours=None, shape="Rectangle"):
        super().__init__(name)
        self.clear_colours()
        self._shape = "Rectangle"
        self._pointlist = None
        if rect is not None:
            self.setup_shape(rect, shape_colours, shape)

    @property
    def colours(self):
        return [self._colour_fill, self._colour_line, self._colour_alt]

    @colours.setter
    def colours(self, new_colours):
        if new_colours is None:
            self.clear_colours()
        else:
            if (len(new_colours) >= 1):
                self._colour_fill = new_colours[0]
                self._colour_alt = new_colours[0]
            if (len(new_colours) >= 2):
                self._colour_line = new_colours[1]
            if (len(new_colours) >= 3 and new_colours[2] != None):
                self._colour_alt = new_colours[2]
            if (len(new_colours) >= 4):
                self._colour_highlight = new_colours[3]
        self._draw_reqd = True

    def clear_colours(self):
        self._colour_fill = None
        self._colour_alt = None
        self._colour_line = None
        self._colour_highlight = None

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, new_shape):
        # Rectangle, Ellipse, Polygon
        self._shape = new_shape

    def setup_shape(self, rect=None, shape_colours=None, shape="Rectangle"):
        if rect is not None:
            self.rect.topleft = rect.topleft
            self.rect.size = rect.size
        self.colours = shape_colours
        self.shape = shape
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self._draw_reqd = True

    def setup_polygon(self, pointlist):
        self._pointlist = pointlist.copy()
        self._draw_reqd = True

    def create_canvas(self, width=None, height=None, fill_colour=None):
        if width is None:
            width = self.rect.width
        if height is None:
            height = self.rect.height
        if fill_colour == None:
            self.image = self.create_surface(width, height, True)
        else:
            self.image = self.create_surface(width, height, False)
            self.image.fill(colours[fill_colour])
        self.rect.size = self.image.get_size()
        self._draw_reqd = True

    def swap_colours(self):
        c = self._colour_fill
        self._colour_fill = self._colour_alt
        self._colour_alt = c
        self._draw_reqd = True

    def draw(self, force_draw=False):
        if self._draw_reqd or force_draw:
            draw_rect = self.rect.copy()
            draw_rect.topleft = (0,0)

            if self._shape == "Ellipse":
                if (self._colour_fill is not None):
                    pygame.draw.ellipse(self.image, colours[self._colour_fill], draw_rect)
                if (self._colour_line != None):
                    pygame.draw.ellipse(self.image, colours[self._colour_line], draw_rect, 3)
            elif self._shape == "Polygon":
                if self._pointlist is not None:
                    pygame.draw.polygon(self.image, colours[self._colour_fill], self._pointlist)
            else:
                if (self._colour_fill is not None):
                    pygame.draw.rect(self.image, colours[self._colour_fill], draw_rect)
                if (self._colour_line is not None):
                    pygame.draw.rect(self.image, colours[self._colour_line], draw_rect, 3)
           
            self._draw_reqd = False

### --------------------------------------------------

class Sprite_TextBox(Sprite_Shape):
    def __init__(self, name="", auto_size=True):
        super().__init__(name)
        self._text = None
        self._font = None
        self._format_string = None
        self._colour_text = None
        self._auto_size = auto_size
        self._align_horiz = 0   # -1=Left; 0=Centre; 1=Right
        self._align_vert  = 0   # -1=Top; 0=Middle; 1=Bottom

    def setup_textbox(self, width, height, text_colour="black", text_size=36, box_colours=None):
        self.colours = box_colours
        self.rect.width = width
        self.rect.height = height
        self.setup_text(text_size, text_colour)

    def setup_text(self, textsize, textcolour="black", format_string="{0}", fontfile=None, text=""):
        self.text = text
        self._font = pygame.font.Font(None, textsize)
        self.text_format = format_string
        self._colour_text = colours[textcolour]

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text):
        self._text = new_text
        self._draw_reqd = True

    @property
    def text_format(self):
        return self._format_string

    @text_format.setter
    def text_format(self, new_text_format):
        self._format_string = new_text_format

    def set_text(self, *args):
        self.text = self._format_string.format(*args)

    def draw(self, force_draw=False):
        if self._draw_reqd or force_draw:
            self.setup_shape(self.rect, [self._colour_fill])
            if self.rect.width == 0:
                self.image = self._font.render(self.text, True, self._colour_text)
                if self._auto_size:
                    self._image_size_to_rect()
            else:
                super().draw(force_draw)
                text_image = self._font.render(self.text, True, self._colour_text)
                text_rect = text_image.get_rect()
                if self._auto_size and (text_rect.width > self.rect.width or text_rect.height > self.rect.height):
                    self.rect.width = text_rect.width
                    self.rect.height = text_rect.height

                if self._align_horiz == -1:
                    text_rect.left = 0
                elif self._align_horiz == 0:
                    text_rect.centerx = self.rect.width/2
                elif self._align_horiz == 1:
                    text_rect.right = self.rect.width
                
                if self._align_vert == -1:
                    text_rect.top = 0
                elif self._align_vert == 0:
                    text_rect.centery = self.rect.height/2
                elif self._align_vert == 1:
                    text_rect.bottom = self.rect.height
                
                self.image.blit(text_image, text_rect)
            self._draw_reqd = False

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

class Sprite_ShapeSetManager(pygame.sprite.LayeredUpdates):
    def __init__(self, name, rect, relative_pos=False):
        super().__init__()
        self.name = name
        self.width = rect.width
        self.height = rect.height
        if relative_pos:
            self.offsetx = 0
            self.offsety = 0
        else:
            self.offsetx = rect.left
            self.offsety = rect.top

    def add_shape(self, sprite):
        super().add(sprite)

    def draw_shapes(self, image):
        for s in self.sprites():
            s.image = image
            s.draw(force_draw=True)

### --------------------------------------------------

class SpriteManager(pygame.sprite.LayeredUpdates):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def draw(self, surface):
        for s in self.sprites():
            s.draw()  # Ask each sprite to draw its image attribute and update rect
        super().draw(surface)

    def sprite(self, name):
        ret_sprite = None
        for s in self.sprites():
            if s.name == name:
                ret_sprite = s
        return ret_sprite

    def find_sprites_by_desc(self, attribute, value):
        ret_sprites = []
        for s in self.sprites():
            if s.get_desc(attribute) == value:
                ret_sprites.append(s)
        return ret_sprites

    def find_sprites_by_name(self, name):
        return self.find_sprites_by_desc("name", name)

    def find_sprite_by_uuid(self, uuid):
        result = self.find_sprites_by_desc("uuid", uuid)
        if len(result) == 0:
            return None
        else:
            return result[0]

    def kill_uuid(self, uuid):
        found = False
        if uuid is not None:
            s = self.find_sprite_by_uuid(uuid)
            if s is not None:
                found = True
                s.kill()
        return found

    def event(self, e):
        dealt_with = False
        if e.type == EVENT_GAME_CONTROL:
            if e.action == "MouseLeftClick" or e.action == "MouseUnclick":
                x, y = e.info['pos']
                sprite_str = self.find_click(x,y,(e.action == "MouseLeftClick"))
                dealt_with = (sprite_str != "")
            elif e.action == "KillSpriteUUID":
                self.kill_uuid(e.uuid)
                dealt_with = True
        return dealt_with

    def cleanup(self):
        pass

    def find_collisions(self):
        sprite_dict = pygame.sprite.groupcollide(self, self, False, False)
        self_collisions = []
        for spr in sprite_dict:
            sprite_dict[spr].remove(spr)
            if len(sprite_dict[spr]) == 0:
                self_collisions.append(spr)

        for spr in self_collisions:
            sprite_dict.pop(spr)

        sprite_collisions = []
        for spr, spr_list in sprite_dict.items():
            sprite_collisions.append((spr, spr_list[0].rect))

        return sprite_collisions
    
    def find_click(self, x, y, click_event=True):
        sprite_str = ""
        for s in self.sprites():
            if s.rect.collidepoint(x, y) and sprite_str == "":
                sprite_str = s.name
                if s.event_on_click != None and click_event:
                    ev = s.event_on_click
                    ev.pos = x, y
                    EventManager.post(ev)
                elif s.event_on_unclick != None and not click_event:
                    ev = s.event_on_unclick
                    ev.pos = x, y
                    EventManager.post(ev)
        return sprite_str
 
    def remove_by_class(self, sprite_class):
        for p in self.sprites():
            if type(p).__name__ == sprite_class:
                self.remove(p)

    def slow_update(self):
        for s in self.sprites():
            s.slow_update()

### --------------------------------------------------

class SpriteGroup(pygame.sprite.Group):
    def collide(self, sprite_group, dokilla=False, dokillb=False, collided=pygame.sprite.collide_mask):
        coll_dict = pygame.sprite.groupcollide(self, sprite_group, dokilla, dokillb, collided)
        # logger.debug("Collide: {0} with {1}".format("A", "B"))
        return coll_dict

### --------------------------------------------------
