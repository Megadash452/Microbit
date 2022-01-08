from microbit import *


BLINK_INTERVAL = 100
TIME_SINCE_START = 0
CURRENT_PLAYER = 1 # two players, 1 and 2

P1_COL = 9
P2_COL = 4


MAP = [           # 5 x 5 grid to show on the microbit
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]


player_light_on = True # used for the blinking
player_position = 0 # ranges between 0 and 4


# Converts a two-dimensional list to a one-dimensional list
def li_2d_to_1d(li: list):
    result = []
    for i in li:
        # i is each 1d list in the 2d li
        result += i
    
    return result



def place_piece(position: int, player: int):
    if not (0 <= position <= 4):
        raise IndexError("'position' argument can only within range 0 and 4")
    if not (1 <= player <= 2):
        raise IndexError("'player' argument can only within range 1 and 2")
    
    
    # TODO: attempt to place piece at y4, but first check if there is already a piece first, 
    # then move up to y3, then check if there is a piece there, then move to y2 ....
    i = 4
    while i >= 0:
        # check if a piece is already placed there
        if MAP[i][position] == 0:
            # if there is a piece, go up one y val
            # otherwise, place the piece
            if CURRENT_PLAYER == 1:
                # if player 1 is playing, the pixel is bright
                MAP[i][position] = P1_COL
            elif CURRENT_PLAYER == 2:
                # if player 2 is playing, the pixel is dim
                MAP[i][position] = P2_COL

            # exit once a piece is placed
            break

        i -= 1



def check_horizontal_win():
    # TODO: revisit and modify
    for i in MAP:
        if [P1_COL] * 4 == i[0:4] or [P1_COL] * 4 == i[1:5]:
            display.scroll("Player 1 Wins!")
            break
        elif [P2_COL] * 4 == i[0:4] or [P2_COL] * 4 == i[1:5]:
            display.scroll("Player 2 Wins!")
            break
        
def check_vertical_win():
    width = len(MAP[0])
    height = len(MAP)

    # bufs act like a streak (so if 2 p1 pieces are found, streak is 2 so buf is 2)
    p1_buf = 0
    p2_buf = 0

    for j in range(width):
        for i in range(height):
            pixel = MAP[i][j]

            if (pixel == P1_COL):
                # increment player streak
                p1_buf += 1
                p2_buf = 0 # clear other player bufs
            elif (pixel == P2_COL):
                p1_buf = 0 # clear other player bufs
                # increment player streak
                p2_buf += 1

            # check for streak of 4 from all players
            if p1_buf >= 4:
                display.scroll("Player 1 Wins!")
                return 1
            elif p2_buf >= 4:
                display.scroll("Player 2 Wins!")
                return 2

# right down diagonal
def check_diagonal_0_win():
    dia_right = []
    for i in range(len(MAP)):
        dia_right.append(MAP[i][i])
    
    # TODO: revisit and modify
    if [P1_COL] * 4 == dia_right[0:4] or [P1_COL] * 4 == dia_right[1:5]:
        display.scroll("Player 1 Wins!")
    elif [P2_COL] * 4 == dia_right[0:4] or [P2_COL] * 4 == dia_right[1:5]:
        display.scroll("Player 2 Wins!")

# left up diagonal
def check_diagonal_1_win():
    dia_left = []
    for i in range(len(MAP)):
        dia_left.append(MAP[i][len(MAP) - 1 - i])
    
    # TODO: revisit and modify
    if [P1_COL] * 4 == dia_left[0:4] or [P1_COL] * 4 == dia_left[1:5]:
        display.scroll("Player 1 Wins!")
    elif [P2_COL] * 4 == dia_left[0:4] or [P2_COL] * 4 == dia_left[1:5]:
        display.scroll("Player 2 Wins!")

def check_win():
    check_horizontal_win()
    check_vertical_win()
    # check_diagonal_0_win()
    # check_diagonal_1_win()


    # check if the map is full (meaning theres no more spots to place pieces)
    found_0_ = False

    for i in MAP:
        for j in i:
            if j == 0:
                found_0_ = True
                break
        if found_0_:
            break

    if not found_0_:
        # STALEMATE
        display.scroll("STALEMATE")

        

# T_L_WAS_PRESSED = False
# touch_logo_up = False
# def start_touch_logo_up_event():
#     # on touch logo down set was pressed to true
#     if pin_logo.is_touched() and not T_L_WAS_PRESSED:
#         T_L_WAS_PRESSED = True
#     # when logo isnt being touched but was touched is true set the _up to true
#     elif T_L_WAS_PRESSED:
#         touch_logo_up = True


# # reset touch logo
# def end_touch_logo_up_event():
#     touch_logo_up = False
    
        

# Entry point
while True:
    # start_touch_logo_up_event()

    # toggle if the player light is on every second (for blinking)
    if TIME_SINCE_START % BLINK_INTERVAL == 0:
        player_light_on = not player_light_on



    # prepare for displaying the map
    show = li_2d_to_1d(MAP)

    # set the blinking player light on the first row (y0)
    if player_light_on and CURRENT_PLAYER == 1:
        show[player_position] = P1_COL
    elif player_light_on and CURRENT_PLAYER == 2:
        show[player_position] = P2_COL
    # turns off the pixel completely. if want transparency leave this as comment
    # else:
    #     show[player_position] = 0

    display.show(Image(5, 5, bytearray(show)))



    # Moving the player piece (it wraps)
    # if button_a.was_pressed():  # Conventional controls with touch logo
    #     if player_position <= 0:
    #         player_position = 4
    #     else:
    #         player_position -= 1
    if button_a.was_pressed(): # controls with no touch logo
        place_piece(player_position, CURRENT_PLAYER)

        # switch players
        if CURRENT_PLAYER == 1:
            CURRENT_PLAYER = 2
        elif CURRENT_PLAYER == 2:
            CURRENT_PLAYER = 1

    if button_b.was_pressed():
        if player_position >= 4:
            player_position = 0
        else:
            player_position += 1


    
    # Player confirms position, places piece, and passes it to the other player
    # if :
    #     place_piece(player_position, CURRENT_PLAYER)

    #     # switch players
    #     if CURRENT_PLAYER == 0:
    #         CURRENT_PLAYER == 1
    #     elif CURRENT_PLAYER == 1:
    #         CURRENT_PLAYER == 0


    check_win()


    # increment time at the end
    TIME_SINCE_START += 1
    # end_touch_logo_up_event()
