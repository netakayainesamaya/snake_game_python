import pygame
import settings

def draw_grid():
    for x in range(settings.game_offset_x, settings.game_offset_x + settings.game_field_width, settings.snake_block):
        pygame.draw.line(settings.dis, settings.grey, (x, settings.game_offset_y), (x, settings.game_offset_y + settings.game_field_height))
    for y in range(settings.game_offset_y, settings.game_offset_y + settings.game_field_height, settings.snake_block):
        pygame.draw.line(settings.dis, settings.grey, (settings.game_offset_x, y), (settings.game_offset_x + settings.game_field_width, y))

class Snake:
    def __init__(self, snake_block, field_width, field_height, field_offset_x, field_offset_y, initial_length=2):
        self.snake_block = snake_block
        self.length = initial_length
        self.snake_list = []
        self.field_width = field_width
        self.field_height = field_height
        self.field_offset_x = field_offset_x
        self.field_offset_y = field_offset_y
        self.head = [self.field_offset_x + self.field_width // 2, self.field_offset_y + self.field_height // 2]
        self.direction = 'RIGHT'
        self.turns = {} # Storing all rotations
        self.snake_list.append({'pos': list(self.head), 'direction': self.direction})
        self.happy_mode = False
        self.happy_timer = 0

    def move(self, direction, foodx, foody):
        
        # Head movement logic
        if direction == 'LEFT' and self.direction != 'RIGHT':
            self.direction = direction
        elif direction == 'RIGHT' and self.direction != 'LEFT':
            self.direction = direction
        elif direction == 'UP' and self.direction != 'DOWN':
            self.direction = direction
        elif direction == 'DOWN' and self.direction != 'UP':
            self.direction = direction
       
        # Maintain rotation if direction changes
        if self.snake_list[-1]['direction'] != self.direction:
            self.turns[tuple(self.head)] = self.direction

        # Checking the distance to food
        if abs(self.head[0] - foodx) == self.snake_block and self.head[1] == foody:
            self.happy_mode = True  # Turn on the "happy" head
            self.happy_timer = 2  # Set the timer
        elif abs(self.head[1] - foody) == self.snake_block and self.head[0] == foodx:
            self.happy_mode = True  
            self.happy_timer = 2  

        # Head movement
        if self.direction == 'LEFT':
            self.head[0] -= self.snake_block
        elif self.direction == 'RIGHT':
            self.head[0] += self.snake_block
        elif self.direction == 'UP':
            self.head[1] -= self.snake_block
        elif self.direction == 'DOWN':
            self.head[1] += self.snake_block

        # Limit movement across the field
        self.head[0] = max(self.field_offset_x, min(self.head[0], self.field_offset_x + self.field_width - self.snake_block))
        self.head[1] = max(self.field_offset_y, min(self.head[1], self.field_offset_y + self.field_height - self.snake_block))
        
        # Add a new head to the snake list
        new_head = {'pos': list(self.head), 'direction': self.direction}
        self.snake_list.append(new_head)

        # Limit the length of the snake
        if len(self.snake_list) > self.length:
            del self.snake_list[0]

        # Update rotations for the snake's body
        for i, block in enumerate(self.snake_list[:-1]):  # We go through all the blocks except the head
            block_pos = tuple(block['pos'])
            if block_pos in self.turns:  # If the block is at the turning point
                block['direction'] = self.turns[block_pos]  # Change the direction of the block when turning

        tolerance = 10  # Allowable difference in coordinates to remove a turn
        tail_pos = tuple(self.snake_list[0]['pos'])  # Tail position
        for turn_pos in list(self.turns.keys()):  # Go through all saved turns 
            # Check if the tail is near the turn, taking into account the permissible error
            if abs(tail_pos[0] - turn_pos[0]) < tolerance and abs(tail_pos[1] - turn_pos[1]) < tolerance:
                del self.turns[turn_pos]
                break  # Removed the rotation, exit the loop

        # Update the state of "happiness"
        if self.happy_mode:
            self.happy_timer -= 1
            if self.happy_timer <= 0:
                self.happy_mode = False

    def grow(self):
        self.length += 1
        self.happy_mode = True
        self.happy_timer = 2  # "Happiness" for 2 frames

    def check_collision(self):
        if (self.head[0] < self.field_offset_x or
                self.head[0] >= self.field_offset_x + self.field_width or
                self.head[1] < self.field_offset_y or
                self.head[1] >= self.field_offset_y + self.field_height):
            return True

        for block in self.snake_list[:-1]:
            if block['pos'] == self.head:
                return True

        return False
    
    def draw(self):

        #1. We check whether there are turns in the snake and if so, how many
        def find_turns(self):
            turns_list = []  # Initialize the list before the loop
            for i, block in enumerate(self.snake_list):
                if i == 0:  # Skip the first block since it has no previous one
                    continue

                prev_block = self.snake_list[i - 1]
                prev_direction = prev_block['direction']
                current_direction = block['direction']

                if prev_direction != current_direction:
                    turns_list.append(i)

            # Return the list of turns only after the loop completes
            if len(turns_list) > 0:
                turns_list.sort(reverse=True)
            
            return turns_list
        
        def draw_all_blocks_in_turns_case(self):
            for i, block in enumerate(self.snake_list):
                if 'image' in block:
                    image = block['image']  # Use the saved image
                else:
                    # Normal logic for body and tail if there is no rotation
                    if i == len(self.snake_list) - 1:  # Snake head
                        if self.happy_mode:
                            image = settings.snake_images[block['direction']]['happy_head']
                        else:
                            image = settings.snake_images[block['direction']]['head']
                    elif i == 0:  # Tail
                        image = settings.snake_images[block['direction']]['tail']
                    elif i % 2 == 0:  # body-1
                        image = settings.snake_images[block['direction']]['body-1']
                    else:  # body-2
                        image = settings.snake_images[block['direction']]['body-2']
   
                # Drawing a block
                settings.dis.blit(image, block['pos'])
        
        turns_list = find_turns(self)

        # 2. We check whether we have turns, if so, then we check one or more, if not, we draw as usual
        if len(turns_list) > 0:
            # count how many turns
            len_turns_list = len(turns_list)
            if len_turns_list > 1:
                # print('len_turns_list > 1', len(turns_list))
                for j in turns_list:
                    turn_index = j
                    # print('turn_index', turn_index)
                    for i, block in enumerate(self.snake_list):
                        if i == len(self.snake_list) - 1:  # Snake head
                            if self.happy_mode:  # "Happy" head
                                image = settings.snake_images[block['direction']]['happy_head']
                            else:
                                image = settings.snake_images[block['direction']]['head']
                        else:
                            prev_block = self.snake_list[turn_index - 1]
                            prev_direction = prev_block['direction']
                            current_direction = self.snake_list[turn_index]['direction']
                            if i <= turn_index:
                                if i == turn_index:
                                    block['image'] = self.get_turn_image(prev_direction, current_direction)
                                elif i == 0:  # Tail
                                    block['image'] = self.get_turn_image_tail(prev_direction, current_direction)
                                elif i % 2 == 0:  # body-1
                                    block['image'] = self.get_turn_image_body1(prev_direction, current_direction)
                                else:  # body-2
                                    block['image'] = self.get_turn_image_body2(prev_direction, current_direction)

                # Third part: draw all blocks
                draw_all_blocks_in_turns_case(self)

            elif len_turns_list == 1:

                turn_index = turns_list[0]

                for i, block in enumerate(self.snake_list):
                    if i == len(self.snake_list) - 1:  # Snake head
                        if self.happy_mode:  # "Happy" head
                            image = settings.snake_images[block['direction']]['happy_head']
                        else:
                            image = settings.snake_images[block['direction']]['head']
                    else:
                        prev_block = self.snake_list[turn_index - 1]
                        prev_direction = prev_block['direction']
                        current_direction = self.snake_list[turn_index]['direction']
                        if i <= turn_index:
                            if i == turn_index:
                                block['image'] = self.get_turn_image(prev_direction, current_direction)
                            elif i == 0:  # Tail
                                block['image'] = self.get_turn_image_tail(prev_direction, current_direction)
                            elif i % 2 == 0:  # body-1
                                block['image'] = self.get_turn_image_body1(prev_direction, current_direction)
                            else:  # body-2
                                block['image'] = self.get_turn_image_body2(prev_direction, current_direction)

                # Third part: draw all blocks
                draw_all_blocks_in_turns_case(self)

        else:
            for i, block in enumerate(self.snake_list):
                # Normal logic for body and tail if there is no rotation
                if i == len(self.snake_list) - 1:  # Snake head
                    if self.happy_mode:
                        image = settings.snake_images[block['direction']]['happy_head']
                    else:
                        image = settings.snake_images[block['direction']]['head']
                elif i == 0:  # Tail
                    image = settings.snake_images[block['direction']]['tail']
                elif i % 2 == 0:  # body-1
                    image = settings.snake_images[block['direction']]['body-1']
                else:  # body-2
                    image = settings.snake_images[block['direction']]['body-2']

                # Отрисовка блока
                settings.dis.blit(image, block['pos'])

            # Third part: drawing all the blocks
            # draw_all_blocks_in_turns_case(self)

    def get_turn_image(self, prev_direction, current_direction):
        if prev_direction == 'RIGHT' and current_direction == 'DOWN':
            return settings.snake_images['TURN']['turn-right-down']
        elif prev_direction == 'DOWN' and current_direction == 'LEFT':
            return settings.snake_images['TURN']['turn-down-left']
        elif prev_direction == 'LEFT' and current_direction == 'UP':
            return settings.snake_images['TURN']['turn-left-up']
        elif prev_direction == 'UP' and current_direction == 'RIGHT':
            return settings.snake_images['TURN']['turn-up-right']
        elif prev_direction == 'RIGHT' and current_direction == 'UP':
            return settings.snake_images['TURN']['turn-right-up']
        elif prev_direction == 'UP' and current_direction == 'LEFT':
            return settings.snake_images['TURN']['turn-up-left']
        elif prev_direction == 'LEFT' and current_direction == 'DOWN':
            return settings.snake_images['TURN']['turn-left-down']
        elif prev_direction == 'DOWN' and current_direction == 'RIGHT':
            return settings.snake_images['TURN']['turn-down-right']
        else:
            return settings.snake_images[current_direction]['body-1']
        
    def get_turn_image_body1(self, prev_direction, current_direction):
        # Rotation logic for body-1
        if prev_direction == 'RIGHT' and current_direction == 'DOWN':
            return settings.snake_images['TURN']['body-1-right-down']
        elif prev_direction == 'DOWN' and current_direction == 'LEFT':
            return settings.snake_images['TURN']['body-1-down-left']
        elif prev_direction == 'LEFT' and current_direction == 'UP':
            return settings.snake_images['TURN']['body-1-left-up']
        elif prev_direction == 'UP' and current_direction == 'RIGHT':
            return settings.snake_images['TURN']['body-1-up-right']
        elif prev_direction == 'RIGHT' and current_direction == 'UP':
            return settings.snake_images['TURN']['body-1-right-up']
        elif prev_direction == 'UP' and current_direction == 'LEFT':
            return settings.snake_images['TURN']['body-1-up-left']
        elif prev_direction == 'LEFT' and current_direction == 'DOWN':
            return settings.snake_images['TURN']['body-1-left-down']
        elif prev_direction == 'DOWN' and current_direction == 'RIGHT':
            return settings.snake_images['TURN']['body-1-down-right']
        else:
            return settings.snake_images[current_direction]['body-1']


    def get_turn_image_body2(self, prev_direction, current_direction):
        # Rotation logic for body-2
        if prev_direction == 'RIGHT' and current_direction == 'DOWN':
            return settings.snake_images['TURN']['body-2-right-down']
        elif prev_direction == 'DOWN' and current_direction == 'LEFT':
            return settings.snake_images['TURN']['body-2-down-left']
        elif prev_direction == 'LEFT' and current_direction == 'UP':
            return settings.snake_images['TURN']['body-2-left-up']
        elif prev_direction == 'UP' and current_direction == 'RIGHT':
            return settings.snake_images['TURN']['body-2-up-right']
        elif prev_direction == 'RIGHT' and current_direction == 'UP':
            return settings.snake_images['TURN']['body-2-right-up']
        elif prev_direction == 'UP' and current_direction == 'LEFT':
            return settings.snake_images['TURN']['body-2-up-left']
        elif prev_direction == 'LEFT' and current_direction == 'DOWN':
            return settings.snake_images['TURN']['body-2-left-down']
        elif prev_direction == 'DOWN' and current_direction == 'RIGHT':
            return settings.snake_images['TURN']['body-2-down-right']
        else:
            return settings.snake_images[current_direction]['body-2']


    def get_turn_image_tail(self, prev_direction, current_direction):
        # Tail rotation logic
        if prev_direction == 'RIGHT' and current_direction == 'DOWN':
            return settings.snake_images['TURN']['tail-right-down']
        elif prev_direction == 'DOWN' and current_direction == 'LEFT':
            return settings.snake_images['TURN']['tail-down-left']
        elif prev_direction == 'LEFT' and current_direction == 'UP':
            return settings.snake_images['TURN']['tail-left-up']
        elif prev_direction == 'UP' and current_direction == 'RIGHT':
            return settings.snake_images['TURN']['tail-up-right']
        elif prev_direction == 'RIGHT' and current_direction == 'UP':
            return settings.snake_images['TURN']['tail-right-up']
        elif prev_direction == 'UP' and current_direction == 'LEFT':
            return settings.snake_images['TURN']['tail-up-left']
        elif prev_direction == 'LEFT' and current_direction == 'DOWN':
            return settings.snake_images['TURN']['tail-left-down']
        elif prev_direction == 'DOWN' and current_direction == 'RIGHT':
            return settings.snake_images['TURN']['tail-down-right']
        else:
            return settings.snake_images[current_direction]['tail']