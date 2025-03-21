# Test to compare greedy search against A* search in an item collection problem.

from MazeGenerator import generate_maze
from agents import GreedyItemSearch, AStarItemSearch
import time, copy

def run_agent(agent_class, grid_cells, cols, rows):
    start_time = time.process_time()
    agent = agent_class(grid_cells, grid_cells[0], cols, rows)
    total_steps = 0

    for _ in agent.generator:
        total_steps += 1
        pass  # Simulates stepping through the path
    
    end_time = time.process_time()
    return end_time - start_time, total_steps
    



def run_tests():
    sizes = {'small': 100, 'medium': 200, 'large': 400}
    items = {'five': 5, 'ten': 10, 'twenty': 20}
    results = {}

    for size_name, size in sizes.items():
        for item_name, item_number in items.items():
            tile_size = 10
            cols, rows = size, size

            grid_cells = generate_maze(size, cols, rows, tile_size, num_items=item_number)
            grid_cells2 = copy.deepcopy(grid_cells)

            # Run agents and collect completion times
            AstarTime, AstarSteps = run_agent(AStarItemSearch, grid_cells, cols, rows)
            GreedyTime, GreedySteps = run_agent(GreedyItemSearch, grid_cells2, cols, rows)

            results[size_name, item_name] = {'A* Time': AstarTime, 'Greedy Time': GreedyTime, 'A* Steps': AstarSteps, 'Greedy Steps': GreedySteps}
            print(f"Results for {size_name} maze ({cols}x{rows}) with {item_name} items:")
            print(f"A* Time: {AstarTime:.4f} seconds")
            print(f"A* Steps: {AstarSteps}")
            print(f"Greedy Time: {GreedyTime:.4f} seconds")
            print(f"Greedy Steps: {GreedySteps}\n")

    return results

if __name__ == "__main__":
    run_tests()