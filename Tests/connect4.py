from microbit import *


BLINK_INTERVAL = 30
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


def switch_player():
    global CURRENT_PLAYER

    if CURRENT_PLAYER == 1:
        CURRENT_PLAYER = 2
    elif CURRENT_PLAYER == 2:
        CURRENT_PLAYER = 1


def move(direction: str):
    global player_position

    if direction == "right":
        if player_position >= 4:
            player_position = 0
        else:
            player_position += 1

    elif direction == "left":
        if player_position <= 0:
            player_position = 4
        else:
            player_position -= 1


def place_piece(position: int, player: int):
    if not (0 <= position <= 4):
        raise IndexError("'position' argument can only within range 0 and 4")
    if not (1 <= player <= 2):
        raise IndexError("'player' argument can only within range 1 and 2")
    
    
    # attempt to place piece at y4, but first check if there is already a piece first, 
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

            # once a piece is placed switch the players
            switch_player()

            # exit once a piece is placed
            break

        i -= 1



def check_horizontal_win():
    # TODO: revisit and modify
    # Uses indexing and slicing to tell if there are 4 consecutive 9s or 4s LED lvl and then displays
    # either P1 or P2 win message
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

#Diagonals win check
#Credits to https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python discussion for the help and understanding of implementing diagonals in lists
def check_diagonal_win():
    #Width and height dimension of the map
    width = len(MAP[0])
    length = len(MAP)
    #Creates a certain number of list based on how many diagonals can be formed for the 2d list (for this 5 by 5 map, we only need 9 lists; be it for left or right diagonals)
    leftup_diag = [[] for i in range(width + length - 1)] 
    rightdn_diag = [[] for i in range(width + length - 1)] 
    
    for col in range(width): 
      for row in range(length):
        #Index at certain lists from the leftup_diag and 
        #appends the certain diagonal value to that list
        #Ex: at Index 0, append the leftup_diag[0] list with the value MAP[0][0], then go to index 1 and append it with the value MAP[1][0] and so on so forth
        leftup_diag[col+row].append(MAP[row][col])
        #Index at certain lists from the rightdn_diag and 
        #appends the certain diagonal value to that list
        #Ex: at Index 0, append the rightdn_diag[0] list with the value MAP[4][0], then go to index 1 and append it with the value from MAP[3][0]
        rightdn_diag[col+row].append(MAP[length - row - 1][col])
    
    #Checks if there are 4 consecutive player colors from left diagonals
    for left_dia in leftup_diag:
      if [P1_COL] * 4 == left_dia[0:4] or [P1_COL] * 4 == left_dia[1:5]:
        display.scroll("Player 1 Wins!")
      elif [P2_COL] * 4 == left_dia[0:4] or [P2_COL] * 4 == left_dia[1:5]:
        display.scroll("Player 2 Wins!")
    
    #Checks if there are 4 consecutive player colors from right diagonals
    for right_dia in rightdn_diag:
      if [P1_COL] * 4 == right_dia[0:4] or [P1_COL] * 4 == right_dia[1:5]:
        display.scroll("Player 1 Wins!")
      elif [P2_COL] * 4 == right_dia[0:4] or [P2_COL] * 4 == right_dia[1:5]:
        display.scroll("Player 2 Wins!")


def check_win():
    check_horizontal_win()
    check_vertical_win()
    check_diagonal_win()

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

        

TL_was_pressed = False
def touch_logo_was_pressed():
    if TL_was_pressed:
        TL_was_pressed = False
        return True
    return False
    
        

# Entry point
while True:
    # start_touch_logo_up_event()
    # TODO: et TL_was_pressed to true when touched

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


    # Player confirms position, places piece, and passes it to the other player
    # if touch_logo_was_pressed():
    #     place_piece(player_position, CURRENT_PLAYER)

    # Moving the player piece (it wraps)
    # if button_a.was_pressed():  # Conventional controls with touch logo
    #     move("left")
    if button_a.was_pressed(): # controls with no touch logo
        place_piece(player_position, CURRENT_PLAYER)
    if button_b.was_pressed():
        move("right")


    check_win()


    # increment time at the end
    TIME_SINCE_START += 1
    # end_touch_logo_up_event()
