# testing minmax agent in mazes with varying sizes and number of enemies

from MazeGenerator import generate_maze
from agents import MiniMaxAgent
import time
import random

def run_agent(agent_class, grid_cells, cols, rows, num_enemies):
    start_time = time.process_time()
    update_time = start_time
    agent = agent_class(grid_cells, grid_cells[0], cols, rows, num_enemies) 

    # First check if agent is caught immediately
    if agent.caught:
        return False, 0.0
    
    step_count = 0
    for _ in agent.generator:
        step_count += 1
        if time.process_time() - update_time > 0.5:
            update_time = time.process_time()
            print(f"Step {step_count} - Agent at ({agent.current_cell.x}, {agent.current_cell.y})")
        
        # Check for caught status AFTER processing the current step
        if agent.caught:
            print(f"Agent caught at step {step_count}")
            return False, time.process_time() - start_time
        
    if agent.caught:
        print(f"Agent caught at step {step_count}")
        return False, time.process_time() - start_time
    
    end_time = time.process_time()
    print(f"Agent successfully explored maze in {step_count} steps")
    return True, end_time - start_time

def run_tests():

    sizes = {'tiny': 10, 'small': 20, 'medium': 40}
    enemies = {'one': 1, 'two': 2, 'three': 3}

    for size_name, size in sizes.items():
        for enemy_name, enemy_number in enemies.items():
            tile_size = 10
            cols, rows = size, size
            
            print(f"\nGenerating {size_name} maze ({cols}x{rows}) with {enemy_name} enemies...")
            grid_cells = generate_maze(size, cols, rows, tile_size)
            grid_cells[-1].end = False

            complete, completion_time = run_agent(MiniMaxAgent, grid_cells, cols, rows, enemy_number)

            print(f"Results for {size_name} maze with {enemy_name} enemies:")
            if complete:
                print(f"✓ SUCCESS - Completion time: {completion_time:.4f} seconds")
            else:
                print(f"✗ FAILED - Agent caught in {completion_time:.4f} seconds")
            print("-" * 60)

if __name__ == "__main__":
    run_tests()