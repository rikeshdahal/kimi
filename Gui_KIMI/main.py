import cv2
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from ui import *
from PyQt5.QtGui import QPixmap
from plyer import notification
from pydub.playback import play
from pygame import mixer
from pynput.keyboard import Key, Controller
from time import sleep
from tkinter import *
import datetime
import audioop
import time
import keyboard
import openai
import os
import pyaudio
import pyjokes
import pyperclip
import pyttsx3
import random
import requests
import speech_recognition as sr
import struct
import sys
import webbrowser
import wikipedia
from vosk import Model, KaldiRecognizer
import pyaudio
import socket
from pydub.playback import play
from pydub import *
from urllib.parse import quote
import urllib.request
import json
import mysql.connector
model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1,
                  rate=16000, input=True, frames_per_buffer=1600)
stream.start_stream()
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="kimi"
)
c = conn.cursor()
# Create a table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS tasks
             (id INT AUTO_INCREMENT PRIMARY KEY, question VARCHAR(255), answer VARCHAR(255))''')
conn.commit()
# database############


def greetMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning,sir")
    elif hour > 12 and hour <= 18:
        speak("Good Afternoon ,sir")

    else:
        speak("Good Evening,sir")

    speak("Please tell me, How can I help you ?")


def weather():
    import requests
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q=Ludhiana'
        json_data = requests.get(url).json()
        format_add = json_data['weather'][0]['main']
        format_temp = json_data['coord']['lat']
        temp = f'Temperature in Your City is {format_temp} Degrees Celsius, and the Climate is {format_add}'
    except:
        temp = 'Weather Forecast is Currently Unavailable'

    out = f'{temp}. Have a good day, Sir.'

    speak(out)


def opens(text):
    import pyautogui
    pyautogui.press("super")
    sleep(1.5)
    pyautogui.typewrite(text)
    pyautogui.press("enter")


def ran(fun):
    import random
    r = random.randint(0, len(fun)-1)
    out = fun[r]
    speak(out)


def create_task(question, answer):
    c.execute("INSERT INTO tasks (question, answer) VALUES (%s, %s)",
              (question, answer))
    conn.commit()
    print("Task created successfully!")
    # speak("Task created successfully!")


def read_tasks():
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    if tasks:
        print("Tasks:")
        for task in tasks:
            print(f"- {task[1]}")
    else:
        print("No tasks found.")


def update_task(task_id, new_question, new_answer):
    c.execute("UPDATE tasks SET question = %s, answer = %s WHERE id = %s",
              (new_question, new_answer, task_id))
    conn.commit()
    speak("Task updated successfully!")


def delete_task(task_id):
    c.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    speak("Task deleted successfully!")


def get_answerfromopenai(question):
    c.execute("SELECT answer FROM tasks WHERE question = %s", (question,))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=0.5,
            max_tokens=60,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0,
        )
        if response.choices:
            answer = response.choices[0].text.strip()
            create_task(question, answer)
            return answer
        else:
            return "I'm sorry, but I don't have an answer to that question."


def get_answer(question):
    c.execute("SELECT answer FROM tasks WHERE question = %s", (question,))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        speak("I'm sorry, but I don't have an answer to that question.")


def talk(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 135)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    print("kimi: "+text)
    engine.say(str(text))
    engine.runAndWait()
    engine.stop()


try:
    socket.create_connection(("www.google.com", 80))
    connected = True
except OSError:
    connected = False
if connected:
    talk("Connected to the internet.")
else:
    print("Not connected to the internet.")


def listen():
    if connected:
        return listen_online()
    else:
        return listen_offline()


def listen_online():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\033[32mListening....\033[0m")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 4)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language="en-in")
        print(f"YOU : {query}.")
        window.terminalPrint(f"YOU : {query}.")

    except:
        return ""

    query = str(query)
    return query.lower()


def listen_offline():
    print("\033[32mListening....\033[0m")
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            p = text[14:-3]
            window.terminalPrint(f"YOU : {p}.")
            if len(p) > 0:
                return p
        elif not data:
            break


keyboard = Controller()

audio_stream = None
interaction_counter = 0


def read_clipboard():
    text = pyperclip.paste()
    if text:
        speak(text)
    else:
        print("No text found in clipboard.")


def volumeup():
    for i in range(5):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(0.1)


def volumedown():
    for i in range(5):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(0.1)


how = ['I am Fine Sir, What about You',
       'I am fine as always', 'what you think', 'just fine!!']
love = ["I love you too", "Aww, thank you for the kind words! I'm here as your digital friend  to help you with any questions or information you might need.", "Remember, I'm always here for you! ", "ohh, thanks you for love i am so glad to know each other.",
        "ohh. love you it\'s always nice to make a new friends."]
angry = ["thats not good i am here to help you so focus for it , so what can i help you today?",
         "it\'s a last warning if you say again i am gone"]
name = ['You Can call me KIMI', 'My Name Is KIMI',
        'you named me KIMI', 'You Should Know this, My name Is KIMI', "my name is Kimi it\'s Lovely to meet you", "I am KIMI"]
creator = ['You made Me Boss!', 'I was Made by Rekeash & Piyush']
can = ['I Can Do Everything .', 'Just Give Me A Try And Figure This Out.',
       'What you Coded Within Me ;) ', 'Your Choice']
sorry = ["sorry", "sorry you wil have to train me first then  can answer your question", "I did not get that", 'What You Said?',
         'I was Unable To Understand', 'I have some Bugs Because of you']
here = ['To Help You Out', 'To Help You To Do Tasks',
        'To Be Your Assistant', 'You Called me, Thatwise']
frd = ['I will Feel Lucky To Be Your Friend', 'Yaa Ofcource']
me = ['You Told Me Your Name, Rekeash & Piyush',
      'I Think That\'s Rekeash & Piyush', 'Your Name That I Know Is Rekeash lot a thanks  Piyush']
thanks = ['My Pleasure', 'Welcome',
          'Ohh Don\'t amberis me by saying thanks ', 'So Sweet!!']
jokes = ['Here is random joke sir', "Sure, here's one for you!",
         'Woho. i am excited to tell you a joke']
joke = ['Why did the tomato turn red? Because it saw the salad dressing!', 'Why don\'t scientists trust atoms? Because they make up everything!', 'Why don\'t skeletons fight each other? They don\'t have the guts!', 'Why did the computer go to the doctor? Because it had a virus!', 'What do you call fake spaghetti? An impasta!',
        'How does a penguin build its house? Igloos it together!', 'Why did the bicycle fall over? Because it was two-tired!', 'Why did the scarecrow win an award? Because he was outstanding in his field!']
greet = ['Hey Whats up!', 'Hello Rekeash',
         'Hi !', 'Hello, How can I help You', 'I am here']
bye = ["bye ", "I am terminating after 3 seconds. 3 , 2 , 1, goodbye"]
fine = ["ohh sound good ", "Nice here that"]


def welcome():
    ran(greet)


counter = 0


def command():
    global counter
    while True:
        query = listen().lower()

        if "wake up" in query:
            counter = 0
            window.blink_interval = 3
            greetMe()

            while True:
                query = listen().lower()
                if "create" in query:
                    speak("Please say the question.")
                    question = listen()
                    speak("Please say the answer.")
                    answer = listen()
                    if question and answer:
                        create_task(question, answer)
                elif "read" in query or "show" in query:
                    read_tasks()
                elif "update" in query:
                    speak("Please say the task ID.")
                    task_id = listen()
                    speak("Please say the new question.")
                    new_question = listen()
                    speak("Please say the new answer.")
                    new_answer = listen()
                    if task_id and new_question and new_answer:
                        update_task(task_id, new_question, new_answer)
                elif "delete" in query or "remove" in query:
                    speak("Please say the task ID.")
                    task_id = listen()
                    if task_id:
                        delete_task(task_id)
                    ## get from data base##
                elif "hey" in query or "kimi" in query or "Kimmy" in query:
                    str1 = query.replace("kimi ", "")
                    str2 = str1.replace("hey ", "")
                    query = str2.replace("Kimmy ", "")
                    answer = get_answer(query)
                    if answer:
                        speak(f"{answer}.")
                        ########## Tasks #################
                elif "go to sleep" in query or "sleep" in query:
                    speak("okay sir you can call me any time!")
                    window.blink_interval = 0
                    break
                elif "what is your name" in query or "your name" in query:
                    ran(name)
                elif "goodbye" in query or "quit" in query:
                    speak("I am terminating After 3 seconds")
                    speak("3")
                    sleep(1)
                    speak("2")
                    sleep(1)
                    speak("1")
                    sleep(1)
                    speak("Good bye")
                    sys.exit()
                elif "click my photo" in query or "take my photo" in query:
                    import pyautogui
                    pyautogui.press("super")
                    sleep(2)
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    sleep(5)
                    speak("SMILE")
                    pyautogui.press("enter")
                    speak("captured")
                elif "capture" in query or "capture pic" in query:
                    speak("SMILE")
                    pyautogui.press("enter")
                    speak("captured")
                    sleep(1)
                    speak("you look smart sir")
                elif "who are you" in query or "where are you from" in query:
                    audio = AudioSegment.from_wav("media\\mahunepalibabu.wav")
                    play(audio)
                elif "open" in query or "lunch" in query:
                    str = query.replace("open ", "")
                    str12 = str.replace("lunch ", "")
                    speak("opening " + str12)
                    opens(str12)
                elif "youtube" in query:
                    import pywhatkit
                    query = query.replace("youtube", "")
                    pywhatkit.playonyt(query)
                    speak("opening")
                elif "wikipedia" in query:
                    speak("Searching from wikipedia....")
                    query = query.replace("wikipedia", "")
                    query = query.replace("search wikipedia", "")
                    query = query.replace("kimi", "")
                    Results = wikipedia.summary(query, sentences=2)
                    speak("According to wikipedia..")
                    print(Results)
                    speak(Results)

                elif "click" in query:
                    import pyautogui
                    import time
                    speak("Searching buttons")
                    query = query.replace("click ", "")
                    query = query.replace("kimi ", "")
                    time.sleep(2)
                    pyautogui.hotkey('ctrl', 'f')
                    pyautogui.typewrite(query)
                    time.sleep(1)
                    pyautogui.hotkey('ctrl', 'enter')
                    speak(query+"buttons Clicked")

                elif "google" in query:
                    import wikipedia as googleScrap
                    query = query.replace("kimi", "")
                    query = query.replace("google search", "")
                    query = query.replace("google", "")
                    speak("This is what i found on google")
                    try:
                        pywhatkit.search(query)
                        result = googleScrap.summary(query, 1)
                        speak(result)
                    except:
                        speak("No speakable output available")
                elif "what is your name" in query or "your name" in query:
                    ran(name)
                elif "how are you" in query:
                    ran(how)
                elif "i am fine" in query or "fine" in query:
                    ran(fine)
                elif "joke" in query or "tell me" in query:

                    ran(jokes)
                    ran(joke)
                    speak(
                        "I hope you enjoyed these jokes! Let me know if there's anything else I can assist you with")

                elif "what time is it" in query or "time" in query:
                    import datetime
                    now = datetime.datetime.now()
                    time = now.strftime('%I:%M %p')
                    speak('The current time is ' + time)
                elif "task add" in query or "create task" in query:
                    tasks = []
                    speak("Do you want to clear old tasks (Please Speak YES or NO)")
                    query = input("you: ")
                    if "yes" in query:
                        file = open("data\\tasks.txt", "w")
                        file.write(f"")
                        file.close()
                        speak("Enter the number of tasks")
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        i = 0
                        for i in range(no_tasks):
                            speak("Enter the tasks")
                            tasks.append(input("Enter the task :- "))
                            file = open("data\\tasks.txt", "a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                            speak("tasks Added")
                    elif "no" in query:
                        i = 0
                        speak("Enter the number of tasks")
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        for i in range(no_tasks):
                            speak("Enter the tasks")
                            tasks.append(input("Enter the task :- "))
                            file = open("data\\tasks.txt", "a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                            speak("tasks Added")
                elif "what is my task" in query:
                    file = open("data\\tasks.txt", "r")
                    content = file.read()
                    file.close()
                    mixer.init()
                    speak("check i will send you a schedule")
                    mixer.music.load("media\\notification.mp3")
                    mixer.music.play()
                    notification.notify(
                        title="My schedule :-",
                        message=content,
                        timeout=15
                    )
                elif "screenshot" in query:
                    import pyautogui
                    im = pyautogui.screenshot()
                    speak("save screenshot from which name sir")
                    query = listen()
                    im.save(query+".jpg")
                    speak("captured")
                elif "get lost" in query or "lost" in query:
                    out = 'You Can\'t Talk To Me Like This,I know, every boy are same,  \n I Am Going.'
                    speak(out)
                    sys.exit(0)
                elif "weather" in query or "wether today" in query:
                    weather()

                elif "make a note" in query:
                    import pyautogui
                    opens("notepad")
                    speak("what do you want to note?")
                    note = listen()
                    pyautogui.typewrite(note)
                    speak("note created successfully")
                    pyautogui.hotkey('alt', 'f4')
                    speak("do you want to save the note? (Please Speak YES or NO)")
                    condition = listen()
                    if "yes" in condition:
                        pyautogui.press("enter")
                        speak("note saved successfully")
                        pyautogui.press("enter")
                    elif "no" in condition:
                        pyautogui.keyDown('left')
                        pyautogui.press("enter")
                        speak("okay note not saved")
                elif "temperature" in query:
                    search = "temperature in kathmandu"
                    url = f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text, "html.parser")
                    temp = data.find("div", class_="BNeawe").text
                    speak(f"current{search} is {temp}")
                elif "good job" in query:
                    speak("Thanks for your complement")
                elif "thanks" in query or ("thank you") in query:
                    ran(thanks)
                elif "love you" in query:
                    ran(love)
                elif "who made you" in query or "who is your father" in query:
                    ran(creator)
                elif "go to" in query:
                    Nameofweb = query.replace("go to ", "")
                    Link = f"https://www.{Nameofweb}.com"
                    webbrowser.open(Link)
                    speak("ok now i am going to " + Nameofweb)
                elif "close" in query:
                    pyautogui.hotkey('alt', 'f4')
                    speak("window closed")
                elif "admin panel" in query:
                    web = (
                        "http://localhost/phpmyadmin/index.php?route=/sql&pos=0&db=hacker&table=tasks")
                    webbrowser.open(web)
                    speak("ok now i am going to " + query)
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that", "")
                    rememberMessage = query.replace("kimi", "")
                    speak("You told me to "+rememberMessage)
                    remember = open("remember.txt", "a")
                    remember.write(rememberMessage)
                    remember.close()
                elif "what do you remember" in query:
                    remember = open("remember.txt", "r")
                    speak("You told me to remember that " + remember.read())
                elif "hello" in query:
                    ran(greet)
                elif "what can you do" in query:
                    ran(can)
                elif 'play music' in query:
                    try:
                        out = 'Playing Music'
                        print(out)
                        speak(out)
                        mus_dir = r'C:\\Users\\dahal\\Music'
                        songs = os.listdir(mus_dir)
                        r = random.randint(0, len(mus_dir) - 1)
                        os.startfile(os.path.join(mus_dir, songs[r]))
                    except:
                        out = 'Playing Music'
                        print(out)
                        speak(out)
                        mus_dir = r'C:\\Users\\dahal\\Music'
                        songs = os.listdir(mus_dir)
                        r = random.randint(0, len(mus_dir) - 1)
                        os.startfile(os.path.join(mus_dir, songs[r]))
                else:
                    ran(sorry)
        if len(query) >= 3:
            counter += 1
            if counter >= 3:
                speak("Please say 'wake up' to activate me.")


def set_audio_threshold(self, threshold):
    self.audio_threshold = threshold


def speak(Text):
    engine = pyttsx3.init()
    window.audio_threshold = 2000
    engine.setProperty('rate', 135)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    window.terminalPrint(f"KIMI : {Text}.")
    engine.say(str(Text))
    engine.runAndWait()
    engine.stop()
    window.audio_threshold = 30000


class kimiMain(QThread):
    def __init__(self):
        super(kimiMain, self).__init__()

    def run(self):
        self.runkimi()

    def runkimi(self):
        while True:
            command()


startExecution = kimiMain()
WINDOW_SIZE = 0


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setMouseTracking(True)
        self.setWindowIcon(QtGui.QIcon("media\\kimi_base.jpg"))
        self.setWindowTitle("KIMI The Voice-Assistant")
        self.camera = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.camera_frame)
        self.timer.start(30)
        self.avatar_image = cv2.imread('media\\kimi_base1.png')
        self.eye_open = cv2.imread('media\\eyeopen.png')
        self.eye_close = cv2.imread('media\\eyeclose.png')
        self.mouth_open = cv2.imread('media\\mouthopen.png')
        self.mouth_close = cv2.imread('media\\mouthclose.png')
        self.eye_x, self.eye_y = 270, 165
        self.mouth_x, self.mouth_y = 290, 260
        self.eye_open = cv2.resize(self.eye_open, (150, 50))
        self.eye_close = cv2.resize(self.eye_close, (150, 50))
        self.mouth_open = cv2.resize(self.mouth_open, (62, 40))
        self.mouth_close = cv2.resize(self.mouth_close, (62, 40))
        self.setup_audio()
        self.last_blink_time = time.time()
        self.blink_duration = 0.1
        self.blink_interval = 0
        self.audio_threshold = 30000
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 150))
        self.ui.close.clicked.connect(self.close)
        self.ui.debug.clicked.connect(self.manualCodeFromTerminal)
        self.ui.output.textChanged.connect(self.autoscroll)
        self.ui.debug.clicked.connect(self.toggledebug)
        self.ui.mic.clicked.connect(self.togglemic)
        self.ui.camera.clicked.connect(self.togglecam)
        self.ui.sound.clicked.connect(self.togglesound)
        self.ui.screen.clicked.connect(self.togglescreen)
        self.ui.input.returnPressed.connect(self.manualCodeFromTerminal)
        startExecution.start()
        self.show()

    def autoscroll(self):
        # Move the cursor to the end of the document
        cursor = self.ui.output.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.ui.output.setTextCursor(cursor)
        self.ui.output.ensureCursorVisible()

    def toggledebug(self):
        if self.ui.output.isVisible():
            self.ui.output.setVisible(False)
            self.ui.debug.setIcon(QIcon("media\\hide.png"))
        else:
            self.ui.output.setVisible(True)
            self.ui.debug.setIcon(QIcon("media\\debug.png"))

    def togglemic(self):
        if self.ui.input.isVisible():
            self.ui.input.setVisible(False)
            self.ui.mic.setIcon(QIcon("media\\mic.png"))
        else:
            self.ui.input.setVisible(True)
            self.ui.mic.setIcon(QIcon("media\\muted.png"))

    def togglecam(self):
        if self.ui.cam.isVisible():
            self.ui.cam.setVisible(False)
            self.ui.camera.setIcon(QIcon("media\\camera.png"))
        else:
            self.ui.cam.setVisible(True)
            self.ui.camera.setIcon(QIcon("media\\off.png"))

    def togglesound(self):
        if self.ui.sound.isChecked():
            self.ui.sound.setIcon(QIcon("media\\sound.png"))
        else:
            self.ui.sound.setIcon(QIcon("media\\muted_sound.png"))

    def togglescreen(self):
        global WINDOW_SIZE
        win_status = WINDOW_SIZE
        if win_status == 0:
            WINDOW_SIZE = 1
            self.showMaximized()
            self.ui.screen.setIcon(QIcon("media\\fullscreen.png"))
        else:
            WINDOW_SIZE = 0
            self.showNormal()
            self.ui.screen.setIcon(QIcon("media\\halfscreen.png"))

    def search_image(self):
        query = self.ui.input.text()
        if query:
            try:
                encoded_query = quote(query)
                search_url = f"https://www.googleapis.com/customsearch/v1?key=AIzaSyAuVDszlW7809n8JXeRQ_rgMy2wLvgb5rI&cx=158a408d737fc46f5&q={encoded_query}&searchType=image"
                response = urllib.request.urlopen(search_url)
                data = json.loads(response.read())
                # Get the URL of the first image result
                image_url = data["items"][0]["link"]
                image_data = urllib.request.urlopen(image_url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                self.ui.debug.setPixmap(pixmap)
            except Exception as e:
                self.ui.debug.setText(f"Error: {str(e)}")
        else:
            self.ui.debug.setText("Please enter a search query.")

    def manualCodeFromTerminal(self):
        cmd = self.ui.input.text()
        if cmd:
            self.ui.input.clear()
            self.ui.output.appendPlainText(
                f"you Just Typed >>> {cmd}")
            if cmd == 'exit':
                self.close()
            elif cmd == 'help':
                speak(
                    "I can do anythings"
                )
            elif 'start' in cmd:
                command()
            elif 'create' in cmd:
                str1 = cmd.replace("kimi ", "")
                query = str1.replace("create ", "")
                speak("Please say the question.")
                question = listen()
                speak("Please say the answer.")
                answer = listen()
                if question and answer:
                    create_task(question, answer)

            elif '' in cmd:
                str1 = cmd.replace("kimi ", "")
                query = str1.replace("hey ", "")
                answer = get_answer(query)
                if answer:
                    talk(f"{answer}.")
            elif 'question' in cmd:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=cmd,
                    temperature=0.5,
                    max_tokens=60,
                    top_p=0.3,
                    frequency_penalty=0.5,
                    presence_penalty=0,
                )
                if response.choices:
                    answer = response.choices[0].text.strip()
                    speak(answer)
                else:
                    return "I'm sorry, but I don't have an answer to that question."

    def setup_audio(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,
                                      frames_per_buffer=1024)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            x = event.globalX() - self.offset.x()
            y = event.globalY() - self.offset.y()
            self.move(x, y)

    def terminalPrint(self, text):
        self.ui.output.appendPlainText(text)

    def camera_frame(self):
        ret, frame = self.camera.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame_rgb.shape
            image = QImage(frame_rgb.data, width, height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.ui.cam.setPixmap(pixmap)
            self.ui.cam.setScaledContents(True)

    def speak_frame(self):
        frame = self.avatar_image.copy()
        current_time = time.time()
        if current_time - self.last_blink_time >= self.blink_interval:
            frame[self.eye_y:self.eye_y + self.eye_open.shape[0],
                  self.eye_x:self.eye_x + self.eye_open.shape[1]] = self.eye_close
            if current_time - self.last_blink_time >= self.blink_interval + self.blink_duration:
                self.last_blink_time = current_time
        else:
            frame[self.eye_y:self.eye_y + self.eye_open.shape[0],
                  self.eye_x:self.eye_x + self.eye_open.shape[1]] = self.eye_open

        audio_data = self.stream.read(1024, exception_on_overflow=False)
        rms = audioop.rms(audio_data, 2)

        if rms > self.audio_threshold:
            frame[self.mouth_y:self.mouth_y + self.mouth_open.shape[0],
                  self.mouth_x:self.mouth_x + self.mouth_open.shape[1]] = self.mouth_open
        else:
            frame[self.mouth_y:self.mouth_y + self.mouth_close.shape[0],
                  self.mouth_x:self.mouth_x + self.mouth_close.shape[1]] = self.mouth_close

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h,
                         bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.ui.avatar.setPixmap(pixmap)

    def closeEvent(self, event):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.camera.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.timer = QTimer()
    window.timer.timeout.connect(window.speak_frame)
    window.timer.start(1)
    sys.exit(app.exec_())
else:
    print(__name__, "Running...")
