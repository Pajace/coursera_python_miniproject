# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def get_card_index(position_x):
    return (position_x-1)/50

def get_card_face(card_index):
    return deck_of_cards[card_index]
 
def is_card_match(index1, index2):
    if get_card_face(index1) == get_card_face(index2):
        return True
    return False

def initial_global_variable():
    global exposed, deck_of_cards, card_face_up, expose_card_state, counter
    exposed = []
    deck_of_cards = []
    card_face_up = {}
    expose_card_state = 0
    counter = 0
    
def new_game():
    global exposed, deck_of_cards, card_face_up
    
    initial_global_variable()
    
    # create the cards in range [0, 8), and exposed to false
    for i in range(8):
        deck_of_cards.extend([i, i])
        exposed.extend([False, False])
        card_face_up[i] = False
    
    # shuffle cards
    random.shuffle(deck_of_cards)        

    print "After shuffle:", deck_of_cards
    
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed_index1, exposed_index2, expose_card_state, counter
    
    card_index = get_card_index(pos[0])
        
    # guard, if card was exposed, ignored it
    if exposed[card_index] == True:
        return
    
    exposed[card_index] = True   
    
    if expose_card_state == 0:
        exposed_index1 = card_index
        expose_card_state = 1
        counter += 1
        print "1 => set exposed_index1 to ", card_index
    elif expose_card_state == 1:
        exposed_index2 = card_index
        expose_card_state = 2
        print "2 => set exposed_index2 to ", card_index
    else:
        expose_card_state = 1
        
        if is_card_match(exposed_index1, exposed_index2):
            card_face_up[get_card_face(exposed_index1)] = True
            print "3A => two card's fase is equal."
        else:
            exposed[exposed_index1] = False
            exposed[exposed_index2] = False
            print "3B => two card's fase is not equal."                                   
        
        counter += 1
        exposed_index1 = card_index
       
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    card_width = 50    
        
    # draw thee Memory deck
    text_pos_x = 7 # text initial x position
    card_pos_x = 25 # card cover initial x position
    card_index = 0
    for card in deck_of_cards:
        if exposed[card_index] == True:
            canvas.draw_text(str(card), [text_pos_x, 75], 64, "White")            
        else:
            # draw card's cover    
            canvas.draw_line([card_pos_x-25,0], [card_pos_x-25, 100], 1, "Red")
            canvas.draw_line([card_pos_x+1, 0], [card_pos_x+1, 100], card_width-1, "Green")                    
        text_pos_x += 50
        card_pos_x += 50
        card_index += 1

    label.set_text("Turns = " + str(counter))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# -------------------------------------------------------------
# test cards expose

exposedIndex = 0
def timer_handler_test_expose():
    global exposed, exposedIndex
    exposed[exposedIndex] = True
    exposed[exposedIndex-1] = False
    exposedIndex = (exposedIndex + 1) % 16

#timer = simplegui.create_timer(500, timer_handler_test_expose)
#timer.start()


# Always remember to review the grading rubric