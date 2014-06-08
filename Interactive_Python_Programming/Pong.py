# Implementation of classic arcade game Pong

import simplegui
import random

# Initialize globals - pos and vel encode vertical info for paddles
width = 600
height = 400
ball_radius = 20
pad_width = 8
pad_height = 80
half_pad_width = pad_width / 2
half_pad_height = pad_height / 2
left = False
right = True
ball_pos = [width / 2, height / 2]
ball_vel = [0, 1] 

paddle1_pos = 50.0
paddle2_pos = 140.0
paddle1_vel = 0.0
paddle2_vel = 0.0
paddle_speed = 10

score1 = 0
score2 = 0


# Initialize ball_pos and ball_vel for new bal in middle of table
# if direction is right, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    # Ball position and velocity 
    ball_pos = [width / 2, height / 2]
    
    # Create a random velocity and direction for the ball.
    # Divide by 60 because the screen refresh rate is 60 times per second 
    if left:
        ball_vel = [-random.randrange(120, 240) / 60, -random.randrange(60, 180) / 60]        
    elif right:
        ball_vel = [random.randrange(120, 240) / 60, -random.randrange(60, 180) / 60] 
   
# Start a new game
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball(left)

# Draw on the canvas 
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, left


    # Draw mid line and gutters
    canvas.draw_line([width / 2, 0],[width / 2, height], 1, "White")
    canvas.draw_line([pad_width, 0],[pad_width, height], 1, "White")
    canvas.draw_line([width - pad_width, 0],[width - pad_width, height], 1, "White")

    # Update ball (x/y cooridinates)
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Detect if the ball touches a paddle and deflect it
    paddle1_top = paddle1_pos - ball_radius
    paddle1_bottom = paddle1_top + pad_height + ball_radius 
    paddle2_top = paddle2_pos - ball_radius
    paddle2_bottom = paddle2_top + pad_height + ball_radius

    if (ball_pos[0] - ball_radius <= pad_width) and (ball_pos[1] >= paddle1_top) and (ball_pos[1] <= paddle1_bottom):
            ball_vel[0] = (ball_vel[0] * 1.18) * -1
            ball_vel[1] = (ball_vel[1] * 1.18) 
        
    elif (ball_pos[0] + ball_radius >= width - pad_width) and (ball_pos[1] >= paddle2_top) and (ball_pos[1] <= paddle2_bottom): 
            ball_vel[0] = (ball_vel[0] * 1.18) * -1
            ball_vel[1] = (ball_vel[1] * 1.18) 
        
    # Detect if the ball touches the gutters (a point is scored) 
    elif ball_pos[0] - ball_radius <= pad_width:
        left = False
        score2 += 1
        spawn_ball(right)
    elif ball_pos[0] + ball_radius >= width - pad_width:
        left = True
        score1 += 1
        spawn_ball(left)
    
    # Make the ball bounce and reflect off of walls
    if ball_pos[1] >= height - ball_radius:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] <= 0 + ball_radius:
        ball_vel[1] = -ball_vel[1]

    # Draw ball
    canvas.draw_circle(ball_pos, ball_radius, 2, "White", "White")
    
    # Draw paddle 1
    canvas.draw_line([pad_width / 2, paddle1_pos], [pad_width / 2, paddle1_pos + pad_height], pad_width, 'White')
    
    # Draw paddle 2
    canvas.draw_line([width - pad_width / 2, paddle2_pos], [width - pad_width / 2, paddle2_pos + pad_height], pad_width, 'White')

    # Update paddle's vertical position, keep paddle on the screen
    if paddle1_pos <= 0.0:
        paddle1_pos = paddle1_vel
    elif paddle1_pos > height - pad_height:
        paddle1_pos = height - pad_height
    else:
        paddle1_pos += paddle1_vel
        
    if paddle2_pos <= 0.0:
        paddle2_pos = paddle2_vel
    elif paddle2_pos > height - pad_height:
        paddle2_pos = height - pad_height
    else:
        paddle2_pos += paddle2_vel

    # Draw scores
    canvas.draw_text(str(score1), (width * 0.25 - 20, 60), 50, 'White')
    canvas.draw_text(str(score2), (width - (width * 0.25) - 20, 60), 50, 'White')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    # Control movement of paddle 1
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += paddle_speed
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= paddle_speed
        
    # Control movement of paddle 2
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += paddle_speed
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= paddle_speed
    
def keyup(key):
    global paddle1_vel, paddle2_vel
   
    #Stop movement of paddle 1
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= paddle_speed
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel += paddle_speed
        
    #Stop movement of paddle 2
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= paddle_speed
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel += paddle_speed


# create frame
frame = simplegui.create_frame("Pong", width, height)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
reset = frame.add_button('New Game', new_game, 150)


# start frame
new_game()
frame.start()
