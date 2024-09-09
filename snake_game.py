import sys
import pygame
import settings
import random
from functions import draw_text, show_countdown, update_speed, show_pause_message, random_round_creating_food_with_screen_difference, main_buttons, your_score, center_button_x, center_button_y, draw_main_menu_button, check_main_menu_button_click, save_high_score, load_high_score, draw_button_with_hover, draw_back_button, check_back_button_click
from game_logic import Snake, draw_grid

# Main function of the game
def gameLoop():
    try:
        global paused
        paused = False  # Initially pause is disabled
        game_over = False
        game_close = False
        new_record = False

        # Initialize the snake
        snake = Snake(settings.snake_block, settings.game_field_width, settings.game_field_height, settings.game_offset_x, settings.game_offset_y)
        high_score = load_high_score()  # Load the current record

        # Reset speed to initial
        settings.snake_speed = 3

        # Function to generate food without placing it under the snake
        def generate_food_avoiding_snake(snake_list):
            while True:
                foodx = random_round_creating_food_with_screen_difference(0, settings.game_field_width, settings.game_offset_x)
                foody = random_round_creating_food_with_screen_difference(0, settings.game_field_height, settings.game_offset_y)

                # Check that food does not appear in a place where there are already snake segments
                if not any(block['pos'] == [foodx, foody] for block in snake_list):
                    break

            return foodx, foody

        foodx, foody = generate_food_avoiding_snake(snake.snake_list)
        
        # Select a random image for food
        food_image = random.choice(settings.food_images)

        # Show countdown 3... 2... 1... GO!
        show_countdown()

        while not game_over:
            while game_close:
                settings.dis.blit(settings.background_game_over, (0, 0))
                if new_record:
                    draw_text("New High Score! Congratulations!", settings.yellow, -150, settings.name_font_regular, 35)
                draw_text("Game Over!", settings.red, -50, settings.name_font_regular, 60)
                draw_text("Press C to Play Again", settings.white, 50, settings.name_font_regular, 35)
                draw_text("R to Reset High Score, or B to go to Menu", settings.white, 100, settings.name_font_regular, 35)
                your_score(snake.length - 2, high_score - 1)  # We transmit both the current score and the record
                draw_main_menu_button(game_menu)
                pygame.display.update()

                # Handling events after a loss
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            save_high_score(high_score)  # Save the record before restarting
                            gameLoop()
                        if event.key == pygame.K_r:  # Resetting the record
                            high_score = 0
                            save_high_score(high_score)
                            gameLoop()
                        if event.key == pygame.K_b:
                            game_menu()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        check_main_menu_button_click(mouse_pos, game_menu)

            # Handling events in the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        snake.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT:
                        snake.direction = 'RIGHT'
                    elif event.key == pygame.K_UP:
                        snake.direction = 'UP'
                    elif event.key == pygame.K_DOWN:
                        snake.direction = 'DOWN'
                    elif event.key == pygame.K_p:  # Add a pause to the "P" key
                        pause_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    check_main_menu_button_click(mouse_pos, game_menu)
       
            # If the game is not paused
            if not paused:
                # Snake movement
                snake.move(snake.direction, foodx, foody)

                # Collision check
                if snake.check_collision():
                    game_close = True

                # Rendering game objects
                settings.dis.blit(settings.background_game, (0, 0))
                pygame.draw.rect(settings.dis, settings.white, [settings.game_offset_x, settings.game_offset_y, settings.game_field_width, settings.game_field_height], 2)
                
                # Draw the grid
                draw_grid()

                # Rendering food image
                settings.dis.blit(food_image, (foodx, foody))

                snake.draw()
                your_score(snake.length - 2, high_score - 1)  # We transmit both the current score and the record
                draw_main_menu_button(game_menu)

                # Check for a new record
                if snake.length - 1 > high_score:
                    high_score = snake.length - 1
                    new_record = True
                    save_high_score(high_score) 

                # Snake eats food
                if abs(snake.head[0] - foodx) < settings.snake_block and abs(snake.head[1] - foody) < settings.snake_block:
                    
                    foodx, foody = generate_food_avoiding_snake(snake.snake_list)

                    snake.grow()

                    # Update speed
                    update_speed()

                    # Select a new food image
                    food_image = random.choice(settings.food_images)

                pygame.display.update()
           
                # Update FPS
                settings.clock.tick(settings.snake_speed)

        # Saving the record after finishing the game
        save_high_score(high_score)

    except Exception as e:
        print(f"An error occurred: {e}")

    pygame.quit()
    print("Game exited")
    sys.exit()


# Game menu
def game_menu():
    menu = True

    while menu:
        settings.dis.blit(settings.background_snake, (0, 0))
        # Draw neon text "Snake Game" with stroke and shadow
        draw_text("Snake Game", settings.neon_color, 255, settings.name_font_title, 80)
        
        # Отрисовываем кнопки
        main_buttons(0, "Start New Game", gameLoop)
        main_buttons(1, "Reset High Score", reset_high_score)
        main_buttons(2, "Rules", show_rules)
        main_buttons(3, "Controls", show_controls)
        main_buttons(4, "Exit", pygame.quit)

        pygame.display.update()
  
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    gameLoop()
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    reset_high_score()
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    show_rules()
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    show_controls()
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    pygame.quit()
                    sys.exit()

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if settings.dis_height / 2 - 30 <= mouse_pos[1] <= settings.dis_height / 2:
                    gameLoop()
                elif settings.dis_height / 2 + 10 <= mouse_pos[1] <= settings.dis_height / 2 + 40:
                    reset_high_score()
                elif settings.dis_height / 2 + 50 <= mouse_pos[1] <= settings.dis_height / 2 + 80:
                    show_rules()
                elif settings.dis_height / 2 + 90 <= mouse_pos[1] <= settings.dis_height / 2 + 120:
                    show_controls()
                elif settings.dis_height / 2 + 130 <= mouse_pos[1] <= settings.dis_height / 2 + 160:
                    pygame.quit()
                    sys.exit()

# Display rules
def show_rules():
    rules = True
    while rules:
        settings.dis.blit(settings.background_menu, (0, 0))
        
        # Clear the screen and display the rules
        draw_text("Rules", settings.neon_color, -130, settings.name_font_regular, 60)
        draw_text("1. Use arrow keys to move the snake.", settings.white, -60, settings.name_font_regular, 30)
        draw_text("2. Eat the blue squares to grow.", settings.white, -20, settings.name_font_regular, 30)
        draw_text("3. Don't run into the walls or yourself.", settings.white, 20, settings.name_font_regular, 30)
        draw_text("Press B to go back to the main menu", settings.white, 170, settings.name_font_regular, 30)

        # Draw the "Back" button
        draw_back_button(game_menu)
        
        # Refresh the screen
        pygame.display.update()

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    rules = False
                    game_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                check_back_button_click(mouse_pos, game_menu)

# Display controls
def show_controls():
    controls = True
    while controls:
        # Clear the screen and display text for control
        settings.dis.blit(settings.background_menu, (0, 0))

        draw_text("Controls", settings.neon_color, -130, settings.name_font_regular, 60)
        draw_text("Arrow Keys: Move", settings.white, -50, settings.name_font_regular, 30)
        draw_text("C: Play Again after Game Over", settings.white, -10, settings.name_font_regular, 30)
        draw_text("R: Reset High Score after Game Over", settings.white, 30, settings.name_font_regular, 30)
        draw_text("Q: Quit the game", settings.white, 70, settings.name_font_regular, font_size=30)
        draw_text("Press B to go back to the main menu", settings.white, 170, settings.name_font_regular, 30)

        # Draw the "Back" button
        draw_back_button(game_menu)
        
        # Refresh the screen
        pygame.display.update()

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    controls = False
                    game_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                check_back_button_click(mouse_pos, game_menu)

# Reset records
def reset_high_score():
    reset_screen = True
    save_high_score(0)  # Reset the record immediately upon entering the reset screen
    
    while reset_screen:
        # Clear the screen and draw text and button
        settings.dis.blit(settings.background_menu, (0, 0))

        draw_text("High Score has been reset!", settings.neon_color, -50, settings.name_font_regular, 60)
        draw_text("Press B to go back to the main menu", settings.white, 170, settings.name_font_regular, 30)
        draw_back_button(game_menu)
        pygame.display.update()

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    reset_screen = False
                    game_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                check_back_button_click(mouse_pos, game_menu)

# Function to handle pause
def pause_game():
    global paused
    paused = True
    show_pause_message()
        
    # Pause loop
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # If you press the P key, unpause
                    paused = False
                elif event.key == pygame.K_b:  # If you press the B key, exit to the main menu
                    paused = False
                    game_menu()  # Call the function to go to the main menu
              
        # Draw the "Main Menu" button on the screen
        draw_main_menu_button(game_menu)

        # Fix FPS during pause
        settings.clock.tick(5)

        # Update the display
        pygame.display.update()

if __name__ == "__main__":
    game_menu()