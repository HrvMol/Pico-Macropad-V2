'''
This version of the project utilises adafruit_imageload to improve the speed of displaying images by loading images to memory. 
It is important to have a microcontroller that has enough memory to store all the images in memory at the same time. 
For 16 bit RGB565, that is 115,794 bits for all 9 images. using 8 bit, it is substantially lower at 67,302 bits for all 9. 
Unless you have a powerful microcontroller, I recommend you use 8 bit for faster load times. 
'''

import board
import busio
import displayio
import digitalio
import adafruit_ili9341
import json
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import adafruit_imageload
import gc
import microcontroller

#YOU CAN USE THIS TO OVERCLOCK YOUR DEVICE IF IT LOADS IMAGES SLOWLY
#microcontroller.cpu.frequency = 250000000

# EDIT THESE TO FIT YOUR DEVICE
# setting pins for the display
DIN = board.GP3
CLK = board.GP2
CS = board.GP0
DC = board.GP1
RST = board.GP4

# display dimensions
WIDTH = 240
HEIGHT = 320



#setting keyboard as a usb device
keyboard = Keyboard(usb_hid.devices)

# Read data from json file
f = open('pages.json')
data = json.load(f)
pages = data['pages']
f.close()

# Setting up display
displayio.release_displays()
screen = displayio.Group()

# configure the display
spi = busio.SPI(clock=CLK, MOSI=DIN)
display_bus = displayio.FourWire(spi, command = DC, chip_select=CS, reset=RST)
display = adafruit_ili9341.ILI9341(display_bus, width=WIDTH, height=HEIGHT, rotation=90, auto_refresh=False)
    
# set up buttons
def btn_settings(btn_pin):
    btn = digitalio.DigitalInOut(btn_pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    return btn

# SET THE PINS BASED OFF YOUR BOARD
btn1 = btn_settings(board.GP22)
btn2 = btn_settings(board.GP26)
btn3 = btn_settings(board.GP27)
btn4 = btn_settings(board.GP19)
btn5 = btn_settings(board.GP20)
btn6 = btn_settings(board.GP21)
btn7 = btn_settings(board.GP16)
btn8 = btn_settings(board.GP17)
btn9 = btn_settings(board.GP18)

# button last value for debouncing
btn1_last = btn2_last = btn3_last = btn4_last = btn5_last = btn6_last = btn7_last = btn8_last = btn9_last = True

# Execute the macro
def handle_macro(button):
    macro = button['macro']
    try: delay = button['delay']
    except: delay = 0.01
    
    for i in range(len(macro)):
        # handle combined bindings
        # check if list
        if isinstance(macro[i], list):
            # press each button and then release each button
            for j in range(len(macro[i])):
                keyboard.press(getattr(Keycode, macro[i][j]))
            time.sleep(delay)
            for j in range(len(macro[i])):
                keyboard.release(getattr(Keycode, macro[i][j]))

        # handle held bindings such as holding shift and typing
        # check if the macro command contains a dot
        elif '.' in macro[i]:
            # split command and check if the last part is for pressing or releasing the key
            splitMacro = macro[i].split('.')
            if splitMacro[1] == 'down':
                print('down')
                keyboard.press(getattr(Keycode, splitMacro[0]))
            elif splitMacro[1] == 'up':
                print('up')
                keyboard.release(getattr(Keycode, splitMacro[0]))

        # handle standard, single key bindings 
        else:
            # press then release key
            keyboard.press(getattr(Keycode, macro[i]))
            time.sleep(delay)
            keyboard.release(getattr(Keycode, macro[i]))
            time.sleep(delay) 
            
# Refresh display with new images
def display_out(newPage):
    #start = time.monotonic()
    
    global screen
    i=1
    popCount = 0

    # iterate throught all 9 image slots
    while i <= 9:
        gc.collect()
        try:
            # if index is not to be set, try to remove any existing image in the place
            if not str(i) in newPage:
                try:
                    # remove images from indexes that arent used.
                    # as popping shortens the length, popCount accomodates for it in future pop operations
                    screen.pop(i - popCount)
                    popCount+=1
                except: pass
                i+=1
                continue
            
            # load image to memory and set as a tile grid
            i = load_image(str(newPage[f'{i}']['image']), i)
        
        # errors relating to either no image or a incorrect reference
        # set image to the default no image image
        except (OSError, KeyError):            
            i = load_image('/images/no-image.bmp', i)
            
    # update display
    display.root_group = screen
    display.refresh()

    # USE THIS TO CHECK FREE MEMORY AND MEASURE TIME TAKEN FOR SCREEN UPDATES
    #print('memory free:', gc.mem_free())
    #print('memory allocated:', gc.mem_alloc())
    #print(microcontroller.cpu.frequency)
    #print(microcontroller.cpu.temperature)
    #end = time.monotonic()
    #print('time taken:', end - start)
    return(newPage)

# load images and add to screen
def load_image(link, i):
    global screen
    
    # setting x and y coordinates for each image
    x = 80 * ((i-1) % 3)
    y = 80 + 80 * ((i-1) // 3)
    
    # use faster memory loading and then when memory runs out, use disk loading
    try:
        bitmapImage, palette = adafruit_imageload.load(link, bitmap=displayio.Bitmap, palette=displayio.Palette)
        image = displayio.TileGrid(bitmapImage, pixel_shader=palette, x=x, y=y)
    except MemoryError:
        print('memory error')
        bitmapImage = displayio.OnDiskBitmap(link)
        image = displayio.TileGrid(bitmapImage, pixel_shader=bitmapImage.pixel_shader, x=x, y=y)
    
    try: screen[i] = image
    except: screen.append(image)
    
    i+=1
    
    return i
    
# Change page or call macro function
def handle_buttons(button, current_page, pages):
    try:
        current_page = display_out(pages[current_page[button]['page']])
    except KeyError as e:
        # if the page doesnt exist throw error
        if str(e) == 'page':
            handle_macro(current_page[button])
        pass
    return current_page

# set the page to home on start up
current_page = display_out(pages['Home'])
        
# run program indefinitely
while True:
    # handle button presses
    if not btn1.value and btn1.value != btn1_last:
        current_page = handle_buttons('1', current_page, pages)

    if not btn2.value and btn2.value != btn2_last:
        current_page = handle_buttons('2', current_page, pages)

    if not btn3.value and btn3.value != btn3_last:
        current_page = handle_buttons('3', current_page, pages)

    if not btn4.value and btn4.value != btn4_last:
        current_page = handle_buttons('4', current_page, pages)

    if not btn5.value and btn5.value != btn5_last:
        current_page = handle_buttons('5', current_page, pages)

    if not btn6.value and btn6.value != btn6_last:
        current_page = handle_buttons('6', current_page, pages)

    if not btn7.value and btn7.value != btn7_last:
        current_page = handle_buttons('7', current_page, pages)

    if not btn8.value and btn8.value != btn8_last:
        current_page = handle_buttons('8', current_page, pages)
        
    if not btn9.value and btn9.value != btn9_last:
        current_page = handle_buttons('9', current_page, pages)
    
    # Debouncing the buttons
    btn1_last = btn1.value
    btn2_last = btn2.value
    btn3_last = btn3.value
    btn4_last = btn4.value
    btn5_last = btn5.value
    btn6_last = btn6.value
    btn7_last = btn7.value
    btn8_last = btn8.value
    btn9_last = btn9.value
    time.sleep(0.01)