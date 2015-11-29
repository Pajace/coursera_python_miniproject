# template for "Stopwatch: The Game"
import simplegui

# define global variables
tensOfSecond = 0
success_times = 0
attempts_times = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    min = t / 600
    sec = (t % 600) / 10
    tenthOfSec = (t % 600 ) - sec * 10
    
    secStr = str(sec)
    if sec < 10:
        secStr = "0" + secStr
    
    return str(min) + ":" + secStr + "." + str(tenthOfSec)
    
def get_score_format():
    return str(success_times) + "/" + str(attempts_times)    

def get_tensOfSec():
    sec = ( tensOfSecond % 600 ) / 10
    return (tensOfSecond % 600) - sec * 10

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button_handler():
    timer.start()

def stop_button_hander():
    global success_times, attempts_times
    if timer.is_running():
        timer.stop()
        attempts_times += 1     
        tesOfSec = get_tensOfSec()
        if tesOfSec == 0:
            success_times += 1

def reset_button_handler():
    global tensOfSecond, success_times, attempts_times
    timer.stop()
    tensOfSecond = 0    
    success_times = 0
    attempts_times = 0
    
# define event handler for timer with 0.1 sec interval
def increase_tenth_of_second_tick():
    global tensOfSecond
    tensOfSecond += 1
    

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(tensOfSecond), [50, 90], 36, "White")
    canvas.draw_text(get_score_format(), [140, 30], 24, "Green")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 200, 150)

# register event handlers
frame.set_draw_handler(draw_handler)
frame.add_button("Start", start_button_handler, 70)
frame.add_button("Stop", stop_button_hander, 70)
frame.add_button("Reset", reset_button_handler, 70)
timer = simplegui.create_timer(100, increase_tenth_of_second_tick)

# start frame
frame.start()


# Please remember to review the grading rubric
