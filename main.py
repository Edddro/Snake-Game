'''
main.py
Edward Drobnis
June 19, 2023
Snake Game - ISC2O ISU - Move the snake to consume the apples and grow as large as possible
'''

# Imports pygame, system, and random
import pygame
import sys
import random

# Initializes pygame
pygame.init()

# Creates a full screen game window and change the display name and icon
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

# Defines the images needed for the snake, and load and resize them to 35 x 35 pixels
snake_head_img = pygame.transform.scale(pygame.image.load("./Graphics/head_right.png").convert_alpha(), (35, 35))
snake_body_img = pygame.transform.scale(pygame.image.load("./Graphics/body_horizontal.png").convert_alpha(), (35, 35))
snake_tail_img = pygame.transform.scale(pygame.image.load("./Graphics/tail_left.png").convert_alpha(), (35, 35))
snake_turn_bottom_right_img = pygame.transform.scale(pygame.image.load("./Graphics/turn_bottom_right.png").convert_alpha(), (35, 35))
snake_turn_bottom_left_img = pygame.transform.scale(pygame.image.load("./Graphics/turn_bottom_left.png").convert_alpha(), (35, 35))
snake_turn_top_right_img = pygame.transform.scale(pygame.image.load("./Graphics/turn_top_right.png").convert_alpha(), (35, 35))
snake_turn_top_left_img = pygame.transform.scale(pygame.image.load("./Graphics/turn_top_left.png").convert_alpha(), (35, 35))

# Defines and load the images needed for the emojis, as well as resize them to 30 x 30 pixels 
apple_img = pygame.transform.scale(pygame.image.load("./Graphics/apple.png").convert_alpha(), (30, 30))
trophy_img = pygame.transform.scale(pygame.image.load("./Graphics/trophy.png").convert_alpha(), (30, 30))

# Defines the background image for the menu screen
background_img = pygame.image.load("./Graphics/background.jpg").convert_alpha()

# Defines the font used in the game with a size of 30
font = pygame.font.SysFont("./Font/PoetsenOne-Regular.ttf", 30)

# Creates two variables, apple_x and apple_y, which hold the default values for the apple's coordinates (this will be used to check if the snake collides with it)
apple_x = 0
apple_y = 0

# Defines two variables, score and high_score, which holds the user's current score and high score
score = 0
high_score = 0

# Creates a variable, scene, to determine what scene to display on the user's screen
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

  # Displays the user's score and high score on the top of the grid
  score_text = font.render(f"{score}", True, BLACK)
  high_score_text = font.render(f"{high_score}", True, BLACK)
  screen.blit(apple_img, (40, 20))
  screen.blit(score_text, (75, 30))
  screen.blit(trophy_img, (115, 20))
  screen.blit(high_score_text, (150, 30))

# Sets the previous apple position to (-1, -1), so it is off the user's screen
prev_apple_x = -1
prev_apple_y = -1

# Creates a function to load the apple
def apple():
  # Allows changes to prev_apple_x and prev_apple_y to be accessed outside the function
  global prev_apple_x, prev_apple_y
  
  # Randomizes the values for x and y when the function is called, and places it in the center of the tile
  x = ((random.randint(70, WIDTH - 70) // 35) * 35) + 2
  y = ((random.randint(105, HEIGHT - 70) // 35) * 35) + 2

  # Checks if the apple is in the same position as the previous apple (to lower the chances of spawning inside the snake)
  while (x, y) == (prev_apple_x, prev_apple_y):
    x = ((random.randint(35, WIDTH - 35) // 35) * 35) + 2
    y = ((random.randint(70, HEIGHT - 35) // 35) * 35) + 2

  # Updates the value of prev_apple_x and prev_apple_y to the new position
  prev_apple_x, prev_apple_y = x, y  

  # Returns the value of x and y
  return x, y

# Creates a function to draw the snake
def draw_snake():
  # Receives the x and y coordinates of the head of the snake (from the "snake" list)
  head_x, head_y = snake[0]
  
  # If the snake is moving to the right, display the head image
  if snake_direction == "right":
    head_img = snake_head_img

  # If the snake is moving to the left, rotate the head by 180 degrees counterclockwise
  elif snake_direction == "left":
    head_img = pygame.transform.rotate(snake_head_img, 180)

  # If the snake is moving up, rotate the head by 90 degrees counterclockwise
  elif snake_direction == "up":
    head_img = pygame.transform.rotate(snake_head_img, 90)

  # If the snake is moving down, rotate the head by 270 degrees counterclockwise
  elif snake_direction == "down":
    head_img = pygame.transform.rotate(snake_head_img, 270)

  # Displays the head image on the coordinates
  screen.blit(head_img, (head_x * 35, head_y * 35 + 35))

  # Loops through the "snake" list except for the head and tail and checks the positions of the body segments around it to determine the image to display
  for i in range(1, len(snake) - 1):
    # Receives the coordinates of the body segment "i," where "i" is a number from 1 to the length of the list minus one
    body_x, body_y = snake[i]
          
    # If the neighboring segments are aligned with the current segment vertically, rotate the horizontal body image by 90 degrees counterclockwise
    if snake[i - 1][0] == body_x and snake[i + 1][0] == body_x:
      body_img = pygame.transform.rotate(snake_body_img, 90)

    # If the neighboring segments are aligned with the current segment horizontally, use the horizontal body image 
    elif snake[i - 1][1] == body_y and snake[i + 1][1] == body_y:
      body_img = snake_body_img

    # If the neighboring segments are not aligned with the current segment, use the turn image
    # Checks if the current segment of the snake's body is positioned horizontally between two neighboring segments
    elif snake[i + 1][0] == body_x and snake[i - 1][1] == body_y:

      # If the left neighboring segment is to the left of the current segment, check which direction the right neighboring segment is in relative to the current segment
      if snake[i - 1][0] < body_x:
        
        # If the right neighboring segment is positioned above the current segment, use the top left turn image
        if snake[i + 1][1] < body_y:
          body_img = snake_turn_top_left_img
          
        # If the right neighboring segment is positioned below the current segment, use the bottom left turn image
        elif snake[i + 1][1] > body_y:
          body_img = snake_turn_bottom_left_img

      # If the left neighboring segment is to the right of the current segment, check which direction the right neighboring segment is in relative to the current segment
      elif snake[i - 1][0] > body_x:

        # If the right neighboring segment is positioned above the current segment, use the top right turn image
        if snake[i + 1][1] < body_y:
          body_img = snake_turn_top_right_img

        # If the right neighboring segment is positioned below the current segment, use the bottom right turn image
        elif snake[i + 1][1] > body_y:
          body_img = snake_turn_bottom_right_img

    # Checks if the current segment of the snake's body is positioned vertically between two neighboring segments
    elif snake[i - 1][0] == body_x and snake[i + 1][1] == body_y:

      # If the bottom neighboring segment is to the left of the current segment, check which direction the top neighboring segment is in relative to the current segment
      if snake[i + 1][0] < body_x:

        # If the top neighboring segment is positioned above the current segment, use the top left turn image
        if snake[i - 1][1] < body_y:
          body_img = snake_turn_top_left_img

        # If the top neighboring segment is positioned below the current segment, use the bottom left turn image
        elif snake[i - 1][1] > body_y:
          body_img = snake_turn_bottom_left_img

      # If the bottom neighboring segment is to the right of the current segment, check which direction the top neighboring segment is in relative to the current segment
      elif snake[i + 1][0] > body_x:

        # If the top neighboring segment is positioned above the current segment, use the top right turn image
        if snake[i - 1][1] < body_y:
          body_img = snake_turn_top_right_img

        # If the top neighboring segment is positioned below the current segment, use the bottom right turn image
        elif snake[i - 1][1] > body_y:
          body_img = snake_turn_bottom_right_img
              
    # Draws the body segment image on the screen at the coordinates
    screen.blit(body_img, (body_x * 35, body_y * 35 + 35))

  # Receives the coordinates of the tail of the snake and draw it
  tail_x, tail_y = snake[-1]

  # Determines the position of the tail segment based on the position of the second-to-last segment
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

  # Draws the tail image on the screen at the appropriate position
  screen.blit(tail_img, (tail_x * 35, tail_y * 35 + 35))

# Creates a function to move the snake
def move_snake():
  # Allows changes to snake_direction, score, high_score, and scene to be accessed outside the function
  global snake_direction, score, high_score, scene

  # Removes the tail of the snake
  snake.pop()

  # Determines the new head position based on the direction the snake is heading (this is used to automatically move the snake)
  head_x, head_y = snake[0]

  # If the snake is facing right, increase head_x by one
  if snake_direction == "right":
    new_head = (head_x + 1, head_y)

    # If the head collides with the wall, move it 70 pixels right (off the user's screen)
    if new_head[0] > (WIDTH - 35) // 35:
      new_head = (head_x + 2, head_y)

  # If the snake is facing left, decrease head_x by one
  elif snake_direction == "left":
    new_head = (head_x - 1, head_y)

    # If the head collides with the wall, move it 70 pixels left (off the user's screen)
    if new_head[0] < 1:
      new_head = (head_x - 2, head_y)

  # If the snake is facing up, decrease head_y by one
  elif snake_direction == "up":
    new_head = (head_x, head_y - 1)

    # If the head collides with the wall, move it 105 pixels up (off the user's screen)
    if new_head[1] < 1:
      new_head = (head_x, head_y - 3)

  # If the snake is facing down, increase head_y by one
  elif snake_direction == "down":
    new_head = (head_x, head_y + 1)

    # If the head collides with the wall, move it 70 pixels down (off the user's screen)
    if new_head[1] > (HEIGHT - 70) // 35:
      new_head = (head_x, head_y + 2)

  # Adds the new head to the beginning of the snake list
  snake.insert(0, new_head)

  # Checks if the snake collides with the wall
  if new_head[0] < 1 or new_head[0] > (WIDTH - 35) // 35 or new_head[1] < 1 or new_head[1] >(HEIGHT - 70) // 35:
    # Plays the collision sound
    pygame.mixer.Sound("./Sounds/crash.mp3").play()

    # Displays the "game over" screen
    scene = "game over"
      
  # Checks if the snake collides with itself
  # Loops through all the objects in the snake list
  for i in range(1, len(snake)):
    # Checks if the coordinates of the head is equal to another object in the list
    if new_head == snake[i]:
      
      # Plays the collision sound
      pygame.mixer.Sound("./Sounds/crash.mp3").play()
          
      # Displays the "game over" screen
      scene = "game over"

  # Checks if the snake has eaten the apple by checking if the head is in the same coordinates as the apple
  # Allows changes to apple_x and apple_y to be accessed outside the function 
  global apple_x, apple_y
  # Checks if the coordinates of the snake's head is equal to the coordinates of the apple
  if new_head == (apple_x // 35, (apple_y - 35) // 35):

    # Plays the crunch sound
    pygame.mixer.Sound("./Sounds/crunch.mp3").play()
      
    # Updates the score and the high score if necessary (if the score is greater than the high score)
    score += 1
    if score > high_score:
      high_score = score
          
    # Moves the apple to another tile
    apple_x, apple_y = apple()
        
    # Adds a new tail to the snake
    snake.append(snake[-1])

  # Redraws the screen (background, snake, and apple) every frame to have a moving animation
  background()
  draw_snake()
  screen.blit(apple_img, (apple_x, apple_y))

  # Updates the display
  pygame.display.update()

# Creates a function to display a menu screen
def menu():
  # Allows changes to scene, snake, snake_direction, and background_rect to be accessed outside the function
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
  screen.blit(button_text, (background_rect.centerx - 5, background_rect.height + background_rect.y + 20))

  # Updates the display
  pygame.display.update()

# Creates a function to display a game over screen
def game_over():
  global scene
  
  # Displays the "game over" message
  game_over_text = font.render("Game Over", True, WHITE)
  screen.blit(game_over_text, (WIDTH // 2, HEIGHT // 2))
  pygame.display.update()
    
  # Waits for 3 seconds
  pygame.time.wait(3000)
  
  # Loads the menu screen
  scene = "menu"

# Calls the apple function to set the position of the apple 
apple_x, apple_y = apple()

# Sets up the clock to control the game's speed
clock = pygame.time.Clock()

# Starts the game loop
while True:
  # Handles events to check what key is pressed (and move the snake if the key pressed is perpendicular to or in the same direction as the snake) and to stop the program when the window is closed
  for event in pygame.event.get():
    # Stops the program when the window is closed
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

    # Checks if "W", "A", "S", "D" or any arrow keys (up, left, down, right) are clicked when the scene is in the main game ("game")
    elif event.type == pygame.KEYDOWN:
      if scene == "game":

        # Changes the snake direction to "up" if the snake was not moving down previously and "w" or the up arrow key is pressed
        if event.key == pygame.K_UP and snake_direction != "down" or event.key == pygame.K_w and snake_direction != "down":
          snake_direction = "up"
              
          # Plays the moving sound
          pygame.mixer.Sound("./Sounds/move.mp3").play()

      # Changes the snake direction to "down" if the snake was not moving up previously and "s" or the down arrow key is pressed
        elif event.key == pygame.K_DOWN and snake_direction != "up" or event.key == pygame.K_s and snake_direction != "up":
          snake_direction = "down"
              
          # Plays the moving sound
          pygame.mixer.Sound("./Sounds/move.mp3").play()

        # Changes the snake direction to "left" if the snake was not moving right previously and "a" or the left arrow key is pressed
        elif event.key == pygame.K_LEFT and snake_direction != "right" or event.key == pygame.K_a and snake_direction != "right":
          snake_direction = "left"
                
          # Plays the moving sound
          pygame.mixer.Sound("./Sounds/move.mp3").play()

        # Changes the snake direction to "right" if the snake was not moving left previously and "d" or the right arrow key is pressed
        elif event.key == pygame.K_RIGHT and snake_direction != "left" or event.key == pygame.K_d and snake_direction != "left":
          snake_direction = "right"

          # Plays the moving sound
          pygame.mixer.Sound("./Sounds/move.mp3").play()

    # Checks if the scene is menu and the mouse is clicked 
    elif event.type == pygame.MOUSEBUTTONDOWN and scene == "menu":
      
      # Checks if the button is clicked (specifically, it checks if the coordinates of the click is within the coordinates of the rectangle)
      if background_rect.x < event.pos[0] < background_rect.x + background_rect.width and background_rect.height + background_rect.y + 5 < event.pos[1] < background_rect.height + background_rect.y + 55:
        # Changes the display to the main game
        scene = "game"
        
        # Resets the apple score
        score = 0

        # Sets the default value of the snake with the snake facing right (resets the snake every game)
        snake = [(3, 7), (2, 7), (1, 7)]
        snake_direction = "right"
        
  # Displays the appropriate scene on the user's screen based on the scene name           
  # Display the game over screen if the scene is "game over"
  if scene == "game over":
    game_over()
  # Display the menu if the scene is "menu"
  elif scene == "menu":
    menu()
  # Display the main game if the scene is "game"
  elif scene == "game":
    move_snake()

  # Set the game's speed to 10 frames per second
  clock.tick(10)