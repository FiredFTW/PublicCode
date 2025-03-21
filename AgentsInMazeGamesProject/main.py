from MazeGenerator import *
from agents import *

#generate custom sized maze
try:
    size = int(input("Cells per row: "))
except:
    print("Invalid number of cells")
    exit()
tile_size = min(WIDTH // size, HEIGHT // size)
cols, rows = WIDTH // tile_size, HEIGHT // tile_size



#pygame setup
pygame.init()
sc = pygame.display.set_mode(RES)
pygame.display.set_caption('Maze Environment')
clock = pygame.time.Clock()

BACKGROUND_COLOR = (30, 30, 30)


#initialise agent
haspath = True
agentInput = input("Agent type:")


match agentInput:
    case "BFS":
        grid_cells = generate_maze(size, cols, rows, tile_size)
        agent = BFSAgent(grid_cells, grid_cells[0], grid_cells[-1], cols, rows )
    case "DFS":
        grid_cells = generate_maze(size, cols, rows, tile_size)
        agent  = DFSAgent(grid_cells, grid_cells[0], grid_cells[-1], cols, rows )
    case "UCS":
        grid_cells = generate_maze(size, cols, rows, tile_size, stepcosts=True)
        agent  = UCSAgent(grid_cells, grid_cells[0], grid_cells[-1], cols, rows )
    case "A*":
        grid_cells = generate_maze(size, cols, rows, tile_size)
        agent  = AStarAgent(grid_cells, grid_cells[0], grid_cells[-1], cols, rows )
    case "A*item":
        num_items = int(input("Number of items: "))
        grid_cells = generate_maze(size, cols, rows, tile_size, num_items=num_items)
        agent  = AStarItemSearch(grid_cells, grid_cells[0], cols, rows)
        haspath = False
    case "greedy":
        num_items = int(input("Number of items: "))
        grid_cells = generate_maze(size, cols, rows, tile_size, num_items=num_items)
        agent  = GreedyItemSearch(grid_cells, grid_cells[0], cols, rows)
        haspath = False
    case "reflex":
        num_enemies = int(input("Number of enemies: "))
        grid_cells = generate_maze(size, cols, rows, tile_size)
        grid_cells[-1].end = False
        agent  = ReflexAgent(grid_cells, grid_cells[0], cols, rows, num_enemies)
        haspath = False
        caught = False
    case "minimax":
        num_enemies = int(input("Number of enemies: "))
        grid_cells = generate_maze(size, cols, rows, tile_size)
        grid_cells[-1].end = False
        agent  = MiniMaxAgent(grid_cells, grid_cells[0], cols, rows, num_enemies)
        haspath = False
        caught = False
    case "AB":
        num_enemies = int(input("Number of enemies: "))
        grid_cells = generate_maze(size, cols, rows, tile_size)
        grid_cells[-1].end = False
        agent  = AlphaBetaAgent(grid_cells, grid_cells[0], cols, rows, num_enemies)
        haspath = False
        caught = False
    case _:
        print("Invalid agent type")
        exit()

# Game loop
while True:
    # Draw maze
    sc.fill(BACKGROUND_COLOR)
    for cell in grid_cells:
        cell.draw(sc)

    # Draw the current path
    try:
        agent.path = next(agent.generator)
    except StopIteration:
        pass
    if haspath:
        agent.draw_path(sc)
    else:
        agent.draw(sc)

    # reflex agent checks
    if hasattr(agent, 'caught'):
        if agent.caught:
            break

    # Pygame checks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.flip()
    pygame.time.delay(50)