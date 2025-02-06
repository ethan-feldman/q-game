from PIL import Image, ImageDraw, ImageColor, ImageFont
import math
from enum import Enum

'''
Color is one of: "red", "green", "blue", "yellow", "orange", "purple".
'''
class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    YELLOW = 'yellow'
    ORANGE = 'orange'
    PURPLE = 'purple'

'''
Shape is one of: "star", "8star", "square", "circle", "clover", "diamond".
'''
class Shape(Enum):
    STAR = 'star'
    EIGHT_STAR = '8star'
    SQUARE = 'square'
    CIRCLE = 'circle'
    CLOVER = 'clover'
    DIAMOND = 'diamond'


'''
Represents a position as an x and y coordinate.
'''
class Position:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def get_x(self):
        return self._x
    
    @property
    def get_y(self):
        return self._y

    def __add__(self, other):
        return Position(self._x + other._x, self._y + other._y)

    def __sub__(self, other):
        return Position(self._x - other._x, self._y - other._y)

    def __str__(self):
        return "(" + str(self._x) + ", " + str(self._y) + ")"
    def __repr__(self):
        return "(" + str(self._x) + ", " + str(self._y) + ")"

    def __eq__(self, other):
        return (self._x, self._y) == (other._x, other._y)
    
    def __hash__(self):
        return hash((self._x, self._y))

    def __lt__(self, other):
        if (self._y < other._y):
            return True
        elif (self._y == other._y):
            return self._x < other._x
        else:
            return False
        
    
    def __gt__(self, other):
        if (self._y > other._y):
            return True
        elif (self._y == other._y):
            return self._x > other._x
        else:
            return False

    ''' 
    Computes positional neighbors of this position. (Left, Right, Up, & Down)
    '''
    def get_neighbors(self):
        neighbors = []
        UP_DOWN_RIGHT_LEFT = (Position(-1, 0), Position(1, 0), Position(0, -1), Position(0, 1))
        for direction_posn in UP_DOWN_RIGHT_LEFT:
            neighbor_posn = self + direction_posn
            neighbors.append(neighbor_posn)
        return neighbors
        

'''Represents the tile in a game map of Q.'''
class Tile:
    color_order = {Color.RED: 1, Color.GREEN: 2, Color.BLUE: 3, Color.YELLOW: 4, Color.ORANGE: 5, Color.PURPLE: 6}
    shape_order = {Shape.STAR: 1, Shape.EIGHT_STAR: 2, Shape.SQUARE: 3, Shape.CIRCLE: 4, Shape.CLOVER: 5, Shape.DIAMOND: 6}

    def __init__(self, color, shape):
        self._color = color
        self._shape = shape

    @property
    def get_color(self):
        return self._color
    
    @property
    def get_shape(self):
        return self._shape

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.get_color == other.get_color and self.get_shape == other.get_shape
        return False
    
    '''
    Compares using shape and color ordering. Shape order is dominant.
    '''
    def __lt__(self, other):
        self_shape = self.shape_order[self._shape]
        other_shape = self.shape_order[other._shape]
        
        if (self_shape < other_shape):
            return True
        elif (self_shape == other_shape):
            return self.color_order[self._color] < self.color_order[other._color]
        else:
            return False
    
    '''
    Compares using shape and color ordering. Shape order is dominant.
    '''
    def __gt__(self, other):
        self_shape = self.shape_order[self._shape]
        other_shape =  self.shape_order[other._shape]
        
        if (self_shape > other_shape):
            return True
        elif (self_shape == other_shape):
            return  self.color_order[self._color] >  self.color_order[other._color]
        else:
            return False
        
    def __str__(self):
        return "Tile(" + str(self._color) + ", " + str(self._shape) + ")"
    def __repr__(self):
        return "Tile(" + str(self._color) + ", " + str(self._shape) + ")"
        
        
'''Represents the game map of Q.'''
class GameMap:
    '''
    Initializes a GameMap with the referee tile placed at (0, 0).
    '''
    def __init__(self, referee_tile = None, tiles= None):
        
        if tiles == None:
         self._tiles = {Position(0, 0): referee_tile}
        else:
            self._tiles = tiles

        
    def get_tiles(self):
        return self._tiles
    '''
    Adds a tile to the map at (x, y) if adjacent to an existing tile. Returns True if successful,
    False otherwise.
    '''
    def add_tile(self, position, tile):
        if position in self._tiles.keys():  # assuming self.tiles is a hashmap with keys as positions and values as tiles
            raise Exception(f'A tile already exists at position {position},{self.get_tiles()}')
        if not (self.check_shares_side(position)):
            raise Exception('tile to be added does not share side with another tile.')
        
        self._add_tile_workhorse(position, tile)
        return True
        
    '''
    Directly places a tile on the map in the given position.
    '''
    def _add_tile_workhorse(self, position, tile):
        self._tiles[position] = tile


    ''' 
    Checks if any tile is adjacent to (x, y). Returns True if there is an adjacent tile, False otherwise. 
    '''
    def check_shares_side(self, position):
        return any(key in position.get_neighbors() for key in self._tiles.keys())

    

    '''
    Returns a list of positions where the tile can be placed on this map.
    '''
    def get_possible_insertions(self, tile):
        possible_insertions = set()
        for tile_position in self._tiles.keys():
            for neighbor_posn in tile_position.get_neighbors():
                if neighbor_posn not in self._tiles.keys() and self.check_rules(neighbor_posn, tile):
                    possible_insertions.add(neighbor_posn)
        return possible_insertions
    
    '''
    Checks if a tile can be added at (x, y) according to the game rules. Returns a boolean.
    '''
    def check_rules(self, position, tile):
        for neighbor_posn in position.get_neighbors():
            adjacent_tile = self._tiles.get(neighbor_posn) 
            if(adjacent_tile):
                if not (adjacent_tile._color == tile._color or adjacent_tile._shape == tile._shape):
                    return False
        return True

    """ 
    Checks if the placements share the same row or column.
    """
    def check_tiles_same_row_or_col(self, placements):
        rows = []
        cols = []
        for placement in placements:
            rows.append(placement[0].get_y)
            cols.append(placement[0].get_x)
        if len(set(rows)) == 1 or len(set(cols)) == 1:
            return True
        return False
    
    '''
    Returns a list of positions where the tile can be placed on this map, but includes previous placements so that the list only returns positions
    that exist in the row or column of the other tiles
    '''
    def restrict_possible_insertions(self, tile, prev_placements):
        possible_insertions = self.get_possible_insertions(tile)
        restricted_insertions = []
        for insertion in possible_insertions:
            if (self.check_tiles_same_row_or_col(prev_placements + [(insertion, tile)])):
                restricted_insertions.append(insertion)
        return restricted_insertions
    


    def render(self, x, y, draw, shape_size):
        render_border(draw, x, y)
        for position in self._tiles.keys():
            tile = self._tiles[position]
            render_tile(draw, tile, x + position._x * shape_size + 175, y + position._y * shape_size + 195, shape_size, ImageColor.getrgb(tile._color.value))
            render_coordinates(draw, position._x, position._y, shape_size, x + position._x * shape_size + 175, y + position._y * shape_size + 195)

    def get_dimensions(self):
        max_x = 0
        max_y = 0
        min_x = 0
        min_y = 0 
        for position in self._tiles.keys():
            if position._x > max_x:
                max_x = position._x

            if position._x < min_x:
                min_x = position._x

            if position._y > max_y:
                max_y = position._y

            if position._y < min_y:
                min_y = position._y
        return (min_x, max_x, min_y, max_y)

class GameMapBuilder:
    def __init__(self):
        self.tiles = {}
        self.referee_tile = None
        
    def build(self):
        return GameMap(None, tiles=self.tiles)
    
    def add_tile(self, position, tile):
        self.tiles[position] = tile
        return self



def render_tile(draw, tile, x, y, shape_size, shade):
        shape_functions = {
            "star": render_4star,
            "8star": render_8star,
            "square": render_square,
            "circle": render_circle,
            "diamond": render_diamond,
            "clover": render_clover
        }
        shape_functions[tile._shape.value](draw, x, y, shape_size, shade)

def render_border(draw, x, y):
    draw.rectangle([x, y, x + 350, y + 350], outline='black')

def render_star(draw_obj, x, y, shape_size, shade, points):
    radius_outer = shape_size / 2
    radius_inner = radius_outer / 2.5
    angle_step = 360.0 / points
    angles = [i * angle_step for i in range(points)]

    star_points = []
    for i, angle in enumerate(angles):
        if i % 2 == 0:
            r = radius_outer
        else:
            r = radius_inner
        star_points.append((x + radius_outer + r * math.cos(math.radians(angle)),
                            y + radius_outer + r * math.sin(math.radians(angle))))
    draw_obj.polygon(star_points, fill=shade)
    draw_obj.rectangle([x, y, x + shape_size, y + shape_size], outline='black')

def render_8star(draw_obj, posX, posY, shape_size,shade):
    render_star(draw_obj, posX, posY, shape_size, shade, 16)


def render_4star(draw_obj, posX, posY, shape_size, shade):
    render_star(draw_obj, posX, posY, shape_size, shade, 8)


def render_square(draw_obj, x, y, shape_size,shade):
    draw_obj.rectangle([x, y, x + shape_size, y + shape_size], fill=shade)
    draw_obj.rectangle([x, y, x + shape_size, y + shape_size], outline='black')


def render_circle(draw_obj, x, y, shape_size,  shade):
    draw_obj.ellipse([x, y, x + shape_size, y + shape_size], fill=shade)
    draw_obj.rectangle([x, y, x + shape_size, y + shape_size], outline='black')


def render_diamond(draw_obj, x, y, shape_size, shade):
    radius = shape_size / 2
    angles = [0, 90, 180, 270]
    points = [(x + radius + radius * math.cos(math.radians(angle)),
               y + radius + radius * math.sin(math.radians(angle))) for angle in angles]
    
    draw_obj.polygon(points, fill=shade)
    draw_obj.rectangle([x, y, x + shape_size, y + shape_size], outline='black')

def render_clover(draw_obj, x, y, shape_size, shade):
    draw_obj.rectangle([x + (shape_size / 4), y + (shape_size / 4), x + shape_size - (shape_size / 4), y + shape_size - (shape_size / 4)], fill=shade)
    draw_obj.chord([(x, y + (shape_size / 4)), (x + (shape_size / 2), y + (shape_size / 4 * 3))], 90, 270, fill=shade)
    draw_obj.chord([(x + (shape_size / 4), y), (x + (shape_size / 4 * 3), y + (shape_size / 2))], 180, 360, fill=shade)
    draw_obj.chord([(x + (shape_size / 2), y + (shape_size / 4)), (x + shape_size, y + (shape_size / 4 * 3))], 270, 90, fill=shade)
    draw_obj.chord([(x + (shape_size / 4), y + (shape_size / 2)), (x + (shape_size / 4 * 3), y + shape_size)], 0, 180, fill=shade)
    draw_obj.rectangle([x, y, x + shape_size, y + shape_size], outline='black')

def render_coordinates(draw_obj, render_x, render_y, shape_size, x, y): 
    font_size = int(shape_size / 3)
    font = ImageFont.truetype("/Q/Common/Other/Arial.ttf", font_size)
    draw_obj.text((x + (shape_size / 7) ,  y + (shape_size/4)), "(" + str(render_x) + ", " + str(render_y) + ")", fill='black', font=font)
    
def generate_each_tile_type():
    """Generate one tile of each type (based on combinations of colors and shapes).
    """
    tiles = []
    for each_color in Color:
        for each_shape in Shape:
            tiles.append(Tile(each_color, each_shape))
    return tiles
