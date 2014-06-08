# Stopwatch: The Game

import simplegui

# Global variables
time = 0
go = False
attempts = 0
success = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    """Takes time in milliseconds and fromats it 
    in stopwatch fashion.
    """
    minutes = t / 600
    tens_of_seconds = (t / 10) % 60 / 10
    ones_of_seconds = ((t / 10) % 60) % 10
    tenths_of_seconds = (t % 10) % 10
    
    return str(minutes) + ":" + str(tens_of_seconds) + \
str(ones_of_seconds) + "." + str(tenths_of_seconds)    
    
# Event handlers for buttons; "Start", "Stop", "Reset"
def start():
    """Starts the timer."""
    global go
    go = True

def stop():
    """Stops the timer and records the number of 
    attempts. Records success if the timer is 
    stopped on a whole number."""
    global go, attempts, success
    
    digits = format(time).split('.')
    zero = int(digits[1])
    
    if zero == 0 and go:
        success += 1
    
    if go:
        attempts += 1
        go = False

def reset():
    """Stops the timer and resets it to zero."""
    global go, time, attempts, success
    go = False
    time = 0
    attempts = 0
    success = 0
    
def counters():
    return str(success) + "/" + str(attempts)

# Event handler for timer with 0.1 sec interval
def timer_handler():
    """Creates a timer updated in milliseconds."""
    global time
    if go:
        time += 1

# Draw handler
def draw(canvas):
    """Draws the timer and counters on the screen."""
    canvas.draw_text(format(time), [100, 100], 24, "White")
    canvas.draw_text(counters(), [450, 40], 17, "White")
    
# Create frame
frame = simplegui.create_frame("Stopwatch", 500, 400)
frame.set_canvas_background("#000")


# Register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw)
frame.add_button("Start", start, 200)
frame.add_button("Stop", stop, 200)
frame.add_button("Reset", reset, 200)

# Start timer and frame
timer.start()
frame.start()
