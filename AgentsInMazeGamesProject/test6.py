# test to compare the performance of Reflex, MiniMax, and AlphaBeta agents.

from MazeGenerator import generate_maze
from agents import MiniMaxAgent, ReflexAgent, AlphaBetaAgent, ExpectiMaxAgent
import time, copy, random

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
            visited_percentage = sum(1 for cell in grid_cells if cell.visited) / len(grid_cells) * 100
            print(f"Agent caught at step {step_count} at {visited_percentage:.2f}% completion")
            return False, time.process_time() - start_time
        
    if agent.caught:
            visited_percentage = sum(1 for cell in grid_cells if cell.visited) / len(grid_cells) * 100
            print(f"Agent caught at step {step_count} at {visited_percentage:.2f}% completion")
            return False, time.process_time() - start_time
    
    end_time = time.process_time()
    print(f"Agent successfully explored maze in {step_count} steps")
    return True, end_time - start_time

def run_tests():

    print("10x10 maze with 1 enemy:")
    maze1 = generate_maze(10, 10, 10, 10)
    maze1[-1].end = False
    maze2 = copy.deepcopy(maze1)
    maze3 = copy.deepcopy(maze1)
    maze4 = copy.deepcopy(maze1)

    print("\nReflex Agent:")
    run_agent(ReflexAgent, maze1, 10, 10, 1)
    print("\nMiniMax Agent:")
    run_agent(MiniMaxAgent, maze2, 10, 10, 1)
    print("\nAlphaBeta Agent:")
    run_agent(AlphaBetaAgent, maze3, 10, 10, 1)
    print("\nExpectiMax Agent:")
    run_agent(ExpectiMaxAgent, maze4, 10, 10, 1)

    print("-" * 60)

    print("20x20 maze with 2 enemies:")
    maze1 = generate_maze(20, 20, 20, 10)
    maze1[-1].end = False
    maze2 = copy.deepcopy(maze1)
    maze3 = copy.deepcopy(maze1)
    maze4 = copy.deepcopy(maze1)

    print("\nReflex Agent:")
    run_agent(ReflexAgent, maze1, 20, 20, 2)
    print("\nMiniMax Agent:")
    run_agent(MiniMaxAgent, maze2, 20, 20, 2)
    print("\nAlphaBeta Agent:")
    run_agent(AlphaBetaAgent, maze3, 20, 20, 2)
    print("\nExpectiMax Agent:")
    run_agent(ExpectiMaxAgent, maze4, 20, 20, 2)

    print("-" * 60)

    print("40x40 maze with 3 enemies:")
    maze1 = generate_maze(40, 40, 40, 10)
    maze1[-1].end = False
    maze2 = copy.deepcopy(maze1)
    maze3 = copy.deepcopy(maze1)
    maze4 = copy.deepcopy(maze1)

    print("\nReflex Agent:")
    run_agent(ReflexAgent, maze1, 40, 40, 3)
    print("\nMiniMax Agent:")
    run_agent(MiniMaxAgent, maze2, 40, 40, 3)
    print("\nAlphaBeta Agent:")
    run_agent(AlphaBetaAgent, maze3, 40, 40, 3)
    print("\nExpectiMax Agent:")
    run_agent(ExpectiMaxAgent, maze4, 40, 40, 3)

    print("-" * 60)

    print("50x50 maze with 4 enemies:")
    maze1 = generate_maze(50, 50, 50, 10)
    maze1[-1].end = False
    maze2 = copy.deepcopy(maze1)
    maze3 = copy.deepcopy(maze1)
    maze4 = copy.deepcopy(maze1)

    print("\nReflex Agent:")
    run_agent(ReflexAgent, maze1, 50, 50, 4)
    print("\nMiniMax Agent:")
    run_agent(MiniMaxAgent, maze2, 50, 50, 4)
    print("\nAlphaBeta Agent:")
    run_agent(AlphaBetaAgent, maze3, 50, 50, 4)
    print("\nExpectiMax Agent:")
    run_agent(ExpectiMaxAgent, maze4, 50, 50, 4)




if __name__ == "__main__":
    run_tests()