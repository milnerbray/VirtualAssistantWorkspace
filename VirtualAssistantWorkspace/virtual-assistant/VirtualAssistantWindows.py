import vosk
import pyaudio
import json
import pyttsx3
# Spotify Controls Libraries
import pyautogui
import time
import psutil
import win32gui # type: ignore
import win32process # type: ignore
import pyjokes as pj
import webbrowser as wb
from pywinauto import Application

# Spotify Controls Function
def spotify_controls(mode_val, search_val):
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
        elif command_val == 8:
            # Terminate Session
            pyautogui.hotkey('alt', 'f4', interval=0.25)
            return
        elif command_val == 9:
            # Bring up Window
            return
        elif command_val == 10:
            # Maximize Window
            app.top_window().maximize()
            return
        elif command_val == 11:
            # Minimize Window
            app.top_window().minimize()
            return

        # Minimize Window
        # app.top_window().minimize()

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
                press_key(process_ids, mode_val, search_val)
            else:
                print("Spotify is Closed")
            break

# Setup Text to Speech
engine = pyttsx3.init()
text_to_speak = ''

# Setup
model = vosk.Model(lang="en-us")
rec = vosk.KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192)
# Simple State Machine
current_state = 0
not_listening_state = 0
listening_state = 1
spotify_state = 2

print("Listening for speech. Start a command by saying 'brAIner'. Use the command 'Terminate' to stop.")
while True:
    data = stream.read(4096, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        recognized_text = result['text']
        if recognized_text != "":
            print(recognized_text)

        # Compare text to see if the activation words has been spoken, then start listening
        if current_state == not_listening_state:
            # brAIner might be a good possible name once AI is integrated in
            if 'brainer' in recognized_text.lower() and not 'no' in recognized_text.lower():
                current_state = listening_state
                print("Listening...")
                engine.say("Yes sir?")
                engine.runAndWait()
                # TODO: Pop up that shows brAIner is listening
        # Compare text to see what command should be executed only if already listening
        elif current_state == listening_state:
            # TODO: Functionality
            # TODO: Fix Substrings (Remove Hard Coding)
            # TODO: Notepad
            # TODO: Spotify API
            # TODO: Google???
            # TODO: Translations???
            if 'google' in recognized_text.lower():
                text_to_speak = "Opening Google"
                print(text_to_speak)
                engine.say(text_to_speak)
                engine.runAndWait()
                wb.open_new_tab("https://www.google.com/")
                text_to_speak = "Searching for " + recognized_text[7:]
                print(text_to_speak)
                engine.say(text_to_speak)
                engine.runAndWait()
                pyautogui.write(recognized_text[7:])
                pyautogui.press('enter')
                text_to_speak = ""
            elif 'you tube search' in recognized_text.lower() or 'youtube search' in recognized_text.lower():
                text_to_speak = "Opening YouTube"
                print(text_to_speak)
                engine.say(text_to_speak)
                engine.runAndWait()
                wb.open_new_tab("https://www.youtube.com/")
                time.sleep(5)
                text_to_speak = "Searching for " + recognized_text[16:]
                print(text_to_speak)
                engine.say(text_to_speak)
                engine.runAndWait()
                for x in range(4):
                    pyautogui.press('tab')
                    time.sleep(0.1)
                pyautogui.write(recognized_text[16:])
                pyautogui.press('enter')
                text_to_speak = ""
            elif 'you tube' in recognized_text.lower() or 'youtube' in recognized_text.lower():
                text_to_speak = "Opening YouTube"
                print(text_to_speak)
                engine.say(text_to_speak)
                engine.runAndWait()
                text_to_speak = ""
                wb.open_new_tab("https://www.youtube.com/")
            elif 'fandango' in recognized_text.lower():
                text_to_speak = "Opening Vudu"
                print(text_to_speak)
                engine.say(text_to_speak)
                engine.runAndWait()
                text_to_speak = ""
                wb.open_new_tab("https://www.vudu.com/")
            elif 'netflix' in recognized_text.lower():
                text_to_speak = "Opening Netflix"
                print(text_to_speak)
                engine.say(text_to_speak)
                engine.runAndWait()
                text_to_speak = ""
                wb.open_new_tab("https://www.netflix.com/")
            elif 'prime video' in recognized_text.lower() or 'video' in recognized_text.lower():
                text_to_speak = "Opening Amazon Prime Video"
                print(text_to_speak)
                engine.say(text_to_speak)
                engine.runAndWait()
                text_to_speak = ""
                wb.open_new_tab("https://www.amazon.com/Amazon-Video/b/?ie=UTF8&node=2858778011&ref_=nav_cs_prime_video")
            elif 'hulu' in recognized_text.lower() or 'who lou' in recognized_text.lower():
                text_to_speak = "Opening Hulu"
                print(text_to_speak)
                engine.say(text_to_speak)
                engine.runAndWait()
                text_to_speak = ""
                wb.open_new_tab("https://www.hulu.com/")
            elif 'h b o' in recognized_text.lower():
                text_to_speak = "Opening HBO Max"
                print(text_to_speak)
                engine.say(text_to_speak)
                engine.runAndWait()
                text_to_speak = ""
                wb.open_new_tab("https://play.max.com/")
            elif 'start music' in recognized_text.lower():
                # Must have Spotify installed on your Windows device for this command to work
                text_to_speak = "Launching Spotify"
                print(text_to_speak)
                engine.say(text_to_speak)
                engine.runAndWait()
                text_to_speak = ""
                exec(open(r"C:\Users\milne\Downloads\VirtualAssistantWorkspace\virtual-assistant\SpotifyOpenWin.py").read())
            elif 'music interface' in recognized_text.lower() or 'user interface' in recognized_text.lower():
                # Must have Spotify installed on your Windows device for this command to work
                text_to_speak = "Moving to Spotify Control Interface"
                current_state = spotify_state
            elif 'joke' in recognized_text.lower():
                text_to_speak = pj.get_joke()
            elif 'hello' in recognized_text.lower():
                text_to_speak = "Hello to you too!"
            elif 'how are you' in recognized_text.lower():
                text_to_speak = "Doing great! How can I help you?"
            elif 'cancel' in recognized_text.lower():
                text_to_speak = "Cancelling..."
            elif 'terminate' in recognized_text.lower():
                text_to_speak = "Termination keyword detected. Goodbye."
                print(text_to_speak)
                engine.say(text_to_speak)
                engine.runAndWait()
                break
            elif recognized_text == '':
                text_to_speak = "Timed out. Cancelling..."
            else:
                text_to_speak = "Unknown Command. I think you said: " + recognized_text.lower()
            
            # Always respond to the Spoken Words
            if text_to_speak != "":
                print("brAIner: " + text_to_speak)
                engine.say(text_to_speak)
                engine.runAndWait()
            if current_state != spotify_state:
                current_state = not_listening_state
        elif current_state == spotify_state:
            menu_val = 0
            search_val = ""
            text_to_speak = ""
            if 'toggle' in recognized_text.lower() or 'play' in recognized_text.lower() or 'pause' in recognized_text.lower():
                text_to_speak = "Toggling Music on Spotify"
            elif 'previous' in recognized_text.lower():
                text_to_speak = "Previous Song"
                menu_val = 1
            elif 'next' in recognized_text.lower() or 'skip' in recognized_text.lower():
                text_to_speak = "Next Song"
                menu_val = 2
            elif 'search' in recognized_text.lower():
                text_to_speak = "Searching for " + recognized_text[7:]
                search_val = recognized_text[7:]
                menu_val = 3
            elif 'repeat' in recognized_text.lower():
                text_to_speak = "Toggling Repeat Setting"
                menu_val = 4
            elif 'shuffle' in recognized_text.lower():
                text_to_speak = "Toggling Shuffle Setting"
                menu_val = 5
            elif 'volume up' in recognized_text.lower():
                text_to_speak = "Turning Volume Up"
                menu_val = 6
            elif 'volume down' in recognized_text.lower():
                text_to_speak = "Turning Volume Down"
                menu_val = 7
            elif 'terminate session' in recognized_text.lower():
                text_to_speak = "Terminating Spotify Session"
                menu_val = 8
            elif 'open' in recognized_text.lower() or 'show' in recognized_text.lower():
                text_to_speak = "Opening Window"
                menu_val = 9
            elif 'maximize' in recognized_text.lower():
                text_to_speak = "Maximizing Window"
                menu_val = 10
            elif 'minimize' in recognized_text.lower():
                text_to_speak = "Minimizing Window"
                menu_val = 11
            elif 'cancel' in recognized_text.lower():
                text_to_speak = "Cancelling..."
                menu_val = -1
            elif recognized_text == '':
                text_to_speak = "Timed out. Cancelling..."
                menu_val = -1
            print(text_to_speak)
            engine.say(text_to_speak)
            engine.runAndWait()
            current_state = not_listening_state
            if menu_val != -1:
                spotify_controls(menu_val, search_val)
        else:
            print("Error")
            engine.say("Error")
            engine.runAndWait()
            current_state = not_listening_state

stream.stop_stream()
stream.close()
p.terminate()