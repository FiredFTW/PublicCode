#Test to compare the performance of BFS and DFS in simple mazes of varing sizes

import time
from MazeGenerator import generate_maze
from agents import BFSAgent, DFSAgent, AStarAgent

def run_agent(agent_class, grid_cells, cols, rows):
    start_time = time.time()
    agent = agent_class(grid_cells, grid_cells[0], grid_cells[-1], cols, rows)

    
    for _ in agent.generator:
        pass  # Simulates stepping through the path
    
    end_time = time.time()
    return end_time - start_time

def run_tests():
    sizes = {'small': 100, 'medium': 200, 'large': 400}  
    results = {}

    for size_name, size in sizes.items():
        tile_size = 10
        cols, rows = size, size
        
        grid_cells = generate_maze(size, cols, rows, tile_size)

        bfs_time = run_agent(BFSAgent, grid_cells, cols, rows)
        dfs_time = run_agent(DFSAgent, grid_cells, cols, rows)
        Astar_time = run_agent(AStarAgent, grid_cells, cols, rows)

        results[size_name] = {'BFS': bfs_time, 'DFS': dfs_time, 'A*': Astar_time}
        print(f"Results for {size_name} maze ({cols}x{rows}):")
        print(f"BFS: {bfs_time:.4f} seconds")
        print(f"DFS: {dfs_time:.4f} seconds")
        print(f"A*: {Astar_time:.4f} seconds\n")


if __name__ == "__main__":
    run_tests()
