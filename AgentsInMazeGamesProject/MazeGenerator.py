import pygame
from random import choice
import random

RES = WIDTH, HEIGHT = 1202, 902

class Cell:
    def __init__(self, x, y, tile_size):
        self.x, self.y = x, y
        self.tile_size = tile_size
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.step_cost = 1
        self.visited = False
        self.thickness = 4
        self.start = False
        self.end = False
        self.item = False

    def draw(self, sc):
        x, y = self.x * self.tile_size, self.y * self.tile_size

        # Visualise step cost with red shading
       
            
        # Draw the cell as a filled rectangle for start and end cells
        if self.start:
            pygame.draw.rect(sc, pygame.Color('green'), (x + self.thickness, y + self.thickness,
                                                         self.tile_size - 2 * self.thickness,
                                                         self.tile_size - 2 * self.thickness))
        elif self.end:
            pygame.draw.rect(sc, pygame.Color('red'), (x + self.thickness, y + self.thickness,
                                                         self.tile_size - 2 * self.thickness,
                                                         self.tile_size - 2 * self.thickness))
        elif self.item:
            pygame.draw.rect(sc, pygame.Color('orange'), (x + self.thickness, y + self.thickness,
                                                         self.tile_size - 2 * self.thickness,
                                                         self.tile_size - 2 * self.thickness))
        elif self.visited:
            pygame.draw.rect(sc, pygame.Color(100, 100, 100), (x + self.thickness, y + self.thickness,
                                                         self.tile_size - 2 * self.thickness,
                                                         self.tile_size - 2 * self.thickness))
        else:
            match self.step_cost:
                case 1: colour = 30, 30, 30
                case 2: colour = 100, 0, 0
                case 3: colour = 200, 0, 0
            pygame.draw.rect(sc, colour, (x + self.thickness, y + self.thickness,
                                             self.tile_size - 2 * self.thickness,
                                             self.tile_size - 2 * self.thickness))
            
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color(200,200,200), (x, y), (x + self.tile_size, y), self.thickness)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color(200,200,200), (x + self.tile_size, y), (x + self.tile_size, y + self.tile_size), self.thickness)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color(200,200,200), (x + self.tile_size, y + self.tile_size), (x, y + self.tile_size), self.thickness)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color(200,200,200), (x, y + self.tile_size), (x, y), self.thickness)

    def check_cell(self, x, y, cols, rows, grid_cells):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells, cols, rows):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, cols, rows, grid_cells)
        right = self.check_cell(self.x + 1, self.y, cols, rows, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, cols, rows, grid_cells)
        left = self.check_cell(self.x - 1, self.y, cols, rows, grid_cells)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
    
    def collect(self):
        self.item = False
    

def remove_walls(current, next):
    dx = current.x - next.x
    dy = current.y - next.y

    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    elif dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False


def remove_random_walls(grid_cells, cols, rows, removal_chance=0.1):
    # randomly remove walls between adjacent cells to introduce more branching and variation in pathing

    for cell in grid_cells:
        x, y = cell.x, cell.y


        neighbors = {
        'top': (x, y - 1),
        'right': (x + 1, y),
        'bottom': (x, y + 1),
        'left': (x - 1, y)
    }
        
        for direction, (nx, ny) in neighbors.items():
            if 0 <= nx < cols and 0 <= ny < rows and random.random() < removal_chance:
                neighbor = cell.check_cell(nx, ny, cols, rows, grid_cells)
                if neighbor:
                    # Remove the walls between current cell and its neighbor

                    match direction:
                        case 'top':
                            cell.walls['top'] = False
                            neighbor.walls['bottom'] = False
                        case 'bottom':
                            cell.walls['bottom'] = False
                            neighbor.walls['top'] = False
                        case 'right':
                            cell.walls['right'] = False
                            neighbor.walls['left'] = False
                        case 'left':
                            cell.walls['left'] = False
                            neighbor.walls['right'] = False


def assign_step_costs(grid_cells):
    step_costs = [1, 2, 3]
    probabilities = [0.7, 0.2, 0.1]  

    for cell in grid_cells:
        if not cell.start and not cell.end:
            cell.step_cost = random.choices(step_costs, probabilities)[0]  

def add_items(grid_cells, num_items = 10):
    items_cells = random.sample(grid_cells[1:], min(num_items, len(grid_cells) - 2))
    for cell in items_cells:
        cell.item = True

def generate_maze(size, cols, rows, tile_size, stepcosts = False, num_items = None):
    
    # Create a grid of cells
    grid_cells = [Cell(col, row, tile_size) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    array = []
    break_count = 1

    # Set start and end cells
    start_cell = grid_cells[0]  # Top-left corner
    end_cell = grid_cells[-1]  # Bottom-right corner
    end_cell.end = True
    if num_items:
        end_cell.end = False

    while break_count != len(grid_cells):
        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells, cols, rows)
        if next_cell:
            next_cell.visited = True
            break_count += 1
            array.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif array:
            current_cell = array.pop()

     # Add randomness to the maze by removing some walls
    remove_random_walls(grid_cells, cols, rows, removal_chance=0.1)
    # Assign step costs to all cells from 1-5
    if stepcosts:   
        assign_step_costs(grid_cells)

    # Add items to the maze
    if num_items:
        add_items(grid_cells, num_items)

    for cell in grid_cells:
        cell.visited = False

    return grid_cells



