import pygame
import sys
from MazeGenerator import *
from agents import *

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1202, 902
BACKGROUND_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 70, 80)
BUTTON_HOVER_COLOR = (90, 90, 100)
TEXT_COLOR = (240, 240, 240)
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 300
INPUT_BOX_HEIGHT = 40
INPUT_BOX_WIDTH = 200

# Global settings
VISUALIZATION_SPEED = 10  # Steps per second, default value

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Maze Algorithm Visualizer')
clock = pygame.time.Clock()

font_large = pygame.font.SysFont('Arial', 32)
font_medium = pygame.font.SysFont('Arial', 24)
font_small = pygame.font.SysFont('Arial', 18)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, width=2, border_radius=5)
        
        text_surf = font_medium.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and self.action:
                return self.action()
        return None

class InputBox:
    def __init__(self, x, y, width, height, prompt, default_text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.prompt = prompt
        self.text = default_text
        self.active = False
        self.prompt_surf = font_small.render(prompt, True, TEXT_COLOR)
        self.prompt_rect = self.prompt_surf.get_rect(bottomleft=(x, y - 5))
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Only allow numeric input
                    if event.unicode.isdigit() or event.unicode == '.':
                        self.text += event.unicode
        return None

    def draw(self, surface):
        # Draw prompt text above the box
        surface.blit(self.prompt_surf, self.prompt_rect)
        
        # Draw input box
        border_color = (180, 180, 200) if self.active else (120, 120, 140)
        pygame.draw.rect(surface, BACKGROUND_COLOR, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=3)
        
        # Render text inside box
        text_surf = font_medium.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(midleft=(self.rect.left + 10, self.rect.centery))
        surface.blit(text_surf, text_rect)

def main_menu():
    """Display the main menu with agent selection buttons"""
    # Clear screen completely when entering menu
    screen.fill(BACKGROUND_COLOR)
    pygame.display.flip()
    screen.fill(BACKGROUND_COLOR)
    
    title = font_large.render("Maze Algorithm Visualizer", True, TEXT_COLOR)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title, title_rect)
    
    sub_title = font_medium.render("Select an agent to visualize:", True, TEXT_COLOR)
    sub_rect = sub_title.get_rect(center=(SCREEN_WIDTH // 2, 130))
    screen.blit(sub_title, sub_rect)

    # Add settings info to main menu
    speed_text = font_small.render(f"Speed: {VISUALIZATION_SPEED} steps/second", True, (180, 180, 180))
    speed_rect = speed_text.get_rect(topleft=(20, SCREEN_HEIGHT - 30))
    screen.blit(speed_text, speed_rect)

    # Create buttons for each agent type and settings
    button_y = 200
    button_spacing = 60
    buttons = []
    
    agent_types = [
        ("BFS (Breadth-First Search)", "BFS"),
        ("DFS (Depth-First Search)", "DFS"),
        ("UCS (Uniform Cost Search)", "UCS"),
        ("A* Search", "A*"),
        ("A* Item Collection", "A*item"),
        ("Greedy Item Search", "greedy"),
        ("Reflex Agent", "reflex"),
        ("MiniMax Agent", "minimax"),
        ("Alpha-Beta Pruning", "AB"),
        ("Settings", "settings"),
        ("Exit", "exit")
    ]
    
    for title, agent_id in agent_types:
        btn = Button(
            SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
            button_y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            title,
            lambda a=agent_id: agent_selection(a)
        )
        buttons.append(btn)
        button_y += button_spacing
    
    # Event loop
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            for button in buttons:
                button.check_hover(mouse_pos)
                result = button.handle_event(event)
                if result:
                    return result
                    
        # Draw buttons
        for button in buttons:
            button.draw(screen)
            
        pygame.display.flip()
        clock.tick(60)

def agent_selection(agent_type):
    """Handle selection of an agent type"""
    if agent_type == "exit":
        pygame.quit()
        sys.exit()
    elif agent_type == "settings":
        settings_menu()
        return None
    
    # Get basic parameters for all agent types
    size = get_parameters("maze_size", "Enter maze size:", "10")
    
    if size is None:  # User cancelled
        return None
        
    tile_size = min(SCREEN_WIDTH // size, SCREEN_HEIGHT // size)
    cols, rows = SCREEN_WIDTH // tile_size, SCREEN_HEIGHT // tile_size
    
    # Get additional parameters based on agent type
    if agent_type in ["A*item", "greedy"]:
        num_items = get_parameters("items", "Enter number of items:", "10")
        if num_items is None:  # User cancelled
            return None
        grid_cells = generate_maze(size, cols, rows, tile_size, num_items=num_items)
        
        if agent_type == "A*item":
            agent = AStarItemSearch(grid_cells, grid_cells[0], cols, rows)
        else:  # greedy
            agent = GreedyItemSearch(grid_cells, grid_cells[0], cols, rows)
        has_path = False
        
    elif agent_type in ["reflex", "minimax", "AB"]:
        num_enemies = get_parameters("enemies", "Enter number of enemies:", "2")
        if num_enemies is None:  # User cancelled
            return None
        grid_cells = generate_maze(size, cols, rows, tile_size)
        grid_cells[-1].end = False
        
        if agent_type == "reflex":
            agent = ReflexAgent(grid_cells, grid_cells[0], cols, rows, num_enemies)
        elif agent_type == "minimax":
            agent = MiniMaxAgent(grid_cells, grid_cells[0], cols, rows, num_enemies)
        else:  # AB (Alpha-Beta)
            agent = AlphaBetaAgent(grid_cells, grid_cells[0], cols, rows, num_enemies)
        has_path = False
        
    elif agent_type == "UCS":
        grid_cells = generate_maze(size, cols, rows, tile_size, stepcosts=True)
        agent = UCSAgent(grid_cells, grid_cells[0], grid_cells[-1], cols, rows)
        has_path = True
        
    else:  # BFS, DFS, A*
        grid_cells = generate_maze(size, cols, rows, tile_size)
        if agent_type == "BFS":
            agent = BFSAgent(grid_cells, grid_cells[0], grid_cells[-1], cols, rows)
        elif agent_type == "DFS":
            agent = DFSAgent(grid_cells, grid_cells[0], grid_cells[-1], cols, rows)
        else:  # A*
            agent = AStarAgent(grid_cells, grid_cells[0], grid_cells[-1], cols, rows)
        has_path = True
    
    # Run visualization with the selected agent
    visualization_loop(agent, grid_cells, has_path)
    return None

def get_parameters(param_type, prompt, default_value):
    """Show a screen to get specific parameters"""
    input_box = InputBox(
        SCREEN_WIDTH // 2 - INPUT_BOX_WIDTH // 2,
        SCREEN_HEIGHT // 2 - 20,
        INPUT_BOX_WIDTH, 
        INPUT_BOX_HEIGHT,
        prompt,
        default_value
    )
    
    confirm_button = Button(
        SCREEN_WIDTH // 2 - 70,
        SCREEN_HEIGHT // 2 + 60,
        140, 50,
        "Confirm",
        lambda: int(input_box.text) if input_box.text.isdigit() else 10
    )
    
    back_button = Button(
        SCREEN_WIDTH // 2 - 70,
        SCREEN_HEIGHT // 2 + 120,
        140, 50,
        "Back",
        lambda: None
    )
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        title = font_large.render(f"Enter {param_type.replace('_', ' ').title()}", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            input_result = input_box.handle_event(event)
            
            confirm_button.check_hover(mouse_pos)
            result = confirm_button.handle_event(event)
            if result is not None:
                return result
                
            back_button.check_hover(mouse_pos)
            if back_button.handle_event(event):
                return None
        
        input_box.draw(screen)
        confirm_button.draw(screen)
        back_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

def settings_menu():
    """Show settings screen to adjust visualization speed"""
    global VISUALIZATION_SPEED
    
    screen.fill(BACKGROUND_COLOR)
    
    title = font_large.render("Settings", True, TEXT_COLOR)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title, title_rect)
    
    # Create slider for speed adjustment (simple version with buttons)
    speed_text = font_medium.render(f"Visualization Speed: {VISUALIZATION_SPEED} steps/second", True, TEXT_COLOR)
    speed_rect = speed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    
    decrease_button = Button(
        SCREEN_WIDTH // 2 - 150,
        SCREEN_HEIGHT // 2,
        60, 40,
        "-",
        lambda: adjust_speed(-1)
    )
    
    increase_button = Button(
        SCREEN_WIDTH // 2 + 90,
        SCREEN_HEIGHT // 2,
        60, 40,
        "+",
        lambda: adjust_speed(1)
    )
    
    back_button = Button(
        SCREEN_WIDTH // 2 - 70,
        SCREEN_HEIGHT // 2 + 100,
        140, 50,
        "Back",
        lambda: True  
    )
    
    def adjust_speed(amount):
        global VISUALIZATION_SPEED
        VISUALIZATION_SPEED = max(1, min(60, VISUALIZATION_SPEED + amount))
        return None
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BACKGROUND_COLOR)
        
        # Re-render speed text with current value
        speed_text = font_medium.render(f"Visualization Speed: {VISUALIZATION_SPEED} steps/second", True, TEXT_COLOR)
        screen.blit(title, title_rect)
        screen.blit(speed_text, speed_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            decrease_button.check_hover(mouse_pos)
            if decrease_button.handle_event(event):
                # Re-render to show updated speed
                continue
                
            increase_button.check_hover(mouse_pos)
            if increase_button.handle_event(event):
                # Re-render to show updated speed
                continue
                
            back_button.check_hover(mouse_pos)
            if back_button.handle_event(event):  
                screen.fill(BACKGROUND_COLOR)
                return
        
        decrease_button.draw(screen)
        increase_button.draw(screen)
        back_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

def visualization_loop(agent, grid_cells, has_path=True):
    """Run the visualization for the selected agent until completion"""
    global VISUALIZATION_SPEED
    
    step_count = 0
    running = True
    completed = False
    caught = False
    
    # For tracking runtime
    start_time = pygame.time.get_ticks()

    # Main visualization loop
    while running:
        # Process events first (to ensure ESC key works immediately)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Force complete cleanup before returning to menu
                    pygame.display.flip()
                    pygame.time.delay(100)
                    screen.fill(BACKGROUND_COLOR)  # Small delay to ensure cleanup
                    main_menu()
                    return  # Exit immediately to menu
        
        # Clear screen
        screen.fill(BACKGROUND_COLOR)
        
        # Draw the maze cells
        for cell in grid_cells:
            cell.draw(screen)
        if has_path:
            agent.draw_path(screen)
        else:
            agent.draw(screen)
        
        # If not completed, advance the agent
        if not completed:
            try:
                # Check caught status before agent moves
                if hasattr(agent, 'caught') and agent.caught:
                    caught = True
                    completed = True
                    end_time = pygame.time.get_ticks()
                    elapsed_time = (end_time - start_time) / 1000

                agent.path = next(agent.generator)
                step_count += 1
                
                # Check caught status again after agent moves
                if hasattr(agent, 'caught') and agent.caught:
                    caught = True
                    completed = True
                    end_time = pygame.time.get_ticks()
                    elapsed_time = (end_time - start_time) / 1000
                
            except StopIteration:
                # Algorithm finished
                completed = True
                end_time = pygame.time.get_ticks()
                elapsed_time = (end_time - start_time) / 1000
        
            
        # Draw completion/stats overlay when finished
        if completed:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, 150))
            overlay.set_alpha(200)
            overlay.fill((20, 20, 30))
            screen.blit(overlay, (0, 0))
            
            # Set status text based on caught status
            if caught or agent.caught:
                status_text = "Agent was caught by enemies!"
                color = (255, 100, 100)
            else:
                status_text = "Exploration completed successfully!"
                color = (100, 255, 100)
                
            # Display statistics
            texts = [
                (status_text, font_large, color),
                (f"Steps taken: {step_count}", font_medium, TEXT_COLOR),
                (f"Time elapsed: {elapsed_time:.2f} seconds", font_medium, TEXT_COLOR),
                ("Press ESC to return to menu", font_small, (180, 180, 180))
            ]
            
            y_offset = 20
            for text, font_obj, text_color in texts:
                text_surf = font_obj.render(text, True, text_color)
                text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                screen.blit(text_surf, text_rect)
                y_offset += 30
        else:
            # Show instructions during simulation
            instruction_text = font_small.render("Press ESC to return to menu", True, (220, 220, 220))
            instruction_rect = instruction_text.get_rect(topleft=(10, 10))
            screen.blit(instruction_text, instruction_rect)
                
        pygame.display.flip()
        
        # Cap frame rate based on speed setting
        clock.tick(VISUALIZATION_SPEED)
    
    # Ensure screen is cleared before returning to menu
    screen.fill(BACKGROUND_COLOR)
    pygame.display.flip()

def main():
    """Main program loop"""
    while True:
        # Ensure clean state at beginning of each menu display
        screen.fill(BACKGROUND_COLOR)
        pygame.display.flip()
        agent_type = main_menu()

if __name__ == '__main__':
    main()
