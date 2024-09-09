import os
import time
import pygame
import random
import settings

def show_countdown():
    countdown_numbers = ['3', '2', '1', 'GO!']

    for number in countdown_numbers:
        settings.dis.blit(settings.background_game_over, (0, 0))  # Update the background
        draw_text(number, settings.white, 0, settings.name_font_regular, 60)  # Display the countdown text in the center of the screen
        pygame.display.update()
        time.sleep(0.5)  # Delay 0.5 second between frames

# Define the path for the record file next to the executable file
def get_high_score_file_path():
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, 'snake_game_high_score.txt')

# Update speed after eating an apple
def update_speed():
    if settings.snake_speed < settings.max_speed:
        settings.snake_speed = min(settings.snake_speed + settings.speed_increment, settings.max_speed)

# Function for displaying the text "Pause"
def show_pause_message():
    # Display the text "Paused" with a glow effect
    draw_text("Paused", settings.white, -50, settings.name_font_regular, 75)
    
    # Display text with instructions for resetting the record and exiting to the menu
    draw_text("P to Continue, or B to go to Menu", settings.white, 50, settings.name_font_regular, 35)
    
    # Refresh the screen
    pygame.display.update()

# Random, round functions for creating food
def random_round_creating_food_with_screen_difference(start, stop, game_offset_asix):
    random_round_point = round(random.randrange(start, stop, settings.snake_block) / settings.snake_block) * settings.snake_block
    random_round_point_with_difference = random_round_point + game_offset_asix
    return random_round_point_with_difference

# Function to center the button along the X axis
def center_button_x(button_width):
    return (settings.dis_width - button_width) / 2

# Centering an element along the Y axis
def center_button_y(element_height, offset=0):
    return (settings.dis_height - element_height) / 2 + offset

# Function to center text on X and Y axis
def center_text_x_y(text_surface, x, y, w, h):
    """
    Centering text along the width and height of the container.
    text_surface: text surface created using font.render()
    x, y: initial coordinates
    w, h: width and height of the container for the text (for example, a button)
    """
    centered_x = x + (w - text_surface.get_width()) / 2
    centered_y = y + (h - text_surface.get_height()) / 2
    return centered_x, centered_y

def calculate_button_size_and_position(text):
    # Load a custom font for text on buttons
    font = settings.score_font  # Use the font from settings
    
    padding_x=15
    padding_y=15

    # Calculate button width based on text length
    text_surface = font.render(text, True, settings.white)
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()

    # The width and height of the button depend on the text
    button_width = text_width + 2 * padding_x
    button_height = text_height - padding_y

    # Returning the parameters for the button: dimensions and text surface
    return button_width, button_height, text_surface

# Function of drawing a button with highlighting on hover
def draw_button_with_hover(x, y, text, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Using a generic function to calculate button size
    button_width, button_height, text_surface = calculate_button_size_and_position(text)

    # Use the function to center the button along the X axis
    # Checking that the button text is not "Main Menu" and not "Back" for centering
    if text != "Main Menu" and text != "Back":
        button_x = center_button_x(button_width)
    else:
        button_x = x

    # Highlight on hover
    if button_x + button_width > mouse[0] > button_x and y + button_height > mouse[1] > y:
        # Drawing a blurry outline for a neon lighting effect
        for offset in range(5, 25, 5):
            glow_rect = pygame.Surface((button_width + offset * 2, button_height + offset * 2), pygame.SRCALPHA)
            pygame.draw.rect(glow_rect, settings.glow_color, (0, 0, button_width + offset * 2, button_height + offset * 2), border_radius=20)
            glow_rect.set_alpha(150 - offset * 5)
            settings.dis.blit(glow_rect, (button_x - offset, y - offset))

        # Drawing the main button with backlight
        pygame.draw.rect(settings.dis, settings.neon_color, (button_x, y, button_width, button_height), border_radius=20)
        if click[0] == 1 and action is not None:
            action()
    else:
        # Default black button with rounded corners
        if text != "Back" and text != 'Main Menu':
            pygame.draw.rect(settings.dis, settings.black, (button_x, y, button_width, button_height), border_radius=20)

    # Centering text on a button
    centered_x, centered_y = center_text_x_y(text_surface, x, y, button_width, button_height)
    settings.dis.blit(text_surface, (centered_x, centered_y))  # Drawing text

def main_buttons(factor, text, function):
    button_spacing = 50

    button_width, button_height, text_surface = calculate_button_size_and_position(text)

    button_x = center_button_x(button_width)
    button_start_y = center_button_y(button_height, -40)
    
    draw_button_with_hover(button_x, button_start_y + button_spacing * factor, text, function)

# Function for drawing the "Back" button
def draw_back_button(game_menu):
    # Determining the margins from the edges of the screen
    right_margin = 10  
    top_margin = 30    

    draw_button_with_hover(right_margin, top_margin, "Back", game_menu)

# Function for checking the pressing of the "Back" button
def check_back_button_click(mouse_pos, game_menu):
    if 10 <= mouse_pos[0] <= 110 and 10 <= mouse_pos[1] <= 50:
        game_menu()

# Function for drawing the "Main Menu" button
def draw_main_menu_button(game_menu):
    # Determining the margins from the edges of the screen
    right_margin = 10  
    top_margin = 20    

    button_width, button_height, text_surface = calculate_button_size_and_position("Main Menu")
    
    # Position the button in the upper right corner
    button_x = settings.dis_width - right_margin - button_width  # Indentation from the right edge of the screen
    button_y = top_margin  # Indentation from the top edge of the screen

    draw_button_with_hover(button_x, button_y, "Main Menu", game_menu)

# Function for checking whether the "Main Menu" button is pressed
def check_main_menu_button_click(mouse_pos, game_menu):
    if 10 <= mouse_pos[0] <= 110 and 10 <= mouse_pos[1] <= 50:
        game_menu()

# Function for drawing text with a glow effect
def draw_text(message, text_color, y_offset, font_name, font_size):
    # We use the font from assets if another is not passed
    font = pygame.font.Font(font_name, font_size)

    # Creating a text surface for the main text
    text_surface = font.render(message, True, text_color)

    # Centering the text relative to the screen
    text_rect = text_surface.get_rect(center=(settings.dis_width / 2, settings.dis_height / 2 + y_offset))


    if message != "Snake Game":
            # Create text surfaces for the outline (1 pixel offset in all directions)
        outline_surfaces = [
            font.render(message, True, settings.white),  # Левый верх
            font.render(message, True, settings.white),  # Верх
            font.render(message, True, settings.white),  # Правый верх
            font.render(message, True, settings.white),  # Левый
            font.render(message, True, settings.white),  # Правый
            font.render(message, True, settings.white),  # Левый низ
            font.render(message, True, settings.white),  # Низ
            font.render(message, True, settings.white),  # Правый низ
        ]

        # Draw a text outline by moving the text one pixel in each direction
        offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        
        y = y_offset
        for surface, (offset_x, offset_y) in zip(outline_surfaces, offsets):
            settings.dis.blit(surface, (text_rect.x + offset_x, text_rect.y + offset_y))

        # Drawing the main text on top of the outline
        settings.dis.blit(text_surface, (text_rect.x, text_rect.y))

    else:
        # If the button is "Main Menu", use the passed value x
        for offset in range(1, 6):  # Soft glow (the larger the offset, the softer the glow will be)
            glow_surface = font.render(message, True, settings.white)
            glow_surface.set_alpha(255 - offset * 50)  # Transparency decreases for each layer
            settings.dis.blit(glow_surface, (text_rect.x - offset, text_rect.y - offset))
            settings.dis.blit(glow_surface, (text_rect.x + offset, text_rect.y + offset))
        settings.dis.blit(text_surface, text_rect)

# Function to display a message about a new record
def new_high_score_message():
    draw_text("New High Score! Congratulations!", settings.yellow, 0, settings.name_font_regular, 35)

# Function for downloading a record
def load_high_score():
    try:
        if os.path.exists(get_high_score_file_path()):
            with open(get_high_score_file_path(), 'r') as file:
                return int(file.read())
        else:
            return 0  
    except Exception as e:
        print(f"Error loading high score: {e}")
        return 0

# Function for saving a record
def save_high_score(high_score):
    try:
        with open(get_high_score_file_path(), 'w') as file:
            file.write(str(high_score))
    except Exception as e:
        print(f"Error saving high score: {e}")

# Scoring
def your_score(score, high_score):
    # Display current account
    value = settings.score_font.render("Score: " + str(score), True, settings.white)
    high_score_value = settings.score_font.render("High Score: " + str(high_score), True, settings.white)
    
    # Place the score and record in the upper left corner
    settings.dis.blit(value, [10, 10])
    settings.dis.blit(high_score_value, [10, 50])

    