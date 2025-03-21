#test to evaluate UCS agent efficiency vs other agents in varying maze sizes

from MazeGenerator import generate_maze
from agents import BFSAgent, DFSAgent, UCSAgent


def run_agent_and_get_cost(agent_class, grid_cells, cols, rows):

    agent = agent_class(grid_cells, grid_cells[0], grid_cells[-1], cols, rows)
    
    final_path = None
    for path in agent.generator:
        final_path = path

    
    return sum(cell.step_cost for cell in final_path)
   

    

def run_tests():
    sizes = {'small': 100, 'medium': 200, 'large': 400}
    results = {}

    for size_name, size in sizes.items():
        tile_size = 10
        cols, rows = size,size

        grid_cells = generate_maze(size, cols, rows, tile_size)

        # Run agents and collect total path costs
        bfs_cost = run_agent_and_get_cost(BFSAgent, grid_cells, cols, rows)
        dfs_cost = run_agent_and_get_cost(DFSAgent, grid_cells, cols, rows)
        ucs_cost = run_agent_and_get_cost(UCSAgent, grid_cells, cols, rows)

        results[size_name] = {'BFS': bfs_cost, 'DFS': dfs_cost, 'UCS': ucs_cost}
        print(f"Results for {size_name} maze ({cols}x{rows}):")
        print(f"BFS Total Path Cost: {bfs_cost}")
        print(f"DFS Total Path Cost: {dfs_cost}")
        print(f"UCS Total Path Cost: {ucs_cost}\n")

    return results

if __name__ == "__main__":
    run_tests()