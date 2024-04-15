# This version of the project utilises displayio.OnDiskBitmap() to load images directly from the storage, minimising memory usage. This is good for microcontrollers with minimal memory.

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

#setting keyboard as a usb device
keyboard = Keyboard(usb_hid.devices)

# Read data from json file
f = open('pages.json')
data = json.load(f)
pages = data['pages']
f.close()

# setting pages
#previous_page = current_page = pages['Home']
#print(current_page)

# Setting up display
displayio.release_displays()

DIN = board.GP3
CLK = board.GP2
CS = board.GP0
DC = board.GP1
RST = board.GP4

WIDTH = 240
HEIGHT = 320

spi = busio.SPI(clock=CLK, MOSI=DIN)
display_bus = displayio.FourWire(spi, command = DC, chip_select=CS, reset=RST)

display = adafruit_ili9341.ILI9341(display_bus, width=WIDTH, height=HEIGHT, rotation=90)

# Create a bitmap with two colors
#bitmap = displayio.Bitmap(display.width, display.height, 2)

# Create a two color palette
#palette = displayio.Palette(2)
#palette[0] = 0x000000
#palette[1] = 0xffffff

# Create a TileGrid using the Bitmap and Palette
#grid_overlay = displayio.TileGrid(bitmap, pixel_shader=palette)

#bitmapImage, palette = adafruit_imageload.load("/images/helldivers.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
#tile_grid1 = displayio.TileGrid(bitmapImage, pixel_shader=palette, y=80)

#NOT WORKING
#def set_images(page):
#    coordinates = [(0, 81), (81, 81)]
#    tile_grid = []
#    for i in range(len(page)):
#        print('started')
#        #bitmapImage = displayio.OnDiskBitmap(str(page[f'{i}']['image']))
#        bitmapImage = displayio.OnDiskBitmap('/images/helldivers.bmp')
#        tile_grid.append(displayio.TileGrid(bitmapImage, pixel_shader=bitmapImage.pixel_shader, x=coordinates[i][0], y=coordinates[i][1]))
#    return tile_grid
        
#print(current_page['1']['image'])
#tile_grid = set_images(current_page)

# Create a Group
#group = displayio.Group()

#NOT WORKING
#for i in range(len(tile_grid)):
#    print(dir(tile_grid[i]))
#    group.append(tile_grid[i])

# Add the TileGrid to the Group
#TODO: WORK OUT HOW TO MAKE OVERLAY SHOW OVERTOP WITHOUT COVERING OTHER LAYERS
#group.append(grid_overlay)
#group.append(tile_grid1)

# Add the Group to the Display
#display.root_group = group

# Draw overlay grid    
#for x in range(78, 81):
#    for y in range(80, HEIGHT):
#        bitmap[x, y] = 1

#for x in range(159, 162):
#    for y in range(80, HEIGHT):
#        bitmap[x, y] = 1


#for x in range(0, WIDTH):
#    for y in range(77, 80):
#        bitmap[x, y] = 1

#for x in range(0, WIDTH):
#    for y in range(158, 161):
#        bitmap[x, y] = 1

#for x in range(0, WIDTH):
#    for y in range(239, 242):
#        bitmap[x, y] = 1
        
def btn_settings(btn_pin):
    btn = digitalio.DigitalInOut(btn_pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    return btn

btn1 = btn_settings(board.GP22)
btn2 = btn_settings(board.GP26)
btn3 = btn_settings(board.GP27)
btn4 = btn_settings(board.GP19)
btn5 = btn_settings(board.GP20)
btn6 = btn_settings(board.GP21)
btn7 = btn_settings(board.GP16)
btn8 = btn_settings(board.GP17)
btn9 = btn_settings(board.GP18)


btn1_last = btn2_last = btn3_last = btn4_last = btn5_last = btn6_last = btn7_last = btn8_last = btn9_last = True

runningMacros = []

# Execute the macro
def handle_macro(button, runningMacros):
    macro = button['macro']
    try: delay = button['delay']
    except: delay = 0.01
    
    print(macro)
    print(delay)
    
#    try:
#        type = button['type']
#        print(type)
#        
#        if type == 'toggle':
#            print('toggle')
#            if macro in runningMacros:
#                print(runningMacros)
#                #runningMacros.remove(button)
#                print('removed')
#            else:
#                print(runningMacros)
#                ruinningMacros.extend(button)
#                print('added')
#                print(runningMacros)
#            
#        else:
#            print('not toggle')
#        
#        return runningMacros
#    except Exception as e:
#        print(e)
    for i in range(len(macro)):
        #print(macro[i])
            
        if isinstance(macro[i], list):
            # print('concurrent')
            for j in range(len(macro[i])):
                keyboard.press(getattr(Keycode, macro[i][j]))
            time.sleep(delay)
            for j in range(len(macro[i])):
                keyboard.release(getattr(Keycode, macro[i][j]))
                time.sleep(delay)

            # keyboard.press(getattr(Keycode, macro[i][0]), getattr(Keycode, macro[i][1]))
            # time.sleep(delay)
            # keyboard.release(getattr(Keycode, macro[i][0]), getattr(Keycode, macro[i][1]))

        elif '.' in macro[i]:
            #print('partial')
            splitMacro = macro[i].split('.')
            if splitMacro[1] == 'down':
                print('down')
                keyboard.press(getattr(Keycode, splitMacro[0]))
            elif splitMacro[1] == 'up':
                print('up')
                keyboard.release(getattr(Keycode, splitMacro[0]))
                    
        else:
            # print('continuous')
            keyboard.press(getattr(Keycode, macro[i]))
            time.sleep(delay)
            keyboard.release(getattr(Keycode, macro[i]))
            time.sleep(delay)
            
# Refresh display with new images
def display_out(newPage):
    screen = displayio.Group()
    #print(newPage)
    loopcount = len(newPage)
    i=0
    while i < loopcount:
        try:
            if not str(i+1) in newPage:
                loopcount+=1
                i+=1
            
            print(i)
            x = 80 * (i % 3)
            y = 80 + 80 * (i // 3)
            
            bitmapImage = displayio.OnDiskBitmap(str(newPage[f'{i+1}']['image']))
            image = displayio.TileGrid(bitmapImage, pixel_shader=bitmapImage.pixel_shader, x=x, y=y)
            screen.append(image)
            
            #print(f'({x},{y})') 
            #print(i%3)
            #print(i//3)
            
            i+=1
            
        except OSError:
            #print(newPage[f'{i+1}']['image'])
            print('image doesnt exist')
            
            bitmapImage = displayio.OnDiskBitmap('/images/noimage.bmp')
            image = displayio.TileGrid(bitmapImage, pixel_shader=bitmapImage.pixel_shader, x=x, y=y)
            screen.append(image)
            
            i+=1
            
        except Exception as e:
            print(f'button at position {i+1} has no image reference')
            
            bitmapImage = displayio.OnDiskBitmap('/images/noimage.bmp')
            image = displayio.TileGrid(bitmapImage, pixel_shader=bitmapImage.pixel_shader, x=x, y=y)
            screen.append(image)
            
            i+=1
            
    display.root_group = screen
    return(newPage)
    

# Change page or call macro function
def handle_buttons(button, current_page, pages, runningMacros):
    try:
        # print(current_page[button]['page'])
        current_page = display_out(pages[current_page[button]['page']])
    except KeyError as e:
        print(e)
        # if the page doesnt exist throw error
        if str(e) != 'page':
            print('error')
        else:
            print('macro')
            runningMacros = handle_macro(current_page[button], runningMacros)
        pass
    return current_page

current_page = display_out(pages['Home'])
        
while True:
    if not btn1.value and btn1.value != btn1_last:
        print('button 1 pressed')
        current_page = handle_buttons('1', current_page, pages, runningMacros)
    if not btn2.value and btn2.value != btn2_last:
        print('button 2 pressed')
        current_page = handle_buttons('2', current_page, pages, runningMacros)
    if not btn3.value and btn3.value != btn3_last:
        print('button 3 pressed')
        current_page = handle_buttons('3', current_page, pages, runningMacros)
    if not btn4.value and btn4.value != btn4_last:
        print('button 4 pressed')
        current_page = handle_buttons('4', current_page, pages, runningMacros)
    if not btn5.value and btn5.value != btn5_last:
        print('button 5 pressed')
        current_page = handle_buttons('5', current_page, pages, runningMacros)
    if not btn6.value and btn6.value != btn6_last:
        print('button 6 pressed')
        current_page = handle_buttons('6', current_page, pages, runningMacros)
    if not btn7.value and btn7.value != btn7_last:
        print('button 7 pressed')
        current_page = handle_buttons('7', current_page, pages, runningMacros)
    if not btn8.value and btn8.value != btn8_last:
        print('button 8 pressed')
        current_page = handle_buttons('8', current_page, pages, runningMacros)
    if not btn9.value and btn9.value != btn9_last:
        print('button 9 pressed')
        current_page = handle_buttons('9', current_page, pages, runningMacros)
    
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