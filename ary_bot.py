# ---------- import dependencies and libraries section ----------

import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pyjokes
from googlesearch.googlesearch import GoogleSearch
import webbrowser
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from playsound import playsound
import pyautogui
import cv2
import numpy as np
from win32api import GetSystemMetrics
import requests
import pywhatkit as kit
import json
import time
import keyboard

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))

# ---------- main caller function section ----------

# plays the predefined commands as audio to the user
def talk(text):
    engine.say(text)
    engine.runAndWait()

# takes voice command from the user
def take_command():
    try:
        # set default command value as null string 
        # in case the bot does not recognise audio
        command = ''    
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)             # voice from user microphone input as source
            command = listener.recognize_google(voice)  # feed voice to text from library
            command = command.lower()                   # convert query to lowercase to match with conditional statements

    except Exception as e:                              # print error message in case of an exception
            print(e)
    return command                                      


# ---------- weather app section ----------

def weather(city):
    talk("Showing weather today at "+city)
    url = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=1707e684234c3af66fafa488873e55a2"
    data = requests.get(url)
    weather = data.json()                       # convert json format data into python format data
    
    if weather["cod"] != "404":
        w = weather["main"]                     # store the value of "main"
        current_temperature = w["temp"]
        current_humidity = w["humidity"]
        current_feels_like = w["feels_like"]
        current_min = w["temp_min"]
        current_max = w["temp_max"]
        z = weather["weather"]
        weather_description = z[0]["description"]

        print("\n temperature = " + "{:.1f}".format(current_temperature - 273.15) + "°C" +
          "\n tempertaure MIN. = " + "{:.1f}".format(current_min - 273.15) + "°C  MAX. = " + "{:.1f}".format(current_max - 273.15) + "°C" +
          "\n cloudiness = " + str(weather["clouds"]["all"]) + "%" +
          "\n wind speed = " + str(weather["wind"]["speed"]) + " m/s" +
          "\n humidity = " + str(current_humidity) + "%")
        talk("\n today feels like " + "{:.1f}".format(current_feels_like - 273.15) + " degree celsius")
        talk("\n today's weather is " + str(weather_description))
 
    else:
        print(" City Not Found !!!")


# ---------- Social Media Bot section ----------

# create audio record file
def record_msg():
    
    freq = 44100
    duration = 10
    
    # record audio file
    print("recording message...")
    recording = sd.rec(int(duration * freq), samplerate = freq, channels = 2)
    sd.wait()
    write("msg.wav", freq, recording)
    wv.write("msg.wav", recording, freq, sampwidth = 2)
    talk("done recording...")
    sd.stop()

def fb_message(contact, message):
    browser = "chrome"
    url = "https://www.facebook.com/"
    webbrowser.get(browser).open_new(url)
    time.sleep(10)
    pyautogui.click(x=1732, y=160)
    time.sleep(2)
    pyautogui.click(x=1540, y=292)
    time.sleep(2)
    keyboard.write(contact)
    time.sleep(2)
    pyautogui.click(x=1586, y=350)
    time.sleep(2)
    pyautogui.click(x=1615, y=993)
    time.sleep(0.5)
    keyboard.write(message)
    time.sleep(0.5)
    pyautogui.press('enter')

def wp_message(contact, message):
    browser = "chrome"
    url = "https://web.whatsapp.com/"
    webbrowser.get(browser).open_new(url)
    time.sleep(10)
    pyautogui.click(x=356, y=258)
    time.sleep(0.5)
    keyboard.write(contact)
    time.sleep(2)
    pyautogui.click(x=312, y=420)
    time.sleep(0.5)
    pyautogui.click(x=1174, y=972)
    time.sleep(0.5)
    keyboard.write(message)
    time.sleep(0.5)
    pyautogui.press('enter')


# ---------- news read section ----------

def news_read():
    text = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=fdc15c6da280423c98e7f741307ca090")
    news = json.loads(text.content)
    
    for i in range(10):    
        title = news['articles'][i]['title']
        description = news['articles'][i]['description']
        print('News ', i+1, ": ", title)
        print(description)
        talk(title)
        talk(description)


# ---------- screen recorder definition section ----------

def screen_shot():
    img = pyautogui.screenshot()                    # Take screenshot using PyAutoGUI
    frame = np.array(img)                           # Convert the screenshot to a numpy array            
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert it from BGR(Blue, Green, Red) to # RGB(Red, Green, Blue)
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    file_name = time_stamp + " ss.png"
    cv2.imwrite(file_name, frame)
  
def record_screen():

    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    resolution = (width, height)
    codec = cv2.VideoWriter_fourcc(*"XVID")
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    file_name = time_stamp + " recording.avi"
    fps = 30.0
    out = cv2.VideoWriter(file_name, codec, fps, resolution)
    
    print("Allow webcam to add to the screen recording? (y/n)")
    choice = input()
    if (choice == 'y'):
        webcam = cv2.VideoCapture(0)

    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Live", 640, 480)
    print("Press 'q' to stop the recording")

    while True:
        img = pyautogui.screenshot()                    # Take screenshot using PyAutoGUI
        frame = np.array(img)                           # Convert the screenshot to a numpy array            
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert it from BGR(Blue, Green, Red) to # RGB(Red, Green, Blue)

        if (choice == 'y'):                             # allow webcam to add to capture screen
            _, frame_2 = webcam.read()
            cam_h, cam_w, _ = frame_2.shape
            frame[0:cam_h, 0:cam_w, :] = frame_2[0:cam_h, 0:cam_w, :]

        out.write(frame)                                # Write it to the output file
        cv2.imshow('Live', frame)                       # Display the recording screen
        
        if cv2.waitKey(1) == ord('q'):                  # Stop recording when we press 'q'
            break
  
    out.release()
    cv2.destroyAllWindows()


# ---------- voice recorder-player definition section ----------

def record_voice():
    
    freq = 44100
    duration = 10
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    file_name = time_stamp + " recording.wav"

    # record audio file
    print("recording voice...")
    recording = sd.rec(int(duration * freq), samplerate = freq, channels = 2)
    sd.wait()
    write(file_name, freq, recording)
    wv.write(file_name, recording, freq, sampwidth = 2)
    talk("done recording...")
    sd.stop()

    # play recorded audio
    print('playing saved recording...')
    playsound(file_name)
    talk('Hey! how about a collab concert')


# ---------- search query based on input section ----------
def run_ary():
    flag = True

    while(flag):
        command = take_command()
        print(command)

        #conditional statement based on command recieved
        if 'how are you' in command:
            talk("Hi user, how are you doing. Hope you doing fine")

        elif 'hello world' in command:
            talk('The world is at Sharda University. Where are you?')

        elif 'play' in command:
            try:
                song = command.replace('play', '')
                talk('playing ' + song)
                kit.playonyt(song)
            
            except Exception as e:
                print (e)

        elif 'show me' in command:
            try:
                item = command.replace('show me', '')
                talk('showing ' + item)
                url = 'https://www.google.com/search?q='+item+'&tbm=shop'
                webbrowser.open_new(url)

            except Exception as e:
                print (e)

        elif 'where is' in command:
            try:
                dir = command.replace('where is', '')
                talk('showing ' + dir + ' on google maps')
                url = 'https://www.google.com/maps/place/'+dir
                webbrowser.open_new(url)

            except Exception as e:
                print (e)

        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('Current time is ' + time)

        elif 'send whatsapp message to' in command:
            try:
                contact = command.replace('send whatsapp message to ', '')
                print("record your message for ", contact)
                talk("record your message for "+contact)
                record_msg()
                filename = "msg.wav"
                r = sr.Recognizer()
                with sr.AudioFile(filename) as source:
                    audio_data = r.record(source)
                    message = r.recognize_google(audio_data)
                    wp_message(contact, message)

            except Exception as e:
                print (e)
                talk('Sorry!!! There was an error sending message')

        elif 'send facebook message to' in command:
            try:
                contact = command.replace('send facebook message to ', '')
                print("record your message for ", contact)
                talk("record your message for "+contact)
                record_msg()
                filename = "msg.wav"
                r = sr.Recognizer()
                with sr.AudioFile(filename) as source:
                    audio_data = r.record(source)
                    message = r.recognize_google(audio_data)
                    fb_message(contact, message)

            except Exception as e:
                print (e)
                talk('Sorry!!! There was an error sending message')

        elif 'who is' in command:
            try:
                person = command.replace('who is', '')
                info = wikipedia.summary(person, 2)
                print(info)
                talk(info)

            except Exception as e:
                print (e)
                talk('Sorry!!! Your person is not that famous right now')
        
        elif 'what is' in command:
            try:
                question = command.replace('what is', '')
                info = wikipedia.summary(question, 2)
                print(info)
                talk(info)

            except Exception as e:
                print (e)
                talk("Sorry!!! We couldn't find what you asked for")

        elif 'date today' in command:
            talk(datetime.date.today())

        elif 'day today' in command:
            now = datetime.datetime.now()
            talk(now.strftime("%A"))

        elif 'news today' in command:
            news_read()

        elif 'take a screenshot' in command:
            screen_shot()

        elif 'weather today in' in command or 'weather in' in command:
            try:
                city = command.replace('weather today in', '')
                weather(city)

            except Exception as e:
                print (e)
                talk("Sorry!!! We couldn't find the results")

        elif 'joke' in command or 'tell me a joke' in command:
            talk(pyjokes.get_joke())

        elif 'record my voice' in command or 'record voice' in command:
            record_voice()

        elif 'record screen' in command or 'record my screen' in command:
            record_screen()

        elif 'bye' in command or 'good night' in command or 'see you' in command:
            talk("It's been a long day, without you my friend. And I'll tell you all about it when I see you again, Take Care...")
            flag = False
        
        elif(command==''):
            talk("Please repeat the command I couldn't hear you.")
        
        else:
            talk('Here are some results from google to help you with')

            url = "https://www.google.co.in/search?q="+command
            webbrowser.open_new(url)

# ---------- driver function section ----------
run_ary()
print("It was nice meeting you")


  
