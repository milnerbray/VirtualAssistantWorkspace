# Tutorial at https://www.youtube.com/watch?v=8v3u4qvAGK8
# Script to interact with Spotify
import pyautogui
import time
import psutil

pyautogui.press('win')
time.sleep(1)
pyautogui.write('Spotify')
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)

program_name = 'Spotify.exe'

# set a timeout
timeout = time.time() + 120 # 2 min timeout

while True:
    # check to see if Spotify is open
    for process in psutil.process_iter():
        try:
            if process.name() == program_name:
                print("Spotify is open!")
                break
        except(psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    else:
        # if the program is not open, check for a timeout
        if time.time() > timeout:
            print("Timed out!")
            break
        else:
            # wait for a short amount of time before checking again
            time.sleep(1)
            continue
    break
time.sleep(4) # Fine Tune
pyautogui.press('space') # play the music