from pynput.keyboard import Key, Listener

macro = []
buffer = []

def on_press(key):
    global buffer, macro
    keyaction =  f'{str(key).lower()} press'

    if keyaction not in buffer:
        buffer.append(keyaction)
        if key != Key.esc:
            macro.append(keyaction)
        print(keyaction)

def on_release(key):
    global buffer, macro

    keyaction =  f'{str(key).lower()} release'

    if key == Key.esc:
        # Stop listener
        return False

    if f'{str(key).lower()} press' in buffer:
        buffer.remove(f'{str(key).lower()} press')
        macro.append(keyaction)
        print(keyaction)

def startlogging():
    global macro, buffer
    macro = []
    buffer = []
    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    
    # print(macro)
    return macro