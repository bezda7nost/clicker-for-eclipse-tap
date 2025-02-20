import pyautogui
import time
import threading
from pynput import keyboard

# Global variables to control the clicker
clicking = False
delay = 0.08  # Adjust the click speed (in seconds)

def clicker():
    global clicking
    while True:
        if clicking:
            pyautogui.click()
        time.sleep(delay)

def reload_tab():
    global clicking
    was_clicking = clicking
    print("\nReloading the tab...")
    clicking = False
    pyautogui.hotkey('ctrl', 'r')
    print("Waiting 15 seconds...")
    time.sleep(15)
    clicking = was_clicking
    status = "Resuming autoclicker..." if clicking else "Autoclicker remains stopped."
    print(status)
    
    # Schedule next reload in 10 minutes (1770 seconds)
    threading.Timer(420, reload_tab).daemon = True
    threading.Timer(420, reload_tab).start()

def on_press(key):
    global clicking
    try:
        if key.char == 's':
            clicking = True
            print("Autoclicker started!")
        elif key.char == 'e':
            clicking = False
            print("Autoclicker stopped!")
        elif key.char == 'q':
            print("Exiting program...")
            return False
    except AttributeError:
        pass

# Start clicker thread
click_thread = threading.Thread(target=clicker)
click_thread.daemon = True
click_thread.start()

# Schedule first reload after 30 minutes (1800 seconds)
reload_timer = threading.Timer(420, reload_tab)
reload_timer.daemon = True
reload_timer.start()

print("Autoclicker started!")
print("Press 's' to start clicking, 'e' to stop, and 'q' to quit.")
print("The browser tab will automatically reload every 30 minutes.")

# Start keyboard listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()