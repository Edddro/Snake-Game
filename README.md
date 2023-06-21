# Snake Game
Snake is a video game that involves controlling a two-dimensional snake that moves around a playing field filled with tiles and eats apples while avoiding obstacles, with the goal of growing the snake as long as possible without crashing into walls or the snake's own body. Developed as an ISC2O final project (ISU Project).

# Table of Contents
> 1. [Usage](#Usage)
> 2. [How to Play](#How-to-Play)
> 3. [Files](#Files)

# Usage
To run the game, run `python3 main.py`. This will execute the main code file, where all the code for the snake game is found. Also, ensure that all the files are in the proper paths (more information about this can be found under [files](#Files)).

# How to Play
## Menu
> Refer to the [menu images](#Menu-1)

When the program begins, a menu screen will appear on the user's screen, which displays two buttons: a bigger one on the left that says `Play`, and a smaller one on the right of `Play` that shows an image of a snake. Clicking the smaller button that displays the snake image will alter the snake's speed. If the snake is green and blue, it will move at 10 frames per second, while if the snake is red and blue, it will move at 20 frames per second, and if the snake is a question mark, the speed will randomize between 10 and 20 frames per second (which changes every game).

## Main Game
After clicking `Play` in the menu, the window will display a snake, which moves to the right of the user's screen automatically. The objective of the game is to prevent the snake from colliding with itself or any walls (the green border outside the tiles) and collecting apples. The user can move the snake by using arrow keys, or `W`, `A`, `S` and `D`, where `W` moves the snake upwards, `A` moves the snake to the left, `S` moves the snake downwards, and `D` moves the snake to the right. It is also important to note that the snake cannot move backwards; instead, it can only continue moving straight or perpendicular. For instance, if the snake is moving to the right, the user can only move the snake up or down or continue letting the snake move to the right. When the snake collides with an apple, the user's score increases by one, and if necessary, the user's high score also updates, which is shown on the top left of the grid. However, when collecting an apple, the snake grows longer by one tile (or one new body image is added), making it more difficult to prevent colliding with the snake.

## Game Over
The game ends once the snake collides with itself or the wall, and text saying `Game Over` appears on the centre of the grid. After three seconds, the window will change back to the menu screen, where it will display the user's score for the game, the user's high score, and the user's option to change the difficulty of the game. It is also important to note that the game runs infinitely until the user closes the window.

# Files
Snake Game consists of many files, including the main Python file, graphics for the snake and objects (such as the apple and trophy images), and sound. The files are listed in more detail below:

### [Main.py](./main.py)
As stated above, [main.py](./main.py) consists of the main Python code used to create the snake game. In this file, the game loads the other files from their paths (including fonts, images, and sounds), deals with events, and deals with drawing the game on the user's screen, which includes drawing the snake and apple at the appropriate position as well as displaying the proper scene on the user's screen.

### [Fonts](./Font)
The game uses [PoetsenOne-Regular](./Font/PoetsenOne-Regular.ttf) for the text in the game, which includes the user's score, "game over" text, and text on the "play" button.

### [Sounds](./Sounds)
The game contains three sound files. This includes the [crash sound](./Sounds/crash.mp3) when the snake collides with a wall or itself, the [crunch sound](./Sounds/crunch.mp3) when the snake consumes an apple, and the [move sound](./Sounds/move.mp3) when the user clicks a key to move the snake.

### [Graphics](./Graphics)
One of the major graphics in Snake Game are the images used to render the snake; however, other images include images on the main screen such as the background image, the image for the speed of the snake, and an apple that spawns randomly on the grid. These graphics are sorted below:

#### Snake 
By default, the snake is facing the right direction, but the images are rotated if necessary based on the direction the snake is heading. However, the game contains four images for each turning position instead of rotating them.

![Head image](./Graphics/head_right.png)
[Head image](./Graphics/head_right.png)

![Body image](./Graphics/body_horizontal.png)
[Body image](./Graphics/body_horizontal.png)

![Tail image](./Graphics/tail_left.png)
[Tail image](./Graphics/tail_left.png)

![Turn image - top left](./Graphics/turn_top_left.png)
[Turn image - top left](./Graphics/turn_top_left.png)

![Turn image - top right](./Graphics/turn_top_right.png)
[Turn image - top right](./Graphics/turn_top_right.png)

![Turn image - bottom left](./Graphics/turn_bottom_left.png)
[Turn image - bottom left](./Graphics/turn_bottom_left.png)

![Turn image - bottom right](./Graphics/turn_bottom_right.png)
[Turn image - bottom right](./Graphics/turn_bottom_right.png)

#### Menu
The menu screen contains a background that is drawn with 35 x 35 pixel rectangles, a background image, an apple image, a trophy image, and images for easy, hard, and random modes.

![Background image](./Graphics/background.jpg)
[Background image](./Graphics/background.jpg) 

![Apple image](./Graphics/apple.png)
[Apple image](./Graphics/apple.png)

![Trophy image](./Graphics/trophy.png)
[Trophy image](./Graphics/trophy.png)

![Easy difficulty image](./Graphics/easy_difficulty.png)
[Easy difficulty image](./Graphics/easy_difficulty.png)

![Hard difficulty image](./Graphics/hard_difficulty.png)
[Hard difficulty image](./Graphics/hard_difficulty.png)

![Random difficulty image](./Graphics/random_difficulty.png)
[Random difficulty image](./Graphics/random_difficulty.png)

#### Main Game Background
The background in the main game is drawn with 35 x 35 pixel rectangles to fill the user's width and height but contains a green border around the tiles, where the snake cannot enter. On the background, the user's score is shown next to an apple image, and the user's high score is listed next to a trophy image.

![Apple image](./Graphics/apple.png)
[Apple image](./Graphics/apple.png)

![Trophy image](./Graphics/trophy.png)
[Trophy image](./Graphics/trophy.png)
