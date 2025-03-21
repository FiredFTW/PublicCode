import time
from MazeGenerator import generate_maze
from agents import AStarAgent

def run_agent(agent_class, heuristic, grid_cells, cols, rows):
    start_time = time.time()
    agent = agent_class(grid_cells, grid_cells[0], grid_cells[-1], cols, rows, heuristic=heuristic)

    # Simulate stepping through the path
    for _ in agent.generator:
        pass

    end_time = time.time()
    return end_time - start_time

def run_tests():
    sizes = {"small": 100, "medium": 200, "large": 400, "massive": 800}
    results = {}
    heuristics = ["manhattan", "euclidean", "chebyshev", "diagonal"]

    for size_name, size in sizes.items():
        tile_size = min(1202 // size, 902 // size)
        cols, rows = 1202 // tile_size, 902 // tile_size
        grid_cells = generate_maze(size, cols, rows, tile_size)

        results[size_name] = {}
        for h in heuristics:
            time_taken = run_agent(AStarAgent, h, grid_cells, cols, rows)
            results[size_name][h] = time_taken
            print(f"{h} heuristic on {size_name} maze ({size}x{size}): {time_taken:.4f} seconds")
        print()

    return results

if __name__ == "__main__":
    run_tests()
