import speech_recognition as sr
import pyttsx3 # may use tensorflowtts
import pyautogui
import webbrowser
import pywhatkit
import datetime
import wikipedia
import pyjokes

class Assistant:
    # variables
    start_phrase = "tracer"
    stop_phrase = "go to sleep"
    recognizer = sr.Recognizer()

    # Setup Speak Engine
    speak_engine = pyttsx3.init()

    def __init__(self, name) -> None:
        self.start_phrase = name
        self.setup_speak_engine()
        print("Successfully initialized new Assistant")

    def setup_speak_engine(self):
        self.speak_engine.setProperty('rate', 150)
        self.speak_engine.setProperty('volume', 1.0)
        voices = self.speak_engine.getProperty('voices')
        self.speak_engine.setProperty('voice', voices[0].id)

    # Access Microphone and get audio file in format of mp3
    def listen(self):
        microphone = sr.Microphone()
        with microphone as source:
            print("listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
            audio = self.recognizer.listen(source)
        return audio

    # Input audio and get text
    def speech_to_text(self, audio) -> str:
        try:
            text = self.recognizer.recognize_google(audio)
            # print(text)
        except sr.UnknownValueError:
            text = "unrecognizable"
            # print("Unknown value")
        return text.lower()

    # Input text into chatGPT or my own large language model and return response
    def get_response(self, text) -> str:
        print()

    # Input text and repeat the text
    def text_to_speech(self, text) -> None:
        self.speak_engine.say(text)
        self.speak_engine.runAndWait()
        self.speak_engine.stop()

    # Just to make the code easier to read
    def respond(self, text):
        self.text_to_speech(text)

    # Run the assistant
    def start(self) -> None:
        active = True

        self.respond("Hello, I am " + self.start_phrase + ", your personal assistant")
        self.respond("For privacy reasons, I will not be able to listen to your commands unless you say my activation phrase. hey " + self.start_phrase + ".")
        
        listeningToTask = False
        tasks = []

        while active:

            audio = self.listen()
            command = self.speech_to_text(audio)
    
            if self.start_phrase in command or listeningToTask:

                # Basic tasks I would use it for
                if listeningToTask:
                    tasks.append(command)
                    listeningToTask = False
                    if (str(len(tasks)) == 1):
                        task = 'task'
                    else:
                        task = 'tasks'
                    self.respond("I have added" + command + " to your to do list. You currently have " + str(len(tasks)) + task + " in your list.")

                elif "add a task" in command:
                    self.respond("Sure, what is the task?")
                    listeningToTask = True
                
                elif "whats in my to do list" in command:
                    self.respond("Your to do list is: ")
                    for task in tasks:
                        self.respond(task)

                elif "reset my to do list" in command:
                    self.respond("I have reset your todo list")
                    tasks = []

                elif "take a screenshot" in command:
                    pyautogui.screenshot('screenshot.png')
                    self.respond("I took a screenshot for you.")

                elif "open" in command and ("chrome" in command or "tab" in command):
                    self.respond("Opening Chrome.")
                    webbrowser.open('https://www.google.com/')

                elif "play" in command:
                    song = command.replace("hey", "")
                    song = song.replace("tracer", "")
                    song = song.replace("play", "")
                    self.respond("Playing " + song + " on Youtube.")
                    pywhatkit.playonyt(song)

                elif "time" in command:
                    time = datetime.datetime.now().strftime("%I:%M %p")
                    self.respond("It is currently " + time)

                elif "who is" or "what is" or "define" in command:
                    question = command.replace("who is", "")
                    question = question.replace("what is", "")
                    question = question.replace("define", "")
                    question = question.replace("tracer", "")
                    question = question.replace("hey", "")
                    info = wikipedia.summary(question)
                    self.respond(info)

                elif "joke" in command:
                    self.respond(pyjokes.get_joke())

                elif self.stop_phrase in command:
                    active = False
                    self.respond("Understood. I hope I was of assistance. Have a great rest of your day!")

                else:
                    self.respond("I have no response to that command at the moment.")
                    # print("recognized")


tracer = Assistant("tracer")
tracer.start()
