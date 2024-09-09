import pygame
import os
import sys

# Define the base path to resources
def resource_path(relative_path):
    """ Get the path to the resource, supporting work in compiled and uncompiled mode. """
    try:
        # PyInstaller creates a temporary path to the files
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Pygame initialization
pygame.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
neon_color = (128, 0, 128)
glow_color = (200, 0, 200, 100)
grey = (140, 140, 140)

# Loading food images
food_images = [
    pygame.image.load(resource_path("assets/images/fruits/papaya.png")),
    pygame.image.load(resource_path("assets/images/fruits/mango.png")),
    pygame.image.load(resource_path("assets/images/fruits/pineapple.png")),
    pygame.image.load(resource_path("assets/images/fruits/dragon-fruit.png")),
    pygame.image.load(resource_path("assets/images/fruits/cherries.png")),
    pygame.image.load(resource_path("assets/images/fruits/bananas.png")),
    pygame.image.load(resource_path("assets/images/fruits/lemon.png")),
    pygame.image.load(resource_path("assets/images/fruits/watermelon.png")),
    pygame.image.load(resource_path("assets/images/fruits/strawberry.png")),
    pygame.image.load(resource_path("assets/images/fruits/apple.png"))
]

# Let's create dictionaries for each direction
snake_images = {
    'UP': {
        'head': pygame.image.load(resource_path("assets/images/snake/head-up.png")),
        'body-1': pygame.image.load(resource_path("assets/images/snake/body-1-up.png")),
        'body-2': pygame.image.load(resource_path("assets/images/snake/body-2-up.png")),
        'tail': pygame.image.load(resource_path("assets/images/snake/tail-up.png")),
        'happy_head': pygame.image.load(resource_path("assets/images/snake/happy_head_up.png"))
    },
    'DOWN': {
        'head': pygame.image.load(resource_path("assets/images/snake/head-down.png")),
        'body-1': pygame.image.load(resource_path("assets/images/snake/body-1-down.png")),
        'body-2': pygame.image.load(resource_path("assets/images/snake/body-2-down.png")),
        'tail': pygame.image.load(resource_path("assets/images/snake/tail-down.png")),
        'happy_head': pygame.image.load(resource_path("assets/images/snake/happy_head_down.png"))
    },
    'LEFT': {
        'head': pygame.image.load(resource_path("assets/images/snake/head-left.png")),
        'body-1': pygame.image.load(resource_path("assets/images/snake/body-1-left.png")),
        'body-2': pygame.image.load(resource_path("assets/images/snake/body-2-left.png")),
        'tail': pygame.image.load(resource_path("assets/images/snake/tail-left.png")),
        'happy_head': pygame.image.load(resource_path("assets/images/snake/happy_head_left.png"))
    },
    'RIGHT': {
        'head': pygame.image.load(resource_path("assets/images/snake/head-right.png")),
        'body-1': pygame.image.load(resource_path("assets/images/snake/body-1-right.png")),
        'body-2': pygame.image.load(resource_path("assets/images/snake/body-2-right.png")),
        'tail': pygame.image.load(resource_path("assets/images/snake/tail-right.png")),
        'happy_head': pygame.image.load(resource_path("assets/images/snake/happy_head_right.png"))
    },
    'TURN' : {
        'turn-right-down': pygame.image.load(resource_path("assets/images/snake/turn-right-down.png")),
        'turn-down-left': pygame.image.load(resource_path("assets/images/snake/turn-down-left.png")),
        'turn-left-up': pygame.image.load(resource_path("assets/images/snake/turn-left-up.png")),
        'turn-up-right': pygame.image.load(resource_path("assets/images/snake/turn-up-right.png")),
        'turn-right-up': pygame.image.load(resource_path("assets/images/snake/turn-right-up.png")),
        'turn-up-left': pygame.image.load(resource_path("assets/images/snake/turn-up-left.png")),
        'turn-left-down': pygame.image.load(resource_path("assets/images/snake/turn-left-down.png")),
        'turn-down-right': pygame.image.load(resource_path("assets/images/snake/turn-down-right.png")),
        
        # Add rotation images for body-1
        'body-1-up-right': pygame.image.load(resource_path("assets/images/snake/turn/body-1/body-1-up-right.png")),
        'body-1-right-down': pygame.image.load(resource_path("assets/images/snake/turn/body-1/body-1-right-down.png")),
        'body-1-down-left': pygame.image.load(resource_path("assets/images/snake/turn/body-1/body-1-down-left.png")),
        'body-1-left-up': pygame.image.load(resource_path("assets/images/snake/turn/body-1/body-1-left-up.png")),
        'body-1-up-left': pygame.image.load(resource_path("assets/images/snake/turn/body-1/body-1-up-left.png")),
        'body-1-left-down': pygame.image.load(resource_path("assets/images/snake/turn/body-1/body-1-left-down.png")),
        'body-1-down-right': pygame.image.load(resource_path("assets/images/snake/turn/body-1/body-1-down-right.png")),
        'body-1-right-up': pygame.image.load(resource_path("assets/images/snake/turn/body-1/body-1-right-up.png")),
        
        # Add rotation images for body-2
        'body-2-up-right': pygame.image.load(resource_path("assets/images/snake/turn/body-2/body-2-up-right.png")),
        'body-2-right-down': pygame.image.load(resource_path("assets/images/snake/turn/body-2/body-2-right-down.png")),
        'body-2-down-left': pygame.image.load(resource_path("assets/images/snake/turn/body-2/body-2-down-left.png")),
        'body-2-left-up': pygame.image.load(resource_path("assets/images/snake/turn/body-2/body-2-left-up.png")),
        'body-2-up-left': pygame.image.load(resource_path("assets/images/snake/turn/body-2/body-2-up-left.png")),
        'body-2-left-down': pygame.image.load(resource_path("assets/images/snake/turn/body-2/body-2-left-down.png")),
        'body-2-down-right': pygame.image.load(resource_path("assets/images/snake/turn/body-2/body-2-down-right.png")),
        'body-2-right-up': pygame.image.load(resource_path("assets/images/snake/turn/body-2/body-2-right-up.png")),
        
        # Add rotating images for the tail
        'tail-up-right': pygame.image.load(resource_path("assets/images/snake/turn/tail/tail-up-right.png")),
        'tail-right-down': pygame.image.load(resource_path("assets/images/snake/turn/tail/tail-right-down.png")),
        'tail-down-left': pygame.image.load(resource_path("assets/images/snake/turn/tail/tail-down-left.png")),
        'tail-left-up': pygame.image.load(resource_path("assets/images/snake/turn/tail/tail-left-up.png")),
        'tail-up-left': pygame.image.load(resource_path("assets/images/snake/turn/tail/tail-up-left.png")),
        'tail-left-down': pygame.image.load(resource_path("assets/images/snake/turn/tail/tail-left-down.png")),
        'tail-down-right': pygame.image.load(resource_path("assets/images/snake/turn/tail/tail-down-right.png")),
        'tail-right-up': pygame.image.load(resource_path("assets/images/snake/turn/tail/tail-right-up.png"))
    }
}

# Common window dimensions
dis_width = 1000
dis_height = 666

# Playing field size
game_field_width = 800
game_field_height = 500

# Playfield offset
game_offset_x = (dis_width - game_field_width) // 2  # Center by width
game_offset_y = dis_height - game_field_height  # Press to the bottom border

# Display initialization
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Clock for FPS control
paused = False
clock = pygame.time.Clock()

# Snake block size and speed
snake_block = 25

snake_speed = 3  # initial speed
max_speed = 10  # maximum speed
speed_increment = 0.5  # how much to increase speed


# Resize images to fit snake size (food size)
for i in range(len(food_images)):
    food_images[i] = pygame.transform.scale(food_images[i], (snake_block, snake_block))

# Resizing head, body and tail images to fit the size of the snake (snake_block size)
for direction in snake_images:
    for part in snake_images[direction]:
        snake_images[direction][part] = pygame.transform.scale(snake_images[direction][part], (snake_block, snake_block))

# Loading a custom font
score_font = pygame.font.Font(resource_path("assets/fonts/Matemasie-Regular.ttf"), 35)  # Font for invoice
name_font_title = resource_path("assets/fonts/SankofaDisplay-Regular.ttf")
name_font_regular = resource_path("assets/fonts/MedievalSharp-Regular.ttf")

background_game = pygame.transform.scale(pygame.image.load(resource_path("assets/images/background_game.jpg")), (dis_width, dis_height))
background_snake = pygame.transform.scale(pygame.image.load(resource_path("assets/images/background_snake.jpg")), (dis_width, dis_height))
background_menu = pygame.transform.scale(pygame.image.load(resource_path("assets/images/menu.jpg")), (dis_width, dis_height))
background_game_over = pygame.transform.scale(pygame.image.load(resource_path("assets/images/background_game_over.jpg")), (dis_width, dis_height))
