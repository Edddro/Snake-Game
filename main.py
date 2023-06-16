'''
main.py
Edward Drobnis
June 9, 2023
Snake Game - ISC2O ISU - Move the snake to eat the apples and get as long as possible
'''

# Import pygame, system, and random
import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Create a full screen game window and change the display name and icon
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Snake Game | ISC2O ISU")
icon = pygame.image.load("./Graphics/head_right.png")
pygame.display.set_icon(icon)

# Creates two CONSTANT variables, height and width, which receive values from the full screen size
WIDTH = screen.get_width()
HEIGHT = screen.get_height()

# Colours
GREEN = (162, 209, 73)
LIGHT_GREEN = (170, 215, 81)
DARK_GREEN = (154, 203, 65)
BLUE = (26, 115, 232)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define the images needed for the snake, and load and resize them to 35 x 35 pixels
snake_head_img = pygame.transform.scale(pygame.image.load("./Graphics/head_right.png").convert_alpha(), (35, 35))
snake_body_img = pygame.transform.scale(pygame.image.load("./Graphics/body_horizontal.png").convert_alpha(), (35, 35))
snake_tail_img = pygame.transform.scale(pygame.image.load("./Graphics/tail_left.png").convert_alpha(), (35, 35))
snake_turn_img = pygame.transform.scale(pygame.image.load("./Graphics/turn_bottom_right.png").convert_alpha(), (35, 35))

# Define and load the images needed for the emojis, as well as resize them to 30 x 30 pixels 
apple_img = pygame.transform.scale(pygame.image.load("./Graphics/apple.png").convert_alpha(), (30, 30))
trophy_img = pygame.transform.scale(pygame.image.load("./Graphics/trophy.png").convert_alpha(), (30, 30))

# Define the background image for the menu screen and resize it to the user's screen size
background_img = pygame.image.load("./Graphics/background.jpg").convert_alpha()

# Defines the font used in the game with a size of 30
font = pygame.font.SysFont("./Font/PoetsenOne-Regular.ttf", 30)

# Set up the default values for the apple's coordinates (this will be used to check if the snake collides with it)
apple_x = 0
apple_y = 0

# Defines two variables, score and high_score, which holds the user's current score and high score
score = 0
high_score = 0

# Creates a variable, scene, to determine what scene to display
scene = "menu"

# Creates a background function, which fills the screen with 35 x 35 tiles, as well as a green background on the top, left, right, and bottom
def background():
    screen.fill(DARK_GREEN)
    for i in range(35, WIDTH - 35, 35):
        for j in range(70, HEIGHT - 35, 35):
            if i % 2 == 0 and j % 2 == 1 or i % 2 == 1 and j % 2 == 0:
                pygame.draw.rect(screen, LIGHT_GREEN, (i, j, 35, 35))
            else:
                pygame.draw.rect(screen, GREEN, (i, j, 35, 35))

    # Displays the score and high score on the top of the grid
    score_text = font.render(f"{score}", True, BLACK)
    high_score_text = font.render(f"{high_score}", True, BLACK)
    screen.blit(apple_img, (40, 20))
    screen.blit(score_text, (75, 30))
    screen.blit(trophy_img, (115, 20))
    screen.blit(high_score_text, (150, 30))

# Set the previous apple position to (-1, -1), so it is off the user's screen
prev_apple_x = -1
prev_apple_y = -1

# Create a function to load the apple
def apple():
    # Allows changes to prev_apple_x and prev_apple_y to be accessed outside the function
    global prev_apple_x, prev_apple_y
  
    # Randomizes the values for x and y when the function is called, and places it in the center of the tile
    x = ((random.randint(35, WIDTH - 35) // 35) * 35) + 2
    y = ((random.randint(70, HEIGHT - 35) // 35) * 35) + 2

    # Check if the apple is in the same position as the previous apple (to lower the chances of spawning inside the snake)
    while (x, y) == (prev_apple_x, prev_apple_y):
      x = ((random.randint(35, WIDTH - 35) // 35) * 35) + 2
      y = ((random.randint(70, HEIGHT - 35) //35) * 35) + 2

    # Updates the value of prev_apple_x and prev_apple_y to the new position
    prev_apple_x, prev_apple_y = x, y  

    # Returns the value of x and y
    return x, y

# Create a function to draw the snake
def draw_snake():
    # Receives the coordinates of the head of the snake (from the "snake" list) and rotates the image respectively, which is placed at the coordinates
    head_x, head_y = snake[0]
    if snake_direction == "right":
        head_img = snake_head_img
    elif snake_direction == "left":
        head_img = pygame.transform.rotate(snake_head_img, 180)
    elif snake_direction == "up":
        head_img = pygame.transform.rotate(snake_head_img, 90)
    elif snake_direction == "down":
        head_img = pygame.transform.rotate(snake_head_img, 270)
    screen.blit(head_img, (head_x * 35, head_y * 35 + 35))

    # Loops through the "snake" list except for the head and tail and checks the positions of the body segments around it to determine the image to display
    for i in range(1, len(snake) - 1):
        # Receives the coordinates of the body segment "i," where "i" is a number from 1 to the length of the list minus one
        body_x, body_y = snake[i]
          
        # If the neighboring segments are aligned with the current segment horizontally, use the horizontal body image 
        if snake[i - 1][0] == body_x and snake[i + 1][0] == body_x:
            body_img = snake_body_img
          
            # If the snake is moving up or down, rotate the image by 90 degrees to match the direction
            if snake_direction in ["up", "down"]:
                body_img = pygame.transform.rotate(body_img, 90)

        # If the neighboring segments are aligned with the current segment vertically, use the vertical body image
        elif snake[i - 1][1] == body_y and snake[i + 1][1] == body_y:
            body_img = snake_body_img

            # If the snake is moving left or right, rotate the image by 180 degrees to match the direction
            if snake_direction in ["left", "right"]:
                body_img = pygame.transform.rotate(body_img, 180)

        # If the neighboring segments are not aligned with the current segment, use the turn image
        elif (snake[i - 1][0] == body_x and snake[i + 1][1] == body_y) or (snake[i - 1][1] == body_y and snake[i + 1][0] == body_x):
            body_img = snake_turn_img

        # Draw the body segment image on the screen at the coordinates
        screen.blit(body_img, (body_x * 35, body_y * 35 + 35))

    # Receive the coordinates of the tail of the snake and draw it
    tail_x, tail_y = snake[-1]

    # Determine the position of the tail segment based on the position of the second-to-last segment
    # If the x-coordinate of the second-to-last segment is less than the x-coordinate of the tail segment, rotate the tail by 180 degrees (snake is going left)
    if snake[-2][0] < tail_x:
      tail_img = pygame.transform.rotate(snake_tail_img, 180)

    # If the x-coordinate of the second-to-last segment is greater than the x-coordinate of the tail segment, the tail is pointing right and does not need to be rotated (snake is going right)
    elif snake[-2][0] > tail_x:
      tail_img = snake_tail_img

    # If the y-coordinate of the second-to-last segment is less than the y-coordinate of the tail segment, rotate the tail by 90 degrees (snake is going up)
    elif snake[-2][1] < tail_y:
      tail_img = pygame.transform.rotate(snake_tail_img, 90)

    # Otherwise, rotate the tail by 270 degrees (snake is going down)
    else:
      tail_img = pygame.transform.rotate(snake_tail_img, 270)

    # Draw the tail image on the screen at the appropriate position
    screen.blit(tail_img, (tail_x * 35, tail_y * 35 + 35))

# Create a function to move the snake
def move_snake():
    global snake_direction, score, high_score, scene

    # Remove the tail of the snake
    snake.pop()

    # Determine the new head position by the direction the snake is heading
    head_x, head_y = snake[0]
    if snake_direction == "right":
        new_head = (head_x + 1, head_y)
    elif snake_direction == "left":
        new_head = (head_x - 1, head_y)
    elif snake_direction == "up":
        new_head = (head_x, head_y - 1)
    elif snake_direction == "down":
        new_head = (head_x, head_y + 1)

    # Add the new head to the beginning of the snake list
    snake.insert(0, new_head)

    # Check if the snake collides with the wall
    if new_head[0] < 2 or new_head[0] > (WIDTH - 70) // 35 or new_head[1] < 2 or new_head[1] > (HEIGHT - 105) // 35:
        # Collision sound
        pygame.mixer.Sound("./Sounds/crash.mp3").play()

        # Displays the "game over" screen
        scene = "game over"
      
    # Check if the snake collides with itself
    for i in range(1, len(snake)):
        if new_head == snake[i]:
          # Collision sound
          pygame.mixer.Sound("./Sounds/crash.mp3").play()
          
          # Displays the "game over" screen
          scene = "game over"

    # Check if the snake has eaten the apple by checking if the head is in the same coordinates as the apple
    global apple_x, apple_y
    if new_head == (apple_x // 35, (apple_y - 35) // 35):

      # Play crunch sound
      pygame.mixer.Sound("./Sounds/crunch.mp3").play()
      
      # Update the score and the high score if necessary
      score += 1
      if score > high_score:
        high_score = score
          
      # Move the apple
      apple_x, apple_y = apple()
        
      # Add a new tail to the snake
      snake.append(snake[-1])

    # Redraw the screen (background, snake, and apple)
    background()
    draw_snake()
    screen.blit(apple_img, (apple_x, apple_y))

    # Update the display
    pygame.display.update()

# Create a function to display a menu screen
def menu():
  global scene, snake, snake_direction, background_rect

  # Calls the background function
  background()
  
  # Gets the position of the background image and centers it
  background_rect = background_img.get_rect()
  background_rect.center = (WIDTH // 2, HEIGHT // 2)

  # Displays the score and high score on the background
  screen.blit(background_img, (background_rect))
  score_text = font.render(f"{score}", True, WHITE)
  high_score_text = font.render(f"{high_score}", True, WHITE)
  screen.blit(pygame.transform.scale(apple_img, (50, 50)), (background_rect.centerx - 70, background_rect.centery - 60))
  screen.blit(score_text, (background_rect.centerx - 50, background_rect.centery - 5))
  screen.blit(pygame.transform.scale(trophy_img, (50, 50)), (background_rect.centerx + 30, background_rect.centery - 60))
  screen.blit(high_score_text, (background_rect.centerx + 50, background_rect.centery - 5))

  # Creates a button
  pygame.draw.rect(screen, BLUE, (background_rect.x, background_rect.height + background_rect.y + 5, background_rect.width, 50))
  button_text = font.render("Play", True, WHITE)
  screen.blit(button_text, (background_rect.centerx, background_rect.height + background_rect.y + 20))

  # Update screen
  pygame.display.update()

# Create a function to end the game
def game_over():
  global scene
  
  # Display the "game over" message
  game_over_text = font.render("Game Over", True, WHITE)
  screen.blit(game_over_text, (WIDTH // 2, HEIGHT // 2))
  pygame.display.update()
    
  # Wait for 3 seconds
  pygame.time.wait(3000)
  
  # Load the menu screen
  scene = "menu"

# Call the apple function to set the position of the apple 
apple_x, apple_y = apple()

# Set up the clock to control the game's speed
clock = pygame.time.Clock()

# Start the game loop
while True:
  # Handle events to check what key is pressed (and move the snake if the key pressed is perpendicular to or in the same direction as the snake) and to stop the program when the window is closed
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      if scene == "game":
        if event.key == pygame.K_UP and snake_direction != "down" or event.key == pygame.K_w and snake_direction != "down":
          snake_direction = "up"
              
          # Moving sound
          pygame.mixer.Sound("./Sounds/move.mp3").play()
              
        elif event.key == pygame.K_DOWN and snake_direction != "up" or event.key == pygame.K_s and snake_direction != "up":
          snake_direction = "down"
              
          # Moving sound
          pygame.mixer.Sound("./Sounds/move.mp3").play()
              
        elif event.key == pygame.K_LEFT and snake_direction != "right" or event.key == pygame.K_a and snake_direction != "right":
          snake_direction = "left"
                
          # Moving sound
          pygame.mixer.Sound("./Sounds/move.mp3").play()
              
        elif event.key == pygame.K_RIGHT and snake_direction != "left" or event.key == pygame.K_d and snake_direction != "left":
          snake_direction = "right"

          # Moving sound
          pygame.mixer.Sound("./Sounds/move.mp3").play()
    elif event.type == pygame.MOUSEBUTTONDOWN and scene == "menu":
      # Checks if the button is clicked
      if background_rect.x < event.pos[0] < background_rect.x + background_rect.width and background_rect.height + background_rect.y + 5 < event.pos[1] < background_rect.height + background_rect.y + 55:
        # Changes the display to the main game
        scene = "game"
        
        # Resets the apple score
        score = 0

      # Sets the default value of the snake with the snake facing right (resets the snake every game)
      snake = [(3, 7), (2, 7), (1, 7)]
      snake_direction = "right"
        
  # Displays the appropriate scene           
  if scene == "game over":
    game_over()
  elif scene == "menu":
    menu()
  else:
    # Call the "move_snake" function to move the snake
    move_snake()

  # Set the game's speed to 10 frames per second
  clock.tick(10)