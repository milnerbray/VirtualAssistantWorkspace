# Messing around with the speech_recognition library with the tutorial at https://www.youtube.com/watch?v=MRugVs73cVA
import speech_recognition as sr
import pyaudio

# Get audio from Mic
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Say Something")
    audio = recognizer.listen(source)
# Recognize the words spoken with Google's speech recognition
words = recognizer.recognize_google(audio)
# Respond to Spoken Words
if 'hello' in words:
    print("Hello to you, too!")
elif 'how are you' in words:
    print("Doing great! How about you?")
else:
    print("Not sure how to respond")