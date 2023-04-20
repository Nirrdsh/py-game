import pgzrun
import random
import time
import pygame.time
# import pygame

TITLE = "Brickbreaker"

# initial score is 0
# time is use to get the initial time and stores in the variable 'start time'
score = 0
# as ball hits the brick, score changes by 10
score_point = 10
start_time = time.time ()
elapsed_time = 0

# setting the size of the game window and number of bricks per row
WIDTH = 640
HEIGHT = 480
PADDLE_HEIGHT = 1
BRICKS_PER_ROW = 10

# setting the paddle initial position
paddle = Actor("paddlered.png")
paddle.x = 320
paddle.y = 440

# choosing the ball type and setting the initial ball position
ball = Actor("ballgrey.png")
ball.x = 320
ball.y = 340

# setting the initial speed
ball_x_speed = 2
ball_y_speed = 2

bricks = []
# placing the bricks in the screen
current_brick_pos_x = 64 / 2
current_brick_pos_y = 32 / 2

# Brick sprites are 64 by 32
# defining the code for different types of bricks
brick_sprites = ["element_green_rectangle.png", "element_yellow_rectangle.png", "element_red_rectangle.png"]
middle_brick = ["element_grey_rectangle.png"]

# this will be used to check if the game is over or not so that it can be used to restart and set everything back to its orignal position
game_over_box = False

# if we want to display any thing on the screen like ball, paddle, score; it must be written in this function
def draw():
    global start_time
    screen.fill((100, 149, 237))
    paddle.draw()
    ball.draw()
    for brick in bricks:
        brick.draw()
    # to draw the score and elapsed time
    screen.draw.text("Score: " + str(score), bottomleft=(10, 480), color="red")
    update_elapsed_time()
    screen.draw.text("Time: " + str(elapsed_time), bottomright = (630, 480), color = "red")
    #if game is over it will call game over function to draw the message
    game_over()


def update_elapsed_time():
    global elapsed_time
    global start_time
    # this is the main code to checking the time
    # first it checks the universal(device) time(which will be our start time) 
    # so as the game goes on it frequently keeps on subtracting the initial time from latest time
    elapsed_time = int(time.time() - start_time)


def update_paddle():
    # it will check the mouse coordinates horizontally 
    # if its horizontal it will move the paddle with the mouse
    global paddle
    if pygame.mouse.get_rel()[0] != 0:
        paddle.x = pygame.mouse.get_pos()[0]

    # if the mouse is not moving it will follow the keys
    else:
        if keyboard.a:
            if (paddle.x - 4 > + 52):
                paddle.x = paddle.x - 4
        if keyboard.d:
            if (paddle.x + 4 < 640 - 48):
                paddle.x = paddle.x + 4


# updates the position of given parameters 
def update_ball():
    global ball_x_speed
    global ball_y_speed
    global score
    global game_over_box


    ball.x = ball.x + ball_x_speed
    ball.y = ball.y + ball_y_speed

    # checks weather the ball has hit the side walls
    if (ball.x > WIDTH - 16) or (ball.x < 0):
        ball_x_speed = ball_x_speed * -1

    # checks weather the ball has hit the top or bottom wall, here speed -1 means reverse the direction
    if (ball.y > HEIGHT - 16) or (ball.y < 0):
        ball_y_speed = ball_y_speed * -1

    # checks weather the ball had collide with paddle, if yes reverse the direction
    if ball.colliderect(paddle):
        ball_y_speed = ball_y_speed * -1

    # checks the ball position, if collided at the bottom, the condition gave over becomes true
    # which will draw the game over sign in the screen
    if (ball.y > HEIGHT - 16):
        game_over_box = True

    for brick in bricks:

        # checks the condition if ball collide with the bricks,the bricks gets removed
        # and speed becomes -1, ball returns
        # score increases by 10
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_y_speed = ball_y_speed * -1
            score = score + score_point


def update():
    update_paddle()
    update_ball()
    update_elapsed_time()


# this function is used to create the row of bricks with the given sprite and position
def place_brick_row(sprite, pos_x, pos_y):
    any_brick = BRICKS_PER_ROW // 2
    for i in range(BRICKS_PER_ROW):
        brick = Actor(sprite)
        brick.x = pos_x + i * 64
        brick.y = pos_y
        if i == any_brick:
            any_brick = random.choice(middle_brick)
            brick.image = any_brick
        bricks.append(brick)


for brick_sprite in brick_sprites:
    place_brick_row(brick_sprite, current_brick_pos_x, current_brick_pos_y)
    current_brick_pos_y += 32


def game_over():
    if game_over_box:
        message = "Game Over"
        restart_game = "Press Enter to Restart"
        message_width = len(message) * 30
        message_height = 50
        # draws the message in the screen game over and want to restart
        screen.draw.filled_rect(
            Rect(WIDTH / 2 - message_width / 2, HEIGHT / 2 - message_height / 2, message_width, message_height),
            (255, 0, 0))
        screen.draw.text(message, center=(WIDTH / 2, HEIGHT / 2), fontsize=40, color="white")
        screen.draw.text(restart_game, center=(WIDTH / 2, HEIGHT / 1.5), fontsize=40, color="white")
        # if user press enter it will call restart function
        if keyboard.RETURN:
            restart()


# reset everything back as usual
def restart():
    global score, ball_x_speed, ball_y_speed, game_over_box, current_brick_pos_x, current_brick_pos_y, bricks, start_time, elapsed_time

    score = 0
    start_time = time.time()
    elapsed_time = 0

    ball.x = 320
    ball.y = 340
    ball_x_speed = 2
    ball_y_speed = 2
    paddle.x = 320
    paddle.y = 440
    bricks = []
    current_brick_pos_x = 64 / 2
    current_brick_pos_y = 32 / 2

    current_brick_pos_y = 32 / 2
    for brick_sprite in brick_sprites:
        place_brick_row(brick_sprite, current_brick_pos_x, current_brick_pos_y)
        current_brick_pos_y += 32

    game_over_box = False


pgzrun.go()