# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

w_key_pressed = False
s_key_pressed = False
up_key_pressed = False
down_key_pressed = False

# initialize ball_pos and ball_vel for new bal in middle of table

# helper function
def calculate_paddle_pos(paddle_pos, paddle_vel):
    paddle_pos += paddle_vel    
    if paddle_pos + paddle_vel <= 0:
        paddle_pos = 0
    elif paddle_pos + paddle_vel >= HEIGHT - PAD_HEIGHT:
        paddle_pos = HEIGHT - PAD_HEIGHT
    return paddle_pos

def is_ball_collide_vertical(vertical_pos):
    collide_left = vertical_pos <= (PAD_WIDTH + BALL_RADIUS)
    collide_right = vertical_pos > (WIDTH - 1 - PAD_WIDTH - BALL_RADIUS)
    
    if collide_left or collide_right:
        return True
    return False

def is_ball_collide_horizontal(horizontal_pos):    
    collide_top = horizontal_pos <= BALL_RADIUS
    collide_bottom = horizontal_pos >= HEIGHT -1 -BALL_RADIUS 
    
    if collide_top or collide_bottom:
        return True
    return False

def is_collide_left_wall(ball_pos):
    return ball_pos <= PAD_WIDTH+BALL_RADIUS

def is_collide_right_wall(ball_horizontal_pos):
    return ball_horizontal_pos >= WIDTH - 1 - PAD_WIDTH - BALL_RADIUS

def is_in_paddle_range(ball_vertical_pos, paddle_range):
    if ball_vertical_pos >= paddle_range[0] and ball_vertical_pos <= paddle_range[1]:
        return True
    return False

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, ball_accelerate # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0,0]
    
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240)/60
        ball_vel[1] = -random.randrange(60, 180)/60
    elif direction == LEFT:
        ball_vel[0] = -random.randrange(120, 240)/60
        ball_vel[1] = -random.randrange(60, 180)/60
    
    ball_accelerate = 1

def get_score_color(score1, score2):
    if score1 == score2:
        return ("White", "White")    
    elif score1 > score2:
        return ("Green", "Red")
    else:
        return ("Red", "Green")   
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    
    orientation = random.randrange(0,11) % 2
    if orientation == 0:
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel, ball_accelerate
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball    
    if is_ball_collide_vertical(ball_pos[0]):
        ball_vel[0] = - ball_vel[0]
    if is_ball_collide_horizontal(ball_pos[1]):
        ball_vel[1] = - ball_vel[1]
                                
        
    ball_pos[0] = ball_pos[0] + ball_accelerate * ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_accelerate * ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos = calculate_paddle_pos(paddle1_pos, paddle1_vel)
    paddle2_pos = calculate_paddle_pos(paddle2_pos, paddle2_vel)
     
    
    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos],
                         [PAD_WIDTH, paddle1_pos],
                         [PAD_WIDTH, paddle1_pos+PAD_HEIGHT], 
                         [0, paddle1_pos+PAD_HEIGHT]],
                        1, "White", "White")
    
    canvas.draw_polygon([[WIDTH-PAD_WIDTH, paddle2_pos],
                         [WIDTH, paddle2_pos], 
                         [WIDTH, PAD_HEIGHT+paddle2_pos], 
                         [WIDTH-PAD_WIDTH, PAD_HEIGHT+paddle2_pos]],
                        1, "White", "White")
    
    # draw scores
    paddle1_range = [paddle1_pos, paddle1_pos + PAD_HEIGHT]
    paddle2_range = [paddle2_pos, paddle2_pos + PAD_HEIGHT]

    if is_collide_left_wall(ball_pos[0]) and is_in_paddle_range(ball_pos[1], paddle1_range):
        print "hit left paddle, acclereate"
        ball_accelerate += 0.2
    elif is_collide_left_wall(ball_pos[0]) and not is_in_paddle_range(ball_pos[1], paddle1_range):
        score2 += 1
        spawn_ball(RIGHT)
    elif is_collide_right_wall(ball_pos[0]) and is_in_paddle_range(ball_pos[1], paddle2_range):
        print "hit right paddle, accelerate"
        ball_accelerate += 0.2
    elif is_collide_right_wall(ball_pos[0]) and not is_in_paddle_range(ball_pos[1], paddle2_range):
        score1 += 1
        spawn_ball(LEFT)
    
    score_color = get_score_color(score1, score2)   
    
    canvas.draw_text(str(score1), (WIDTH/2/2, 100), 100, score_color[0])
    canvas.draw_text(str(score2), ( WIDTH/4 * 2.5, 100), 100, score_color[1])
    

    
def keydown(key):
    global paddle1_vel, paddle2_vel
    global w_key_pressed, s_key_pressed, up_key_pressed, down_key_pressed    
        
    # pressed a key
    if key == simplegui.KEY_MAP["up"]:
        up_key_pressed = True
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP["down"]:
        down_key_pressed = True
        paddle2_vel = 3
    elif key == simplegui.KEY_MAP["w"]:
        w_key_pressed = True
        paddle1_vel = -3
    elif key == simplegui.KEY_MAP["s"]:
        s_key_pressed = True
        paddle1_vel = 3       
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    global w_key_pressed, s_key_pressed, up_key_pressed, down_key_pressed
    
    # release a key
    if key == simplegui.KEY_MAP["up"]:
        up_key_pressed = False
        if down_key_pressed:
            paddle2_vel = 3
        else:
            paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        down_key_pressed = False
        if up_key_pressed:
            paddle2_vel = -3
        else:
            paddle2_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        w_key_pressed = False
        if s_key_pressed == True:
            paddle1_vel = 3
        else:
            paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        s_key_pressed = False
        if w_key_pressed == True:
            paddle1_vel = -3
        else:
            paddle1_vel = 0        

def reset_button_handler():
    global score1, score2, ball_pos
    ball_vel[0] = 0
    ball_vel[1] = 0
    ball_pos = [WIDTH/2, HEIGHT/2]
    score1 = 0
    score2 = 0
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

reset_button = frame.add_button("Reset", reset_button_handler, 100)

# start frame
new_game()
frame.start()
