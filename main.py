import pygame
import math
from queue import PriorityQueue

# Window settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('A* Pathfinding Visualizer')

# Colours for the squares. Each indicating a state
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGREY = (24,24,24)
LIGHTGREY = (66,66,66)
MOONRED = (255, 0, 0)
GREEN = (13,55,13)
BLUE = (0, 255, 0)
PURPLE = (128, 165, 0)
TURQUOISE = (64, 224, 208)

class Square:
    """The individual square in each grid."""

    def __init__(self, row, col, width, height, total_rows):
        self.row = row # Row on grid
        self.col = col # Column on grid
        self.x = row * width # x-coordinate
        self.y = col * width # y-coordinate
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.height = height
        self.total_rows = total_rows

    def getPosition(self):
        return self.row, self.col

    # -------------------------- Square State --------------------------
    def exploredSquare(self):
        """Check if the square has been considered."""
        return self.color == DARKGREY

    def unexploredSquare(self):
        """Checks if the square open for consideration."""
        return self.color == WHITE

    def borderSquare(self):
        """Check if the square is traversable."""
        return self.color == BLACK

    def startpoint(self):
        """Starting point for the A*"""
        return self.color == GREEN

    def endpoint(self):
        return self.color == BLUE

    def resetSquare(self):
        """Reset an invalid (red) square to a valid (white) square"""
        self.color = WHITE

    # -------------------------- Manipulate Square State --------------------------

    def setExplored(self):
        self.color = DARKGREY

    def setUnexplored(self):
        self.color = WHITE

    def setBorder(self):
        self.color = BLACK

    def setStartpoint(self):
        self.color = GREEN

    def setEndpoint(self):
        self.color = BLUE

    def setPath(self):
        """Create a path from the startpoint to the endpoint."""
        self.color = MOONRED

    def drawSquare(self, screen):
        """Draw the square on the window."""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def updateNeighbors(self):
        pass

    def __lt__(self):
        """Operator overload / unary predicate"""
        pass


def drawGrid(num_rows, num_cols, screen_width, screen_height):
    """Creates a grid of squares."""

    grid = [] # A multidimensional array that consists of squares
    height_square = screen_height // num_rows # Height of square
    width_square = screen_width // num_cols # Width of square
    for x in range(num_rows):
        grid.append([]) # Add row
        for y in range(num_cols):
            # Add columns
            square = Square(x, y, width_square, height_square, num_rows)
            grid[x].append(square)
    return grid

def drawGridLines(screen, screen_width, screen_height, num_rows, num_cols):
    """Adds grid lines to the grid"""

    x_gap = screen_width // num_cols
    y_gap = screen_height // num_rows
    for i in range(num_rows):
        # TODO: CHANGE
        pygame.draw.line(screen, BLACK, (0, i*y_gap), (screen_width, i*y_gap))
        for j in range(num_cols):
            pygame.draw.line(screen, BLACK, (j*x_gap, 0), (j*x_gap, screen_width))

def draw(screen, screen_width, screen_height, grid, num_rows, num_cols):
    """Creates the grid by drawing a square for every position."""
    screen.fill(WHITE)

    # START HERE
    for row in grid:
        for square in row:
            # Draw square one the grid
            square.drawSquare(screen)

    drawGridLines(screen, screen_width, screen_height, num_rows, num_cols)
    pygame.display.update()

def getClickedPosition():
    """Returns the x and y position of the cursor."""
    return get_pos()

def hCost(start):
    """Finds the distance from the end node."""

    pass

def gCost(end):
    """Finds the distance from the start node."""
    pass

def fCost():
    """Finds the optimal square to traverse."""
    pass

def main(screen, screen_width, screen_height):
    ROWS = 30
    COLS = 30
    grid = drawGrid(ROWS, COLS, screen_width, screen_height)

    start = None
    end = None

    while True:
        draw(screen, screen_width, screen_height, grid, ROWS, COLS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    main(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)
