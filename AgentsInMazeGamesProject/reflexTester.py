from MazeGenerator import *
from agents import ReflexAgent, AdversarialAgent, MiniMaxAgent
import pygame


size = 10
tile_size = min(WIDTH // size, HEIGHT // size)
cols, rows = WIDTH // tile_size, HEIGHT // tile_size

pygame.init()
sc = pygame.display.set_mode(RES)
pygame.display.set_caption('Maze Environment - Debug Mode')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 18)  # For debug text

BACKGROUND_COLOR = (30, 30, 30)

num_enemies = 1
grid_cells = generate_maze(size, cols, rows, tile_size)
grid_cells[-1].end = False
agent = MiniMaxAgent(grid_cells, grid_cells[0], cols, rows, num_enemies)

# Debugging variables
step_number = 0
awaiting_keypress = True
agent_caught = False

def draw_debug_info():
    # Display debugging information
    info_text = [
        f"Step: {step_number}",
        "Press RIGHT ARROW to advance",
        "Press Q to quit",
        f"Agent at: ({agent.current_cell.x}, {agent.current_cell.y})",
        f"Caught: {agent_caught}"
    ]
    
    for i, text in enumerate(info_text):
        text_surface = font.render(text, True, (255, 255, 255))
        sc.blit(text_surface, (10, 10 + i * 20))

# Game loop
while True:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                # Advance the generator by one step
                awaiting_keypress = False
            elif event.key == pygame.K_q:
                pygame.quit()
                exit()
    
    # Draw maze and current state
    sc.fill(BACKGROUND_COLOR)
    for cell in grid_cells:
        cell.draw(sc)
    
    # Only advance the generator when space is pressed
    if not awaiting_keypress:
        try:
            agent.path = next(agent.generator)
            step_number += 1
        except StopIteration:
            pass  # Generator is done
        awaiting_keypress = True  # Wait for next keypress
        
    # Draw the agent and enemies
    agent.draw(sc)
    
    # Check if caught but don't exit
    if hasattr(agent, 'caught') and agent.caught and not agent_caught:
        agent_caught = True
        print(f"Agent caught at step {step_number}!")
    
    # Draw debug information
    draw_debug_info()
    
    # Update display
    pygame.display.flip()
    clock.tick(60)