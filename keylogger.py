import time
from pynput.keyboard import Key, Listener

data_buffer = ""

def on_press(key):
    global data_buffer
    try:
        data_buffer += key.char
    except AttributeError:
        special_keys = {Key.space: " ", Key.enter: "\n", Key.tab: "[TAB]"}
        data_buffer += special_keys.get(key, f"[{key.name.upper()}]")

def on_release(key):
    if key == Key.esc:
        return False


listener = Listener(on_press=on_press, on_release=on_release)

listener.start()

try:
    print("Main process is running... (Press ESC to stop)")
    while listener.running:
        print(f"Main Process heartbeat. Buffer size: {len(data_buffer)} chars")
        
        if "[ENTER]" in data_buffer or "\n" in data_buffer:
            print(f">>> User just typed a line!")
            
        time.sleep(5)
except KeyboardInterrupt:
    listener.stop()

print("\nFinal capture:", data_buffer)