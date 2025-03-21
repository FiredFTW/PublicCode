# Test to compare hueristic functions in A* 4-corners search.

from MazeGenerator import generate_maze
from agents import AStarFourCornersAgent
import time

def run_agent(agent_class, grid_cells, cols, rows):
    start_time = time.process_time()
    agent = AStarFourCornersAgent(grid_cells, grid_cells[0], grid_cells[-1], cols, rows, agent_class)
    
    for _ in agent.generator:
        pass  # Simulates stepping through the path
    
    end_time = time.process_time()
    return end_time - start_time
    

def run_tests():
    sizes = {'small': 100, 'medium': 200, 'large': 400, 'massive': 800}
    results = {}

    for size_name, size in sizes.items():
        tile_size = 10
        cols, rows = size, size

        grid_cells = generate_maze(size, cols, rows, tile_size)

        # Run agents and collect completion times
        sum_heuristic = run_agent("sum", grid_cells, cols, rows)
        max_heuristic = run_agent("max", grid_cells, cols, rows)

        results[size_name] = {'Sum Heuristic': sum_heuristic, 'Max Distance Heuristic': max_heuristic}
        print(f"Results for {size_name} maze ({cols}x{rows}):")
        print(f"Sum Heuristic: {sum_heuristic:.4f} seconds")
        print(f"Max Distance Heuristic: {max_heuristic:.4f} seconds\n")

    return results

if __name__ == "__main__":
    run_tests()