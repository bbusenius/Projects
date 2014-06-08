# Program template for Spaceship
import simplegui
import math
import random

# Globals for the user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
MARGIN_SIDE = 30
MARGIN_TOP = 30
FONT_SIZE = 18
FONT_COLOR = 'White'
FONT_TYPE = 'sans-serif'
FONT_SPACING = 20
started = False
browser_info = "This game works best with Chrome and other webkit browsers."
instructions = "Use <- and -> arrow keys to navigate. Use the up arrow key to fire thrusters. Use the spacebar to fire missiles."

# Global constants for environment, behavior, sprites, and ship 
SHIP_ROTATION_SPEED = 0.15
SHIP_ACCELERATION_SPEED = 0.2
FRICTION = 0.020
MISSILE_SPEED = 8
NUMBER_OF_ASTEROIDS = 12
SAFE_RANGE = 150
difficulty = 1
asteroid_speed = 3
indestructible_time = 5
reset_timer = list([indestructible_time])

# Class for managing information about image objects
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        """Returns the center point of the image."""
        return self.center

    def get_size(self):
        """Returns the width and height of the image in pixels."""
        return self.size

    def get_radius(self):
        """Returns the image radius."""
        return self.radius

    def get_lifespan(self):
        """Returns the lifespan or image duration."""
        return self.lifespan

    def get_animated(self):
        """Returns a boolean. Is the image animated?"""
        return self.animated

    
# Art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# Debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# Nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# Splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# Ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
ship_invincible_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/2117288/Python-Projects/Asteroids/double_ship_invincible.png")
blank_image = simplegui.load_image("https://dl.dropboxusercontent.com/nothing.png")

# Missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# Asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# Alternate asteroid images. Share asteroid_info.
asteroid_blue_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
asteroid_brown_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")
asteroid_blend_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# Animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# Different explosion for the ship
explosion_ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# Sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# Helper functions to handle transformations
def reset_game():
    """Method starts a new game and reiniciates variables if the 
    player doesn't have anymore lives. Otherwise, the player loses 
    a life and is sent to the middle of the screen."""
    global started, score, lives, rock_group, indestructible
    if lives == 0:
        started = False
        my_ship.pos = [WIDTH / 2, HEIGHT / 2]
        my_ship.vel = [0, 0]
        rock_group = set([])
    else:
        my_ship.pos = [WIDTH / 2, HEIGHT / 2]
        my_ship.vel = [0, 0]
        my_ship.invincible = True
        new_life_timer.start()
        
def reset_score():
    """Resets the games score and lives to their beginning values."""
    global score, lives
    score = 0
    lives = 3
    soundtrack.rewind()
    soundtrack.play()

def angle_to_vector(ang):
    """Returns the angle transformed as a forward vector."""
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    """Calculate the distance between two points."""
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(group, canvas):
    """Draws and updates asteroid rock sprites in the draw handler.
    Processes a set of sprites.
    """
    # Iterate over a copy of the set, not the original
    group_copy = group.copy()
    
    # See if a sprite's life is over, update and draw the sprite
    for sprite in group_copy:
        alive = sprite.update()
        if alive == False:
            group.remove(sprite)            
        sprite.draw(canvas)
        sprite.update()

def group_collide(group, other_object):
    """Method checks for collisions between members of the set 
    and other objects.
    """
    collision = False
    
    # Iterate over a copy of the set, not the original
    group_copy = group.copy()
    for member in group_copy:
        if member.collide(other_object):
            collision = True
            group.remove(member)
            
            # Add an explosion for the asteroid to the explosion group
            explosion_group.add(Sprite(member.get_position(), 
                                       member.get_velocity(), 
                                       member.get_angle(), 
                                       member.get_angle_vel(), 
                                       explosion_image, explosion_info, explosion_sound))
         
            # Add an explosion for the ship to the explosion group
            if isinstance(other_object, Ship):
                explosion_group.add(Sprite(other_object.pos, 
                                           other_object.vel, 
                                           other_object.angle, 
                                           other_object.angle_vel, 
                                           explosion_ship_image, explosion_info, explosion_sound))                        
    return collision

def group_group_collide(group1, group2):
    """Method checks if objects in different sets collide with eachother. 
    Use this to see if missiles collide with asteroids. Remove asteroids 
    and missiles upon collision. Return a count of collisions between 
    missiles and asteroids.
    """
    collision_count = 0
    group1_copy = group1.copy()
    for instance in group1_copy:
        collision = group_collide(group2, instance)
        if collision == True:
            group1.discard(instance)
            group2.discard(instance)
            collision_count += 1
    return collision_count
    
def is_indestructible(): 
    """Method checks to see if a player is indestructible after losing a life.
    Returns a boolean.
    """
    global indestructible_time, reset_timer
    
    if indestructible_time > 0 and my_ship.invincible:
        indestructible_time -= 0.001 * 24 
    else:
        indestructible_time = reset_timer[0]
        my_ship.invincible = False
        new_life_timer.stop()
    return my_ship.invincible
        
    
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.invincible = False
        self.blink_flag = False
        
    def get_position(self):
        """Get ship position."""
        return self.pos
    
    def get_radius(self):
        """Get ship radius."""
        return self.radius
        
    def draw(self,canvas):
        """Draws the spaceship on the canvas."""
        # If the player has lost a life the ship is invincible after it spawns. Draw a faded transparent ship.
        if self.invincible:
            blink_timer.start()
        else:
            self.image = ship_image
             
        canvas.draw_image(self.image, ship_info.center, ship_info.size, self.pos, (ship_info.size[0], ship_info.size[1]), self.angle)
        
        # Show engine fire when the thrusters are on
        if self.thrust:
            self.image_center[0] = self.image_size[0] + (self.image_size[0] / 2)
        else:
            self.image_center[0] = self.image_size[0] - (self.image_size[0] / 2)
        
    def update(self):
        """Updates the spaceship object in the draw handler 
        every microsecond that the draw handler redraws the screen.
        """
        # Change the rotation
        self.angle += self.angle_vel
        
        # Change positon based on velocity 
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # Slow the ship down with friction
        self.vel[0] *= (1 - FRICTION)
        self.vel[1] *= (1 - FRICTION)
        
        # Detect forward thrust (up arrow is presed)
        forward = angle_to_vector(self.angle)        
        if self.thrust:
            self.vel[0] += forward[0] * SHIP_ACCELERATION_SPEED
            self.vel[1] += forward[1] * SHIP_ACCELERATION_SPEED
            
        # Make the ship redraw on the opposite side of the screen
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
              
    def change_angular_velocity(self, change):
        """Change the rotation of the ship.
        Args:            
            increment: string, right key is pressed, rotate clockwise.                
            decrement: string left key is pressed, rotate counter-clockwise.
        """
        if change == "increment":
            self.angle_vel += SHIP_ROTATION_SPEED 
        elif change == "decrement":
            self.angle_vel -= SHIP_ROTATION_SPEED 
            
    def get_thrusters(self, status):
        """Manipulate the behavior based on the 
        status of the thrusters.
        """
        if status == "on":
            self.thrust = True
            ship_thrust_sound.set_volume(0.5)
            ship_thrust_sound.play()
        elif status == "off":
            self.thrust = False
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
            
    def get_forward_postion(self, index_list, n):
        """Applys the math needed to find the x/y 
        coordinates of the tip of the ship.
        """          
        forward_vector = angle_to_vector(self.angle)
        return [self.pos[index] + forward_vector[index] * n for index in index_list]
            
    def shoot(self):
        """Method for shooting missiles. Is responsiblie for the 
        launch point, velocity, and general behavior of missiles.
        """
        global missile_group
        forward_vector = angle_to_vector(self.angle)
        
        # Create a missle instance
        missile_group.add(Sprite(self.get_forward_postion([0, 1], self.radius), 
                           [self.vel[i] + MISSILE_SPEED * forward_vector[i] for i in [0, 1]], 
                           0, 0, missile_image, missile_info, missile_sound))
    
    def blink(self):
        """Make the ship blink while it respawns."""
        if self.blink_flag == False:
            self.blink_flag = True
            self.image = blank_image
        elif self.blink_flag == True:
            self.blink_flag = False
            self.image = ship_invincible_image

# Sprite class for meteors and missiles.
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.invincible = False
        
        if sound:
            sound.rewind()
            sound.play()
   
    def get_position(self):
        """Get sprite position."""
        return self.pos
    
    def get_velocity(self):
        """Get sprite velocity."""
        return self.vel
    
    def get_radius(self):
        """Get sprite radius."""
        return self.radius
    
    def get_angle(self):
        """Get sprite angle."""
        return self.angle
    
    def get_angle_vel(self):
        """Get sprite angular velocity."""
        return self.angle_vel
    
    def draw(self, canvas):
        """Draws asteroids and missiles on the canvas."""
        if self.animated == True:
            # Make an explosion
            self.image_center = [self.image_center[0] * self.age, self.image_center[1]]
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                              self.pos, self.image_size, self.angle)
        else:
            # No explosion
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
    
    def update(self):
        """Updates the meteor and missile objects in the draw handler 
        every microsecond that the draw handler redraws the screen. 
        """
        
        # Make rock sprites rotate and move
        self.angle += self.angle_vel
        
        # Make the rocks redraw on the opposite side of the screen
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # Update the age of the sprite, remove it if it is too old
        self.age += 1
        if self.age >= self.lifespan:
            remove_sprite = False
        else:
            remove_sprite = True
        return remove_sprite
        
    def collide(self, other_object):
        """Method detects if the sprite collides with another object.
        If there is a collision, return True.
        """
        other_object_pos = other_object.get_position()
        distance = dist(self.pos, other_object_pos)
        
        if not other_object.invincible:
            return distance < self.radius + other_object.get_radius()
        
def draw(canvas):
    """Draw handler for the game."""
    global time, lives, score, started, rock_group
    
    # Start the intro music
    soundtrack.play()
    
    # Animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # Draw lives and score strings
    canvas.draw_text("Lives", (MARGIN_SIDE, MARGIN_TOP), FONT_SIZE, FONT_COLOR, FONT_TYPE)
    canvas.draw_text(str(lives), (MARGIN_SIDE, MARGIN_TOP + FONT_SPACING), FONT_SIZE, FONT_COLOR, FONT_TYPE)
    canvas.draw_text("Score", (WIDTH - MARGIN_SIDE - frame.get_canvas_textwidth("Score", FONT_SIZE, FONT_TYPE), MARGIN_TOP), FONT_SIZE, FONT_COLOR, FONT_TYPE)
    canvas.draw_text(str(score), (WIDTH - MARGIN_SIDE - frame.get_canvas_textwidth("Score", FONT_SIZE, FONT_TYPE), MARGIN_TOP + FONT_SPACING), FONT_SIZE, FONT_COLOR, FONT_TYPE)

    # Draw ship sprite
    my_ship.draw(canvas)
    
    #Draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
    # Update ship sprite
    my_ship.update()
    
    # Update and draw asteroid sprite sets
    process_sprite_group(rock_group, canvas)
    
    # Update and draw missile sets
    process_sprite_group(missile_group, canvas)
    
    # Update and draw explosion sets
    process_sprite_group(explosion_group, canvas)
    
    # Check for collisions between the ship and asteroids. Update lives accordingly.
    collision = group_collide(rock_group, my_ship)
    
    invincible = is_indestructible()
    if collision and invincible == False:
        my_ship.image = ship_invincible_image
        lives -= 1
        #See if a new game should be started. If yes, start a new game
        reset_game()
        
    # Check for collisions between missiles and asteroids.
    point = group_group_collide(missile_group, rock_group)
    if point:
        score += 1
               
def rock_spawner():
    """Timer handler that spawns a rock every second.
    The method is called by a timer."""
    
    # General code for randomizing
    lower = -asteroid_speed
    upper = asteroid_speed
    
    # Set random velocity. Velocity increases with score.
    randomizor = (random.randrange(lower, upper) + random.random()) * (score * difficulty / 10.0) + 0.18
    
    # Set random position, velocity, angle, and angular velocity for the rocks
    rock_pos = (random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
    rock_vel = (randomizor, randomizor)
    rock_ang = random.randrange(0, 360)
    rock_ang_vel = random.choice([-1, 1]) * (random.random() * 0.2 - 0.1) 
    
    distance_from_ship = dist(rock_pos, my_ship.get_position())
    
    # Vary asteroid images
    random_asteroid = random.choice([asteroid_blue_image, asteroid_brown_image, asteroid_blend_image])
    
    # Create a set of asteroid instances but limit them to a specified number
    if len(rock_group) < NUMBER_OF_ASTEROIDS and started == True and distance_from_ship >= SAFE_RANGE:
        rock_group.add(Sprite(rock_pos, rock_vel, rock_ang, rock_ang_vel, random_asteroid, asteroid_info))
        
def key_map(inputs, key):
    """Helper method for keydown and keyup handlers.
    Maps key presses to functions to avoid long conditionals.
    """
    for i in inputs:                    
        if key == simplegui.KEY_MAP[i]:
            if inputs[i][1] == None:
                inputs[i][0]()
            else:
                inputs[i][0](inputs[i][1])

def keydown(key):
    """Key handler for button down interactions."""
    actions = {"up": [my_ship.get_thrusters, "on"],
          "left": [my_ship.change_angular_velocity, "decrement"],
          "right": [my_ship.change_angular_velocity, "increment"],
          "space": [my_ship.shoot, None]}
    
    key_map(actions, key)
        
def keyup(key):
    """Key handler for button up interactions."""
    actions = {"up": [my_ship.get_thrusters, "off"],
          "left": [my_ship.change_angular_velocity, "increment"],
          "right": [my_ship.change_angular_velocity, "decrement"]}

    key_map(actions, key)
        
def click(pos):
    """Mouseclick handlers that reset UI and conditions whether splash image is drawn"""
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        reset_score()
        started = True
    
# Initialize the frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# Initialize a ship and two sprite sets
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# Register event handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
frame.add_label(browser_info)
frame.add_label("")
frame.add_label(instructions)

# Timer spawns a new meteor every second
timer = simplegui.create_timer(1000.0, rock_spawner)
# Timer makes ship blink while invincible
blink_timer = simplegui.create_timer(300.0, my_ship.blink)
# Timer while invincible
new_life_timer = simplegui.create_timer(1000.0, is_indestructible)

# Get things rolling
timer.start()
frame.start()