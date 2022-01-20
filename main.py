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

    def updateNeighbors(self, grid):
        self.neighbors = []
        # Down
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].borderSquare():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Up
        if self.row < 0 and not grid[self.row - 1][self.col].borderSquare():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].borderSquare():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].borderSquare():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


##########################################
# GRID 
##########################################
def drawGrid(num_rows, num_cols, screen_width, screen_height):
    """Creates a grid of squares."""

    grid = [] # A multidimensional array that consists of squares
    height_square = screen_height // num_rows # Height of square
    width_square = screen_width // num_cols # Width of square

    # Create a multidimensional array to store the squares
    for x in range(num_rows):
        grid.append([]) # Add row
        for y in range(num_cols):
            # Add columns
            square = Square(x, y, width_square, height_square, num_rows)
            grid[x].append(square)
    return grid

def drawGridLines(screen, screen_width, screen_height, num_rows, num_cols):
    """Adds grid lines to the grid"""

    # Calculate the gap measurements for each axis
    x_gap = screen_width // num_cols
    y_gap = screen_height // num_rows
    # Find and create the grid lines
    for i in range(num_rows):
        pygame.draw.line(screen, BLACK, (0, i*y_gap), (screen_width, i*y_gap))
        for j in range(num_cols):
            pygame.draw.line(screen, BLACK, (j*x_gap, 0), (j*x_gap, screen_width))

def draw(screen, screen_width, screen_height, grid, num_rows, num_cols):
    """Creates the grid by drawing a square for every position."""

    # Pygame good practice to fill the window with white
    screen.fill(WHITE)

    # Draw the sqaures in each position
    for row in grid:
        for square in row:
            # Draw square one the grid
            square.drawSquare(screen)

    drawGridLines(screen, screen_width, screen_height, num_rows, num_cols)
    pygame.display.update()

##########################################
# MOUSE 
##########################################
def getClickedPosition(cursor_pos, rows, cols, screen_width, screen_height):
    """Returns the x and y position of the cursor."""

    # Calculate the grid squares
    x_gap = screen_width // cols
    y_gap = screen_height // rows
    # Grab the cursor position from pygame.get_pos()
    x, y = cursor_pos
    # Find the position of the cursor
    row = x // x_gap
    col = y // y_gap
    return row, col

##########################################
# ALGORITHM
##########################################
def hCost(p1, p2):
    """Finds the distance from the end node."""

    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def aStar(draw, grid, startpoint, endpoint):
    count = 0
    # The set of discovered squares that may need to be (re-)expanded.
    # Initially, only the start node is known.
    open_set = PriorityQueue()
    open_set.put(0, count, startpoint)
    # Previously explored square
    came_from = {}
    # Find G-Cost and H-Cost
    g_cost = {square: float("inf") for row in grid for square in row}
    g_cost[startpoint] = 0
    f_cost = {square: float("inf") for row in grid for square in row}
    f_cost[startpoint] = hCost(startpoint.getPosition(), endpoint.getPosition())

    open_set_hash = {startpoint}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == endpoint:
            reconstruct_path(came_from, endpoint, draw)
            endpoint.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_cost = g_cost[current] + 1

            if temp_g_cost < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = temp_g_cost
                f_cost[neighbor] = temp_g_cost + hCost(neighbor.getPosition(), endpoint.getPosition())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_cost[neighbor]), count, neighbor)
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != startpoint:
            current.make_closed()

    return False

def main(screen, screen_width, screen_height):
    ROWS = 30
    COLS = 30
    grid = drawGrid(ROWS, COLS, screen_width, screen_height)

    startpoint = None
    endpoint = None

    program = True
    while program:
        draw(screen, screen_width, screen_height, grid, ROWS, COLS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program = False

            # LEFT CLICK
            if pygame.mouse.get_pressed()[0]:
                cursor_pos = pygame.mouse.get_pos()
                row, col = getClickedPosition(cursor_pos, ROWS, COLS, screen_width, screen_height)
                clicked_square = grid[row][col]
                # Sets the startpoint
                if not startpoint and clicked_square != endpoint:
                    startpoint = clicked_square
                    startpoint.setStartpoint()
                # Sets the endpoint
                elif not endpoint and clicked_square != startpoint:
                    endpoint = clicked_square
                    endpoint.setEndpoint()
                # Sets the border
                elif clicked_square != endpoint and clicked_square != startpoint:
                    clicked_square.setBorder()
            # RIGHT CLICK 
            elif pygame.mouse.get_pressed()[2]:
                cursor_pos = pygame.mouse.get_pos()
                row, col = getClickedPosition(cursor_pos, ROWS, COLS, screen_width, screen_height)
                clicked_square = grid[row][col]
                clicked_square.resetSquare()
                if clicked_square == startpoint:
                    startpoint = None
                elif clicked_square == endpoint:
                    endpoint = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and startpoint and endpoint:
                    for row in grid:
                        for square in row:
                            square.updateNeighbors(grid)

                    aStar(lambda: draw(screen,screen_width,screen_height, grid, ROWS, COLS), grid, startpoint, endpoint)

                if event.key == pygame.K_c:
                    startpoint = None
                    endpoint = None
                    grid = make_grid(ROWS, screen_width)

    pygame.quit()

if __name__ == '__main__':
    main(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)
