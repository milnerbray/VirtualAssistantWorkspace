# Script to interact with Spotify
import pyautogui
import time
import psutil
import win32gui # type: ignore
import win32process # type: ignore
from pywinauto import Application

# locate physical window
def get_spotify_window_title(pids):
    titles = []
    returnpid = 0
    def _enum_cb(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            if pids is None or pid in pids:
                nonlocal returnpid
                returnpid = pid
    win32gui.EnumWindows(_enum_cb, titles)
    return returnpid

# Spotify Controls
# 0: Pause/Play: Space
# 1: Previous: Ctrl + Left
# 2: Next: Ctrl + Right
# 3: Quick Search: Ctrl + K
# 4: Repeat: Ctrl + R
# 5: Shuffle: Ctrl + S
# 6: Volume Up: Ctrl + Up
# 7: Volume Down: Ctrl + Down
def press_key(spotify_pids, command_val, search_string):
    app = Application().connect(process=get_spotify_window_title(spotify_pids))
    app.top_window().set_focus()
    time.sleep(1)
    if command_val == 0:
        # Pause/Play
        pyautogui.press('space')
    elif command_val == 1:
        # Previous
        pyautogui.hotkey('ctrl', 'left', interval=0.25)
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'left', interval=0.25)
    elif command_val == 2:
        # Next
        pyautogui.hotkey('ctrl', 'right', interval=0.25)
    elif command_val == 3:
        # Quick Search
        pyautogui.hotkey('ctrl', 'k', interval=0.25)
        pyautogui.write(search_string)
        time.sleep(0.5)
        pyautogui.hotkey('shift', 'enter', interval=0.25)
        pyautogui.press('esc')
    elif command_val == 4:
        # Repeat
        pyautogui.hotkey('ctrl', 'r', interval=0.25)
    elif command_val == 5:
        # Shuffle
        pyautogui.hotkey('ctrl', 's', interval=0.25)
    elif command_val == 6:
        # Volume Up
        for x in range(5):
            pyautogui.hotkey('ctrl', 'up', interval=0.1)
    elif command_val == 7:
        # Volume Down
        for x in range(5):
            pyautogui.hotkey('ctrl', 'down', interval=0.1)

    # Get the Window
    window = app.top_window()

    # Minimize the Window
    window.minimize()

program_name = "Spotify.exe"
process_ids = []
timeout = time.time() + 120
isOpen = False
while True and time.time() < timeout:
    # Check if the program is open
    for process in psutil.process_iter():
        try:
            if program_name in process.name():
                isOpen = True
                process_ids.append(process.pid)
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    else:
        if isOpen:
            print("Spotify is Open")
            time.sleep(1)
            # TODO: Voice Command to choose which happens
            press_key(process_ids, 3, "carry on my wayward son")
        else:
            print("Spotify is Closed")
        break