from microbit import *

amogus = [
    Image("11111:"
          "11111:"
          "11111:"
          "11111:"
          "11111"),
          
    Image("23432:"
          "44322:"
          "44442:"
          "24242:"
          "23232"),
          
    Image("35653:"
          "66433:"
          "66663:"
          "36463:"
          "25352"),
          
    Image("27872:"
          "88444:"
          "88882:"
          "28380:"
          "17271"),
    
    Image("09990:"
          "99555:"
          "99990:"
          "09990:"
          "09090"),
]

image_empty = Image("00000:"
                    "00000:"
                    "00000:"
                    "00000:"
                    "00000")

show_image = image_empty


while True:
    if button_a.was_pressed():
        display.show(amogus[::-1], delay=200)
        display.show(image_empty)
    elif button_b.was_pressed():
        display.show(amogus, delay=200)