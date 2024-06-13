import speech_recognition as sr
import pyaudio
import pyttsx3

# Setup Text to Speech
engine = pyttsx3.init()
text_to_speak = ''
# Setup Speech to Text
words = ''
recognizer = sr.Recognizer()
# Simple State Machine
current_state = 0
not_listening_state = 0
listening_state = 1

# Get audio from Mic
with sr.Microphone() as source:
    print("Say Something. If you wish to exit, say exit.")
    while True:
        audio = recognizer.listen(source)
        # Take audio and parse it into text
        if audio != []:
            words = recognizer.recognize_google(audio)
        else:
            words = ''
        print(words)
        # Compare text to see if the activation words has been spoken, then start listening
        if current_state == not_listening_state:
            if 'Brayden' in words or 'Braden' in words:
                current_state = listening_state
                print("Listening...")
        # Compare text to see what command should be executed only if already listening
        elif current_state == listening_state:
            if words == "cancel" or words == "Cancel":
                text_to_speak = "Cancelling..."
            elif 'hello' in words:
                text_to_speak = "Hello to you, too!"
            elif 'how are you' in words:
                text_to_speak = "Doing great! How about you?"
            elif words == "exit" or words == "Exit":
                engine.say("Exiting program...")
                engine.runAndWait()
                break
            else:
                text_to_speak = "Unknown Command. I think you said: " + words
        
            # Always respond to the Spoken Words
            print(text_to_speak)
            engine.say(text_to_speak)
            engine.runAndWait()
            current_state = not_listening_state
        else:
            print("Error")
            engine.say("Error")
            engine.runAndWait()
            current_state == not_listening_state