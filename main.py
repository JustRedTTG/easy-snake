import pygameextra as pe
import random

"""
Code made with love by Red <3 

please use pygameextra 2 version 2.0.0b7 or older
`pip install pygameextra 2.0.0b7`

Simple snake functionality:
1. Adjustable display size
2. Simple board logic
3. Simple direction logic
4. Simple movement logic
5. Simple draw logic
6. Simple score counter
7. Simple pause, game over and reset functionality 
8. Snake gradient, personal favorite feature!


Everything is simple!
Snake is a very simple game!
Thanks to the power of pygameextra for making things even easier <3
"""

full_screen = False # Full screen preferences
mobile_controls = False # Mobile preferences

if full_screen:
    pe.init((0, 0)) # Initialize PygameExtra to width 0 and height 0, which is the maximum size
    w, h = pe.display.get_size() # Get this maximum size
else:
    pe.init() # Initialize PygameExtra
    w, h = 700, 500
    pe.display.make((w, h), mode=pe.display.DISPLAY_MODE_HIDDEN)


offset_x: int                   # Offset X
offset_y: int                   # Offset Y

board_size = 25                 # Board grid size
board_pixel_size: int           # Cell pixel size in board

time_in_milliseconds_till_movement = 120 # The variable name says it all tbh

temp = {}  # A temporary dictionary to store reoccurring things and save process time
colors = { # A colors dictionary to store all the colors used by the game
    'board outline': pe.colors.white,            # Board outline color
    'score color': pe.colors.white,              # Score text color
    'game over color': pe.colors.red,            # Game Over text color
    'game over background': pe.colors.black,     # Game Over text background
    'pause color': pe.colors.white,              # Pause text color
    'snake color': pe.colors.green,              # Snake color
    'snake color final': pe.colors.verydarkaqua, # Snake color 2
    'apple color': pe.colors.red                 # Apple color
}

board: list                       # Set the type of variable for the board to a list

snake_size: int                   # This will store the record of how long the snake is
snake_direction: int              # This variable will store the direction
snake_begin_size = 3              # Set a reference to make the score 0 when the size is the beginning size
snake_direction_change_chain = [] # Key chaining basically

enable_teleport = True # This allows the snake to go from one side to the other instead of losing the game
game_over = False      # This variable will indicate if the game has ended, and we have lost :(
pause = False          # This variable will indicate if the game is paused


def initialize_board(): # By separating this initialization we can reset the game whenever the player looses and chooses to retry!
    global board, snake_size, snake_direction
    board = [[-2 for _ in range(board_size)] for _ in range(board_size)] # Make a nested array for the board!
    # [print(*x) for x in board] # - DEBUG THE BOARD WITH THIS
    board[board_size//3][board_size//2] = 1               # Indicate that in this spot in the board is where the snake is located
    board[board_size - board_size//3][board_size//2] = -1 # Indicate that in this spot in the board is where the apple is located

    snake_size = 3      # Set a record for how long the snake is
    snake_direction = 1 # We can interpret this as 0 is up and 1 is right and so on, going clockwise


def temp_calibrate():
    global temp
    temp['board outline rect'] = (offset_x, offset_y,            # Use the offset to begin with
                                  board_size * board_pixel_size, # Calculate the dimension of the board
                                  board_size * board_pixel_size)
    temp['board outline width'] = h // 200                       # Calculate the outline width
    temp['move time requirement'] = time_in_milliseconds_till_movement / 1000 # Calculate the move time requirement
    temp['score font size'] = int((w if w > h else h) * (.035 if w > h else .04))    # Make the score text font size to be .03 times the screen width
    temp['score'] = pe.text.Text('0', 'font.ttf', temp['score font size'], (offset_x//2 if w > h else w//2, temp['score font size']), [colors['score color'], None]) # Make the score text
    temp['game over font size'] = int((board_size * board_pixel_size) * .14) # Make the game over text font size to be .14 times the game screen
    temp['pause font size'] = int((board_size * board_pixel_size) * .14)     # Same goes for the pause text
    temp['game over'] = pe.text.Text('GAME OVER', 'font.ttf', temp['game over font size'], (w//2, h//2), [colors['game over color'], colors['game over background']]) # Make the game over text
    temp['game over translucent'] = pe.text.Text('GAME OVER', 'font.ttf', temp['game over font size'], (w//2, h//2), [colors['game over color'], None])               # Make the translucent game over text
    temp['pause'] = pe.text.Text('PAUSED', 'font.ttf', temp['pause font size'], (w // 2, h // 2), [colors['pause color'], None]) # >>>                                # Make the pause text


def resize():
    global offset_x, offset_y, board_pixel_size, w, h
    w, h = pe.display.get_size()
    if w > h:
        offset_x = w // 2 - h // 2
        board_pixel_size = h // board_size
        offset_y = h // 2 - (board_size * board_pixel_size) // 2
    else:
        offset_y = h // 2 - w // 2
        board_pixel_size = w // board_size
        offset_x = w // 2 - (board_size * board_pixel_size) // 2
    temp_calibrate()


def calculate_snake_color(snake_index, translucency):
    if snake_index == 1: # If the snake index is 1, aka the snake head
        return *colors['snake color'], translucency # Return the main snake color with translucency
    snake_color_change = ( # Figure out the difference between the two snake colors
        colors['snake color final'][0] - colors['snake color'][0], # Red channel
        colors['snake color final'][1] - colors['snake color'][1], # Green channel
        colors['snake color final'][2] - colors['snake color'][2]  # Blue channel
    )
    percent_of_change = (snake_index / snake_size) # Calculate how much to fade between the colors
    return (
        colors['snake color'][0] + snake_color_change[0] * percent_of_change, # Red channel
        colors['snake color'][1] + snake_color_change[1] * percent_of_change, # Green channel
        colors['snake color'][2] + snake_color_change[2] * percent_of_change, # Blue channel
        translucency                                                          # Translucency channel
    )


def draw_board(translucency):
    x = 0                 # Set to start from the first column in the board
    x_in_pixel = offset_x # Set the x to the x offset
    y_in_pixel = offset_y # Set the y to the y offset
    while x < board_size: # Loop through the board columns
        for index, y in enumerate(board[x]): # Loop through the rows in this column
            if y == -1:                      # It's an apple, draw an apple!!
                pe.draw.ellipse((*colors['apple color'], translucency), (x_in_pixel, y_in_pixel, board_pixel_size, board_pixel_size))
            elif 0 < y <= snake_size:        # It's a part of the snake, draw a snake!!
                pe.draw.rect(calculate_snake_color(y, translucency), (x_in_pixel, y_in_pixel, board_pixel_size, board_pixel_size))
            y_in_pixel += board_pixel_size   # Increase the y value by the board pixel size
        x += 1                               # Next column
        x_in_pixel += board_pixel_size       # Increase the x value by the board pixel size
        y_in_pixel = offset_y                # Reset the y to the y offset
    pe.draw.rect((*colors['board outline'], translucency), temp['board outline rect'], temp['board outline width'])  # Draw an outline around the board


def find_snake_head():
    for xi, x in enumerate(board):         # Loop through every column in the board
        for yi, y in enumerate(board[xi]): # Loop through the row in that column
            if y == 1:                     # If it's 1, then that's the snake's head
                return xi, yi              # Return the index at which it is located!


def generate_new_apple():
    xi, yi = find_snake_head() # Find where the snake is, to prevent the apple from being too close!
    new_xi, new_yi = xi, yi    # Set the apple position where the snake is, making it an invalid position!
    # We do several checks in the following loop
    # 1. Is the apple still within a 2 blocks radius of the snake?
    # 2. Is the apple on top of the snake?
    while xi-2 <= new_xi <= xi+2 or yi-2 <= new_yi <= yi+2 or 1 <= board[new_xi][new_yi] <= snake_size:
        new_xi, new_yi = random.randint(0, board_size-1), random.randint(0, board_size-1) # Generate a random position
    # Once the loop exits it means all the checks have passed through and the apple is right where we want it!
    board[new_xi][new_yi] = -1 # Set the new apple location on the board!


def get_next_snake_position():
    xi, yi = find_snake_head() # Find the snake's head

    # Now we have to change these coordinates
    if snake_direction == 0:   # Up
        yi -= 1                # Remove one from y index, which is up in our case
    elif snake_direction == 1: # Right
        xi += 1                # Add one to x index, which is right
    elif snake_direction == 2: # Down
        yi += 1                # Add one to y index, which is down in our case
    elif snake_direction == 3: # Left
        xi -= 1                # Remove one from x index, which is left

    # Now we have to verify the position
    if xi < 0:               # The snake has gone too far to the left
        xi = board_size-1    # > We go to the right far-most side
    elif xi >= board_size:   # The snake has gone too far to the right
        xi = 0               # > We go to the left far-most side
    elif yi < 0:             # The snake has gone too far to the top
        yi = board_size-1    # > We go to the bottom far-most side
    elif yi >= board_size:   # The snake has gone too far to the bottom
        yi = 0               # > We go to the top far-most side
    else:
        return xi, yi, False # We return the snake position and False to indicate it hasn't gone too far!
    return xi, yi, True      # We return the snake position and True to indicate it has gone too far and was teleported!


def move_snake():
    global game_over, snake_size, snake_direction

    if len(snake_direction_change_chain) > 0:                          # Check if there is a chain of direction changes
        snake_direction = snake_direction_change_chain.pop(0)          # Get the first thing

    next_xi, next_yi, teleported = get_next_snake_position()           # Get the next location of the snake and whether it teleported

    for xi, x in enumerate(board):                                     # Loop through every column in the board
        board[xi] = [value + 1 if value > 0 else value for value in x] # Add one if it's larger than 0

    if teleported and not enable_teleport:          # The snake has teleported and that isn't allowed
        game_over = True                            # > Game over
    elif 1 < board[next_xi][next_yi] <= snake_size: # If the snake has bitten itself
        game_over = True                            # > Game over
    else:                                           # The snake hasn't violated any of our rules
        if board[next_xi][next_yi] == -1:           # > The snake has eaten an apple!
            snake_size += 1                         # >> GROW!
            board[next_xi][next_yi] = 1             # >> Set the new coordinate before generating the apple
            generate_new_apple()                    # >> Generate a new apple somewhere on the board
        else:
            board[next_xi][next_yi] = 1             # Set the new coordinate to 1, aka the snake's head


def update_score_text():
    string = str(snake_size-snake_begin_size) # The value that the score counter should equal
    if temp['score'].text != string:          # Check the value
        temp['score'].text = string           # Set the value
        temp['score'].init()                  # Reinitialize the text


def event_handler():
    global snake_direction, pause, game_over
    pe.event.quitcheckauto() # Quit if the X button is pressed

    new_snake_direction = -1 # Initialize the new snake direction to be no nexistent
    if pe.event.resizeCheck():
        pe.event.rundown()
        resize()
    pos = pe.mouse.pos()
    if pe.event.key_DOWN(pe.pygame.K_LEFT) or pe.event.key_DOWN(pe.pygame.K_a) or (mobile_controls and pos[0] < w//2 and h//3 <= pos[1] <= h-h//3):       # Keypress left
        new_snake_direction = 3                                                       # > Update the new snake position to left
    elif pe.event.key_DOWN(pe.pygame.K_RIGHT) or pe.event.key_DOWN(pe.pygame.K_d) or (mobile_controls and pos[0] > w//2 and h//3 <= pos[1] <= h-h//3):    # Keypress right
        new_snake_direction = 1                                                       # > Update the new snake position to right
    if pe.event.key_DOWN(pe.pygame.K_DOWN) or pe.event.key_DOWN(pe.pygame.K_s) or (mobile_controls and pos[1] > h//2 and w//3 <= pos[0] <= w-w//3):       # Keypress down
        new_snake_direction = 2                                                       # > Update the new snake position to down
    elif pe.event.key_DOWN(pe.pygame.K_UP) or pe.event.key_DOWN(pe.pygame.K_w) or (mobile_controls and pos[1] < h//2 and w//3 <= pos[0] <= w-w//3):       # Keypress up
        new_snake_direction = 0                                                       # > Update the new snake position to up
    if pe.event.key_DOWN(pe.pygame.K_ESCAPE) or pe.event.key_DOWN(pe.pygame.K_SPACE): # Keypress ESC or Space
        if game_over:          # If the game has ended and the player pressed this button
            initialize_board() # Reset the game
            game_over = False  # No longer over is it
            return             # Return
        pause = not pause      # Otherwise, pause or unpause the game

    if new_snake_direction < 0 or game_over: return # Seems there's nothing else to do

    old_snake_direction = snake_direction           # Remember the old direction

    if len(snake_direction_change_chain) > 0: # Check if there is something hiding in the chain
        # Check if the last item in the chain is the same as what we are about to put in
        if snake_direction_change_chain[len(snake_direction_change_chain) - 1] == new_snake_direction:
            return
    else:
        # Check if the direction is already that of the new direction
        if snake_direction == new_snake_direction:
            return

    if len(snake_direction_change_chain) > 0: # Check if there is something hiding in the chain
        snake_direction = snake_direction_change_chain[len(snake_direction_change_chain)-1]  # Set the next direction
    else:                                                                                    #
        snake_direction = new_snake_direction                                                # Set the next direction
    xi, yi, _ = get_next_snake_position()                        # Get the next position
    snake_direction = old_snake_direction                        # Return the variable to its previous value
    if board[xi][yi] != 2:                                       # If the snake doesn't go into itself
        snake_direction_change_chain.append(new_snake_direction) # Add the direction to the chain


initialize_board() # Initialize the board
resize()   # Calculate all temporary values
delta_time = 0     # Set a starter value for delta time
pre_delta_time = 0 # Set a starter value for the previous delta time
await_move = 0     # Set a starter value for move time

# We create a display reference using the provided width, height and full screen variables
pe.display.make((w, h), "Simple Snake", pe.display.DISPLAY_MODE_FULLSCREEN if full_screen else pe.display.DISPLAY_MODE_RESIZABLE)

while True:
    t = pe.pygame.time.get_ticks()                     # Get the ticks
    [event_handler() for pe.event.c in pe.event.get()] # Handle the events
    pe.fill.full(pe.colors.black)                      # Drench the screen in black

    temp['score'].display()                     # Draw the score
    draw_board(150 if pause else 255)           # Draw the board, if the game is paused make it translucent
    if not pause and not game_over and await_move >= temp['move time requirement']: # Check if the game isn't over, and it's move time!
        move_snake()                            # > Move the snake
        await_move = 0                          # > Reset the move time
    elif pause:                                 # Let's take a break :)
        temp['pause'].display()                 # > Draw the paused text on screen
    elif game_over:                             # The game is over?!
        temp['game over'].display()             # Draw GAME OVER!
        draw_board(150)                         # Redraw the board but less translucent
        temp['game over translucent'].display() # Draw the translucent GAME OVER!
        # The wanted effect is that it seems like the stuff behind the text is slightly faded to make the text more readable
    else:
        await_move += delta_time             # Add delta to the move time

    update_score_text()                      # Update the score text if the snake has grown!

    delta_time = (t - pre_delta_time) / 1000 # Set the delta time
    pe.display.update()                      # Refresh the display
    pre_delta_time = t                       # Set the previous delta time