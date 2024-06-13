# Messing around with a Text to Speech Library following the tutorial at https://www.youtube.com/watch?v=j7m5st1VKfA&list=PLsFyHm8kJsx1A_KgUcsyRyX99pd6NOc50&index=45
import pyttsx3
engine = pyttsx3.init()
text_to_speak = ''
while text_to_speak != 'exit':
    text_to_speak = input('What should I say? ')
    engine.say(text_to_speak)
    engine.runAndWait()
    print('Type exit to quite the program')