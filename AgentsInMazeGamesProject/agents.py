import pygame
from collections import deque
import heapq
import itertools
import math
import random


class BaseAgent:
    def __init__(self, maze, start, end, cols, rows):
        self.maze = maze
        self.start = start
        self.end = end
        self.cols = cols
        self.rows = rows
        self.path = [self.maze[0]]

    def get_neighbors(self, cell):
        neighbors = []
        x, y = cell.x, cell.y

        # Check each direction, ensuring walls are not blocking
        if not cell.walls['top']:
            neighbors.append(self.get_cell(x, y - 1))
        if not cell.walls['right']:
            neighbors.append(self.get_cell(x + 1, y))
        if not cell.walls['bottom']:
            neighbors.append(self.get_cell(x, y + 1))
        if not cell.walls['left']:
            neighbors.append(self.get_cell(x - 1, y))

        return [n for n in neighbors if n]

    def get_cell(self, x, y):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            index = x + y * self.cols
            return self.maze[index]
        return None

    def draw_path(self, sc):
        for cell in self.path:
            x, y = cell.x * cell.tile_size, cell.y * cell.tile_size
            pygame.draw.rect(sc, pygame.Color('blue'), (x + cell.thickness, y + cell.thickness, cell.tile_size 
                                                        - cell.thickness, cell.tile_size - cell.thickness))



class BFSAgent(BaseAgent):
    def __init__(self, maze, start, end, cols, rows):
        super().__init__(maze, start, end, cols, rows)
        self.generator = self.bfs()


    def bfs(self):
        queue = deque([(self.start, [])])
        visited = set()
        visited.add(self.start)

        while queue:
            current_cell, path = queue.popleft()
            new_path = path + [current_cell]

            if current_cell == self.end:
                yield new_path  # Yield the complete path to the end
                return  

            # Explore neighbors
            neighbors = self.get_neighbors(current_cell)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, new_path))
                    yield new_path  # Yield intermediate path

        yield []  

class DFSAgent(BaseAgent):
    def __init__(self, maze, start, end, cols, rows):
        super().__init__(maze, start, end, cols, rows)
        self.generator = self.dfs()


    def dfs(self):
        stack = [(self.start, [])]
        visited = set()
        visited.add(self.start)

        while stack:
            current_cell, path = stack.pop()
            new_path = path + [current_cell]

            if current_cell == self.end:
                yield new_path  # Yield the complete path to the end
                return  

            # Explore neighbors
            neighbors = self.get_neighbors(current_cell)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, new_path))
                    yield new_path  # Yield intermediate path

        yield []  


class UCSAgent(BaseAgent):
    def __init__(self, maze, start, end, cols, rows):
        super().__init__(maze, start, end, cols, rows)
        self.generator = self.uniform_cost()
        self.counter = itertools.count() #counter used for tie-breaking in pq

    def uniform_cost(self):
        pq = []  # Priority queue
        heapq.heappush(pq, (0, next(self.counter), self.start, []))  # (cost, unique count, cell, path)
        visited = set()

        while pq:

            cost, _, current_cell, path = heapq.heappop(pq)

            # Ensure no duplicate expansions of the same cell
            if current_cell in visited:
                continue

            visited.add(current_cell)
            new_path = path + [current_cell]
            yield new_path  

            if current_cell == self.end:
                yield new_path
                print("Total step cost:", sum([cell.step_cost for cell in new_path]))
                return

            for neighbor in self.get_neighbors(current_cell):
                if neighbor not in visited:
                    step_cost = current_cell.step_cost
                    heapq.heappush(pq, (cost + step_cost, next(self.counter), neighbor, new_path))
        
        yield [] 


class AStarAgent(BaseAgent):
    def __init__(self, maze, start, end, cols, rows, heuristic="manhattan"):
        super().__init__(maze, start, end, cols, rows)
        self.counter = itertools.count()
        self.generator = self.search()
        match heuristic:
            case "manhattan":
                self.heuristic = self.manhattan_heuristic
            case "euclidean":
                self.heuristic = self.euclidean_heuristic
            case "chebyshev":
                self.heuristic = self.chebyshev_heuristic
            case "diagonal":
                self.heuristic = self.diagonal_heuristic

    def manhattan_heuristic(self, cell):
        return abs(cell.x - self.end.x) + abs(cell.y - self.end.y)
    
    def euclidean_heuristic(self, cell):
        dx = cell.x - self.end.x
        dy = cell.y - self.end.y
        return math.sqrt(dx*dx + dy*dy)
    
    def chebyshev_heuristic(self, cell):
        dx = abs(cell.x - self.end.x)
        dy = abs(cell.y - self.end.y)
        return max(dx, dy)
    
    def diagonal_heuristic(self, cell):
        dx = abs(cell.x - self.end.x)
        dy = abs(cell.y - self.end.y)
        D = 1
        D2 = math.sqrt(2)
        return D * (dx + dy) + (D2 - 2*D) * min(dx, dy)

    def search(self):
        pq = []
        heapq.heappush(pq, (0, next(self.counter), self.start, []))
        visited = set()

        while pq:
            cost, _, current_cell, path = heapq.heappop(pq)

            # Ensure no duplicate expansions of the same cell
            if current_cell in visited:
                continue

            visited.add(current_cell)
            new_path = path + [current_cell]
            yield new_path  

            if current_cell == self.end:
                yield new_path
                return

            for neighbor in self.get_neighbors(current_cell):
                if neighbor not in visited:
                    step_cost = current_cell.step_cost
                    total_cost = cost + step_cost + self.heuristic(neighbor)
                    heapq.heappush(pq, (total_cost, next(self.counter), neighbor, new_path))
        
        yield []

class AStarFourCornersAgent(BaseAgent):
    def __init__(self, maze, start, end, cols, rows, heuristic_choice):
        super().__init__(maze, start, end, cols, rows)
        self.counter = itertools.count()
        self.maze = maze
        self.cols = cols
        self.rows = rows
        # Only store the other two corners since start is one corner and end is the other
        self.corners = [
            (cols-1, 0),
            (0, rows-1),
        ]

        # Decide which heuristic function to use
        if heuristic_choice == "sum":
            self.corners_heuristic = self.sum_heuristic
        else:
            self.corners_heuristic = self.max_dist_heuristic

        self.generator = self.search()

    def sum_heuristic(self, cell, visited_corners):
        # Sum of Euclidean distances
        h = 0
        for (cx, cy) in self.corners:
            if (cx, cy) not in visited_corners:
                dx = cell.x - cx
                dy = cell.y - cy
                h += math.sqrt(dx*dx + dy*dy)
        return h

    def max_dist_heuristic(self, cell, visited_corners):
        # Maximum distance to any unvisited corner
        distances = []
        for (cx, cy) in self.corners:
            if (cx, cy) not in visited_corners:
                dx = cell.x - cx
                dy = cell.y - cy
                distances.append(math.sqrt(dx*dx + dy*dy))
        return max(distances) if distances else 0
    

    def single_corner_search(self, start_cell, goal_cell):
        pq = []
        state_counter = itertools.count()

        visited = set()
        heapq.heappush(pq, (0, next(state_counter), start_cell, []))

        while pq:
            cost, _, current, path = heapq.heappop(pq)
            if current in visited:
                continue
            visited.add(current)

            new_path = path + [current]
            if current == goal_cell:
                return new_path

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    step_cost = current.step_cost
                    h = self.corners_heuristic(neighbor, {(start_cell.x, start_cell.y), (goal_cell.x, goal_cell.y)})
                    heapq.heappush(
                        pq,
                        (cost + step_cost + h, next(state_counter), neighbor, new_path)
                    )
        return []

    def search(self):
        final_path = []

        # Move from start to first corner
        corner_cells = []
        for (cx, cy) in self.corners:
            corner_cells.append(self.maze[cy * self.cols + cx])

        current = self.start
        for corner_cell in corner_cells:
            path_segment = self.single_corner_search(current, corner_cell)
            if not path_segment:
                yield []
                return
            # If the path is non-empty, merge (avoid duplicating the current cell)
            if final_path:
                final_path += path_segment[1:]
            else:
                final_path = path_segment
            current = corner_cell
            yield final_path

        # go from last corner to end
        last_leg = self.single_corner_search(current, self.end)
        if not last_leg:
            yield []
            return
        final_path += last_leg[1:]

        yield final_path

class AStarItemSearch(BaseAgent):
    def __init__(self, maze, start, cols, rows):
        super().__init__(maze, start, None, cols, rows)
        self.maze = maze
        self.current_cell = start
        self.counter = itertools.count()
        self.generator = self.search()

    def heuristic(self, cell, items_left):
        # A* heuristic that estimates the minimum cost to collect all remaining items
        if not items_left:
            return 0
        
        # Distance to nearest item (greedy component)
        min_dist = min(abs(cell.x - it.x) + abs(cell.y - it.y) for it in items_left)
        
        # Compute Minimum Spanning Tree (MST) over remaining items
        mst_cost = self.compute_mst_cost(items_left)
        
        return min_dist + mst_cost

    def compute_mst_cost(self, items):
        # Computes the minimum spanning tree (MST) cost for the remaining items using Prim's algorithm
        if not items:
            return 0
        
        nodes = [(cell.x, cell.y) for cell in items]
        mst_cost = 0
        visited = set()
        pq = [(0, nodes[0])]  # (cost, (x, y))
        
        while pq and len(visited) < len(nodes):
            cost, node = heapq.heappop(pq)
            if node in visited:
                continue
            visited.add(node)
            mst_cost += cost
            
            for neighbor in nodes:
                if neighbor not in visited:
                    dist = abs(node[0] - neighbor[0]) + abs(node[1] - neighbor[1])
                    heapq.heappush(pq, (dist, neighbor))
        
        return mst_cost

    def search(self):
        while any(cell.item for cell in self.maze):
            items_left = [cell for cell in self.maze if cell.item]
            pq = []
            heapq.heappush(pq, (0, next(self.counter), self.current_cell))
            visited = set()

            while pq:
                _, _, self.current_cell = heapq.heappop(pq)
                
                if self.current_cell.item:
                    self.current_cell.collect()
                    break  # Restart search after collecting an item
                
                visited.add(self.current_cell)
                for neighbor in self.get_neighbors(self.current_cell):
                    if neighbor not in visited:
                        h = self.heuristic(neighbor, items_left)
                        heapq.heappush(pq, (h, next(self.counter), neighbor))
                
                yield self.current_cell  # Yield current location for visualisation

    def draw(self, sc):
        cell = self.current_cell
        x, y = cell.x * cell.tile_size, cell.y * cell.tile_size
        pygame.draw.rect(sc, pygame.Color('blue'), (x + cell.thickness, y + cell.thickness, cell.tile_size 
                                                        - cell.thickness, cell.tile_size - cell.thickness))


class GreedyItemSearch(BaseAgent):
    def __init__(self, maze, start, cols, rows):
        super().__init__(maze, start, None, cols, rows)
        self.maze = maze
        self.current_cell = start
        self.counter = itertools.count()
        self.generator = self.search()

    def heuristic(self, cell, items_left):
        # using minimum Manhattan distance to any item
        return min(abs(cell.x - it.x) + abs(cell.y - it.y) for it in items_left) if items_left else 0

    def search(self):
        while any(cell.item for cell in self.maze):
            items_left = [cell for cell in self.maze if cell.item]
            pq = []
            heapq.heappush(pq, (0, next(self.counter), self.current_cell))
            visited = set()

            while pq:
                _, _, self.current_cell = heapq.heappop(pq)
                
                if self.current_cell.item:
                    self.current_cell.collect()
                    yield self.current_cell  # Ensure it counts before breaking
                    break  # Restart search after collecting an item
                
                visited.add(self.current_cell)
                for neighbor in self.get_neighbors(self.current_cell):
                    if neighbor not in visited:
                        h = self.heuristic(neighbor, items_left)
                        heapq.heappush(pq, (h, next(self.counter), neighbor))

                yield self.current_cell  # Ensure it yields every step


    def draw(self, sc):
        cell = self.current_cell
        x, y = cell.x * cell.tile_size, cell.y * cell.tile_size
        pygame.draw.rect(sc, pygame.Color('blue'), (x + cell.thickness, y + cell.thickness, cell.tile_size 
                                                        - cell.thickness, cell.tile_size - cell.thickness))
        

class ReflexAgent(BaseAgent):
    def __init__(self, maze, start, cols, rows, num_enemies):
        super().__init__(maze, start, None, cols, rows)
        self.maze = maze
        self.current_cell = start
        self.generator = self.search()
        self.enemies = [AdversarialAgent(maze, cols, rows, start, self) for _ in range(num_enemies)]
        self.caught = False
        # Movement history to detect cycles
        self.movement_history = []  # Store recent positions
        self.history_limit = 6  # How far back to check for cycles
        self.avoid_cells = set()  # Cells to temporarily avoid when in a cycle
        self.avoid_timer = 0  # Counter to reset avoid_cells after some steps
        # Flee factor - higher value means more aggressive fleeing
        self.flee_factor = 2.5  # Increased to make agent more responsive to enemies

    def get_safe_moves(self):
        # Evaluate all valid neighbors with their safety score (distance to nearest enemy)
        neighbors = self.get_neighbors(self.current_cell)
        safe_moves = []
        
        for cell in neighbors:
            # Calculate base safety score (distance to nearest enemy)
            distances = [self.manhattan_distance(cell, enemy.current_cell) for enemy in self.enemies]
            base_score = min(distances) if distances else 10  # Default high value if no enemies
            
            # Calculate direction vector from enemy to potential move
            # Higher scores for moves that are in opposite direction from enemies
            direction_bonus = 0
            for enemy in self.enemies:
                # Skip if enemy is too far away (over 8 cells)
                if self.manhattan_distance(self.current_cell, enemy.current_cell) > 8:
                    continue
                    
                # Vector from enemy to current position
                ex, ey = enemy.current_cell.x, enemy.current_cell.y
                cx, cy = self.current_cell.x, self.current_cell.y
                
                # Vector from current position to potential new position
                nx, ny = cell.x, cell.y
                
                # If moving away from enemy (in opposite direction), add bonus
                # Check if dot product of vectors is negative (moving in opposite directions)
                if (nx - cx) * (cx - ex) + (ny - cy) * (cy - ey) > 0:
                    direction_bonus += self.flee_factor  # Bonus for moving away from enemy
            
            # Combine base score with direction bonus
            total_score = base_score + direction_bonus
            safe_moves.append((cell, total_score))
            
        return safe_moves
    
    def manhattan_distance(self, cell1, cell2):
        return abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)

    def find_path_to_nearest_unvisited(self):
        from collections import deque
        queue = deque([(self.current_cell, [self.current_cell])])
        seen = {self.current_cell}
        while queue:
            cell, path = queue.popleft()
            if cell != self.current_cell and not cell.visited:
                return path
            for nb in self.get_neighbors(cell):
                if nb not in seen:
                    seen.add(nb)
                    queue.append((nb, path + [nb]))
        return []

    def detect_cycle(self):
        """Detect if agent is stuck in a cycle"""
        if len(self.movement_history) < self.history_limit:
            return False
            
        # Check for patterns like A->B->A->B->A->B (period 2)
        if (self.movement_history[-1] == self.movement_history[-3] == self.movement_history[-5] and
            self.movement_history[-2] == self.movement_history[-4] == self.movement_history[-6]):
            return True
            
        # Check for patterns like A->B->C->A->B->C (period 3)
        if (self.movement_history[-1] == self.movement_history[-4] and
            self.movement_history[-2] == self.movement_history[-5] and
            self.movement_history[-3] == self.movement_history[-6]):
            return True
            
        return False

    def search(self):
        path_stack = []  # Stack to keep track of movement history
        while not all(cell.visited for cell in self.maze):
            # First check if already caught (before movement)
            for enemy in self.enemies:
                if enemy.current_cell == self.current_cell:
                    self.caught = True
                    print("Player caught by enemy!")
                    yield self.current_cell
                    return

            # Update movement history for cycle detection
            self.movement_history.append(self.current_cell)
            if len(self.movement_history) > self.history_limit:
                self.movement_history.pop(0)
            
            # Check if we're in a cycle
            if self.detect_cycle():
                self.avoid_cells = set(self.movement_history)
                self.avoid_timer = 5  # Avoid for next 5 steps
            
            # Decrease avoid timer
            if self.avoid_timer > 0:
                self.avoid_timer -= 1
                if self.avoid_timer == 0:
                    self.avoid_cells.clear()
                    
            # PLAYER MOVES FIRST
            self.current_cell.visited = True
            
            # Check for enemies in dangerous proximity (closer distance threshold)
            dangerous_enemies = [
                enemy for enemy in self.enemies 
                if self.manhattan_distance(self.current_cell, enemy.current_cell) <= 2
            ]
            
            if dangerous_enemies:
                # Emergency escape - prioritize getting away from immediate threats
                neighbors = self.get_neighbors(self.current_cell)
                if neighbors:
                    # Find safest neighbor with maximum distance from all enemies
                    best_cell = max(
                        neighbors,
                        key=lambda cell: sum(self.manhattan_distance(cell, enemy.current_cell) for enemy in dangerous_enemies)
                    )
                    self.current_cell = best_cell
                    yield self.current_cell
                    
                    # ENEMIES MOVE AFTER PLAYER
                    for enemy in self.enemies:
                        enemy.move()
                        # Check if caught after enemy move
                        if enemy.current_cell == self.current_cell:
                            self.caught = True
                            print("Player caught by enemy!")
                            return
                    
                    continue
            
            # Check if any enemy is nearby and visible (increased detection range)
            enemies_nearby = any(
                self.manhattan_distance(self.current_cell, enemy.current_cell) <= 6 and
                enemy.has_line_of_sight_to_player() for enemy in self.enemies
            )
            
            # If no enemy is nearby or visible, use BFS path planning
            if not enemies_nearby:
                bfs_path = self.find_path_to_nearest_unvisited()
                if len(bfs_path) > 1 and bfs_path[1] not in self.avoid_cells:
                    self.current_cell = bfs_path[1]
                    yield self.current_cell
                    
                    # ENEMIES MOVE AFTER PLAYER
                    for enemy in self.enemies:
                        enemy.move()
                        if enemy.current_cell == self.current_cell:
                            self.caught = True
                            return
                    
                    continue
            
            # Standard movement logic with improved safety scoring
            unvisited_neighbors = [cell for cell in self.get_neighbors(self.current_cell) if not cell.visited]
            safe_moves = self.get_safe_moves()
            
            # Filter out cells we're trying to avoid from cycles
            safe_moves = [(cell, score) for cell, score in safe_moves if cell not in self.avoid_cells]
            
            if not safe_moves and self.avoid_cells:  # If all neighbors are in avoid_cells
                safe_moves = self.get_safe_moves()  # Reset and use all available moves
            
            if unvisited_neighbors:
                # Prefer unvisited moves that maximize safety
                candidate_moves = [(cell, score) for cell, score in safe_moves if cell in unvisited_neighbors]
                if candidate_moves:
                    best_move = max(candidate_moves, key=lambda x: x[1])[0]
                    path_stack.append(self.current_cell)
                    self.current_cell = best_move
                else:
                    # If we're avoiding cells, pick one not in the avoid list
                    candidates = [c for c in unvisited_neighbors if c not in self.avoid_cells]
                    if candidates:
                        path_stack.append(self.current_cell)
                        self.current_cell = random.choice(candidates)
                    else:
                        path_stack.append(self.current_cell)
                        self.current_cell = random.choice(unvisited_neighbors)
            elif safe_moves:
                # When no unvisited neighbor exists, choose the safest available move
                self.current_cell = max(safe_moves, key=lambda x: x[1])[0]
            elif path_stack:
                # Backtrack but avoid recently visited cells if possible
                backtrack_options = [cell for cell in path_stack if cell not in self.avoid_cells]
                if backtrack_options:
                    self.current_cell = backtrack_options[-1]
                    path_stack.remove(self.current_cell)
                else:
                    self.current_cell = path_stack.pop()  # Regular backtrack if no choice
            else:
                neighbors = [n for n in self.get_neighbors(self.current_cell) if n not in self.avoid_cells]
                if neighbors:
                    self.current_cell = random.choice(neighbors)
                else:
                    self.current_cell = random.choice(self.get_neighbors(self.current_cell))

            yield self.current_cell
            
            # ENEMIES MOVE AFTER PLAYER
            for enemy in self.enemies:
                enemy.move()
                if enemy.current_cell == self.current_cell:
                    self.caught = True
                    print("Player caught!")
                    return
        
        self.enemies = []  # Clear enemies after all cells are visited
        return

    def get_safe_moves(self):
        # Enhanced safety scoring to deal with multiple enemies
        neighbors = self.get_neighbors(self.current_cell)
        safe_moves = []
        
        for cell in neighbors:
            # Calculate base safety score (total distance from all enemies)
            enemy_distances = [self.manhattan_distance(cell, enemy.current_cell) for enemy in self.enemies]
            
            # Minimum distance to closest enemy (primary safety concern)
            min_distance = min(enemy_distances) if enemy_distances else 10
            
            # Average distance to all enemies (secondary safety concern)
            avg_distance = sum(enemy_distances) / len(enemy_distances) if enemy_distances else 10
            
            # Higher weight for minimum distance (avoiding closest enemy is most important)
            safety_score = min_distance * 1.5 + avg_distance * 0.5
            
            # Bonus for moving away from multiple enemies
            direction_bonus = 0
            for enemy in self.enemies:
                # Vector components
                ex, ey = enemy.current_cell.x, enemy.current_cell.y
                cx, cy = self.current_cell.x, self.current_cell.y
                nx, ny = cell.x, cell.y
                
                # If moving away from enemy, add bonus
                if (nx - cx) * (cx - ex) + (ny - cy) * (cy - ey) > 0:
                    # Higher bonus for closer enemies
                    distance = self.manhattan_distance(cell, enemy.current_cell)
                    if distance <= 3:
                        direction_bonus += 4  # Major bonus for escaping close enemies
                    else:
                        direction_bonus += 1  # Minor bonus for moving away from distant enemies
            
            # Final score combines safety distance and direction bonus
            total_score = safety_score + direction_bonus
            safe_moves.append((cell, total_score))
            
        return safe_moves

    def draw(self, sc):
        for enemy in self.enemies:
            enemy.draw(sc)
        x, y = self.current_cell.x * self.current_cell.tile_size, self.current_cell.y * self.current_cell.tile_size
        pygame.draw.rect(sc, pygame.Color('green'), (x + 2, y + 2, self.current_cell.tile_size - 4, self.current_cell.tile_size - 4))


class AdversarialAgent(BaseAgent):
    def __init__(self, maze, cols, rows, start, player):
        self.maze = maze
        self.current_cell = random.choice([cell for cell in maze if cell != start])
        self.cols = cols
        self.rows = rows
        self.player = player
        self.last_valid_cell = self.current_cell  # Keep track of last valid position
        self.vision_range = 5  # Maximum line of sight distance in cells
        self.seen_player = False  # Flag to track if player was recently seen

    def get_cell(self, x, y):
        """Helper method to get cell at specific coordinates"""
        for cell in self.maze:
            if cell.x == x and cell.y == y:
                return cell
        return None

    def has_line_of_sight_to_player(self):
        """Check if there's a direct line of sight to player without walls in the way"""
        start_x, start_y = self.current_cell.x, self.current_cell.y
        player_x, player_y = self.player.current_cell.x, self.player.current_cell.y
        
        # If we're at the same position, we can see the player
        if start_x == player_x and start_y == player_y:
            return True
            
        # Check if player is within vision range
        if abs(start_x - player_x) + abs(start_y - player_y) > self.vision_range:
            return False
        
        # Check if player is in one of the four cardinal directions (orthogonal)
        if start_x == player_x:  # Same column - vertical line of sight
            direction = 1 if player_y > start_y else -1
            # Check each cell along the line of sight
            y = start_y + direction
            while y != player_y + direction:
                # Check for walls blocking the view
                current_cell = self.get_cell(start_x, y - direction)
                if not current_cell:
                    return False
                
                # Check if the wall in the direction we're moving is present
                if direction == 1 and current_cell.walls['bottom']:
                    return False
                elif direction == -1 and current_cell.walls['top']:
                    return False
                
                y += direction
            return True
            
        elif start_y == player_y:  # Same row - horizontal line of sight
            direction = 1 if player_x > start_x else -1
            # Check each cell along the line of sight
            x = start_x + direction
            while x != player_x + direction:
                # Check for walls blocking the view
                current_cell = self.get_cell(x - direction, start_y)
                if not current_cell:
                    return False
                
                # Check if the wall in the direction we're moving is present
                if direction == 1 and current_cell.walls['right']:
                    return False
                elif direction == -1 and current_cell.walls['left']:
                    return False
                
                x += direction
            return True
            
        # Not in the same row or column
        return False

    def move(self):
        # Save the current cell as last valid before trying to move
        self.last_valid_cell = self.current_cell
        
        # Get all valid neighbor cells (respecting walls)
        neighbors = self.get_neighbors(self.current_cell)
        if not neighbors:
            return  # No valid moves
        
        # Check if the player is visible via line of sight
        self.seen_player = self.has_line_of_sight_to_player()
        
        # If player is visible, move toward them
        if self.seen_player:
            # Find the neighbor that gets us closest to the player
            next_cell = min(neighbors, 
                            key=lambda cell: abs(cell.x - self.player.current_cell.x) + 
                                           abs(cell.y - self.player.current_cell.y))
            self.current_cell = next_cell
            return
            
        # If we can't see player, move completely randomly (dumber behavior)
        self.current_cell = random.choice(neighbors)
    
    def draw(self, sc):
        # Safety check to ensure current_cell is not None
        if not self.current_cell:
            self.current_cell = self.last_valid_cell
            if not self.current_cell:
                self.current_cell = self.maze[0]  # Fallback to first cell
                
        x, y = self.current_cell.x * self.current_cell.tile_size, self.current_cell.y * self.current_cell.tile_size
        # Draw the enemy in red, or yellow if it has spotted the player
        color = pygame.Color('yellow') if self.seen_player else pygame.Color('red')
        pygame.draw.rect(sc, color, (x + 2, y + 2, self.current_cell.tile_size - 4, self.current_cell.tile_size - 4))


class MiniMaxAgent(ReflexAgent):
    def __init__(self, maze, start, cols, rows, num_enemies):
        super().__init__(maze, start, cols, rows, num_enemies)
        self.search_depth = 2  # Limited search depth
        self.generator = self.search()
        self.visited_counts = {cell: 0 for cell in maze}  # Track visits
        
    def search(self):
        """Minimax-based search for movement."""
        while not all(cell.visited for cell in self.maze):
            # Mark current cell as visited
            self.current_cell.visited = True
            self.visited_counts[self.current_cell] += 1

            # Check if caught by an enemy
            if any(enemy.current_cell == self.current_cell for enemy in self.enemies):
                self.caught = True
                print("Player caught!")
                return

            # Decide the next move using minimax
            best_move = self.minimax_decision()
            if best_move:
                self.current_cell = best_move
            else:
                # If minimax fails, move to the nearest unvisited cell
                path = self.find_path_to_nearest_unvisited()
                if path:
                    self.current_cell = path[0]
                else:
                    # As a last resort, move randomly
                    self.current_cell = random.choice(self.get_neighbors(self.current_cell))
            
            yield self.current_cell
            
            # Move enemies
            for enemy in self.enemies:
                enemy.move()
                if enemy.current_cell == self.current_cell:
                    self.caught = True
                    print("Player caught after minimax move!")
                    return
        
    def minimax_decision(self):
        """Use minimax to select the best move."""
        valid_moves = self.get_neighbors(self.current_cell)
        if not valid_moves:
            return None

        best_score = float('-inf')
        best_move = None
        
        for move in valid_moves:
            game_state = {
                'player_pos': move,
                'enemy_positions': [enemy.current_cell for enemy in self.enemies],
                'visit_count': self.visited_counts[move]
            }
            
            score = self.minimax(game_state, depth=1, max_depth=self.search_depth, is_maximizing=False)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def minimax(self, state, depth, max_depth, is_maximizing):
        """Minimax evaluation with depth limit."""
        if depth == max_depth:
            return self.evaluate_state(state)

        player_pos = state['player_pos']
        enemy_positions = state['enemy_positions']
        
        # If caught by an enemy, return a low score
        if any(enemy_pos == player_pos for enemy_pos in enemy_positions):
            return -1000

        if is_maximizing:
            max_eval = float('-inf')
            for move in self.get_neighbors(player_pos):
                new_state = {**state, 'player_pos': move}
                max_eval = max(max_eval, self.minimax(new_state, depth + 1, max_depth, False))
            return max_eval
        else:
            min_eval = float('inf')
            for i, enemy_pos in enumerate(enemy_positions):
                possible_moves = self.predict_enemy_movement(enemy_pos, player_pos)
                for move in possible_moves:
                    new_enemy_positions = enemy_positions[:]
                    new_enemy_positions[i] = move
                    new_state = {**state, 'enemy_positions': new_enemy_positions}
                    min_eval = min(min_eval, self.minimax(new_state, depth + 1, max_depth, True))
            return min_eval

    def evaluate_state(self, state):
        """Evaluate the desirability of a given state."""
        score = 0
        player_pos = state['player_pos']
        visit_count = state['visit_count']

        # Reward moving to unvisited cells
        if visit_count == 0:
            score += 100
        else:
            score -= visit_count * 5  # Penalize revisits

        # Penalize being close to enemies
        for enemy_pos in state['enemy_positions']:
            distance = self.manhattan_distance(player_pos, enemy_pos)
            if distance <= 1:
                score -= 100
            elif distance <= 2:
                score -= 50
            
        return score

    def predict_enemy_movement(self, enemy_pos, player_pos):
        """Predict enemy movement (chase or random)."""
        neighbors = self.get_neighbors(enemy_pos)
        if self.check_line_of_sight(enemy_pos, player_pos):
            return [min(neighbors, key=lambda cell: self.manhattan_distance(cell, player_pos))]
        return neighbors
    
    def check_line_of_sight(self, pos1, pos2):
        """Check if pos2 is in line of sight from pos1 (orthogonal only)"""
        # Only consider orthogonal (same row or column)
        if pos1.x != pos2.x and pos1.y != pos2.y:
            return False
            
        # Calculate Manhattan distance
        manhattan_dist = abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)
        
        # Check if within vision range (using same range as AdversarialAgent)
        if manhattan_dist > 5:  # Using vision_range = 5
            return False
            
        if pos1.x == pos2.x:  # Same column - check vertical line of sight
            y1, y2 = min(pos1.y, pos2.y), max(pos1.y, pos2.y)
            for y in range(y1, y2):
                current_cell = self.get_cell(pos1.x, y)
                next_cell = self.get_cell(pos1.x, y + 1)
                if not current_cell or not next_cell:
                    return False
                # Check if there's a wall blocking the view
                if current_cell.walls['bottom'] or next_cell.walls['top']:
                    return False
            return True
            
        else:  # Same row - check horizontal line of sight
            x1, x2 = min(pos1.x, pos2.x), max(pos1.x, pos2.x)
            for x in range(x1, x2):
                current_cell = self.get_cell(x - 1, pos1.y)
                next_cell = self.get_cell(x, pos1.y)
                if not current_cell or not next_cell:
                    return False
                # Check if there's a wall blocking the view
                if current_cell.walls['right'] or next_cell.walls['left']:
                    return False
            return True



class AlphaBetaAgent(MiniMaxAgent):
    def __init__(self, maze, start, cols, rows, num_enemies):
        super().__init__(maze, start, cols, rows, num_enemies)
    
    def minimax(self, state, depth, max_depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        """Minimax with Alpha-Beta Pruning."""
        if depth == max_depth:
            return self.evaluate_state(state)

        player_pos = state['player_pos']
        enemy_positions = state['enemy_positions']
        
        # If caught by an enemy, return a low score
        if any(enemy_pos == player_pos for enemy_pos in enemy_positions):
            return -1000

        if is_maximizing:
            max_eval = float('-inf')
            for move in self.get_neighbors(player_pos):
                new_state = {**state, 'player_pos': move}
                max_eval = max(max_eval, self.minimax(new_state, depth + 1, max_depth, False, alpha, beta))
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            for i, enemy_pos in enumerate(enemy_positions):
                possible_moves = self.predict_enemy_movement(enemy_pos, player_pos)
                for move in possible_moves:
                    new_enemy_positions = enemy_positions[:]
                    new_enemy_positions[i] = move
                    new_state = {**state, 'enemy_positions': new_enemy_positions}
                    min_eval = min(min_eval, self.minimax(new_state, depth + 1, max_depth, True, alpha, beta))
                    beta = min(beta, min_eval)
                    if beta <= alpha:
                        break  # Alpha cut-off
            return min_eval


class ExpectiMaxAgent(MiniMaxAgent):
    def __init__(self, maze, start, cols, rows, num_enemies):
        super().__init__(maze, start, cols, rows, num_enemies)

    def minimax(self, state, depth, max_depth, is_maximizing):
        """Expectimax evaluation with depth limit."""
        if depth == max_depth:
            return self.evaluate_state(state)

        player_pos = state['player_pos']
        enemy_positions = state['enemy_positions']

        # If caught by an enemy, return a low score
        if any(enemy_pos == player_pos for enemy_pos in enemy_positions):
            return -1000

        if is_maximizing:  # Player's turn (maximize score)
            return max(
                self.minimax({**state, 'player_pos': move}, depth + 1, max_depth, False)
                for move in self.get_neighbors(player_pos)
            )

        else:  # Expectation calculation for enemy moves
            expected_value = 0
            total_moves = 0

            for i, enemy_pos in enumerate(enemy_positions):
                possible_moves = self.predict_enemy_movement(enemy_pos, player_pos)
                probability = 1 / len(possible_moves)  # Assume uniform probability
                
                for move in possible_moves:
                    new_enemy_positions = enemy_positions[:]
                    new_enemy_positions[i] = move
                    new_state = {**state, 'enemy_positions': new_enemy_positions}

                    expected_value += probability * self.minimax(new_state, depth + 1, max_depth, True)
                    total_moves += 1  # Track number of evaluated moves

            return expected_value  # No need to divide again, probability handles weighting
