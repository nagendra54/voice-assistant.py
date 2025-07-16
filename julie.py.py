import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import os
import sys
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='wikipedia')

genai.configure(api_key="") 
model = genai.GenerativeModel('models/gemini-2.5-pro')


# Initialize TTS engine
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
try:
    engine.setProperty('voice', voices[1].id)
except IndexError:
    engine.setProperty('voice', voices[0].id)

def talk(text):
    print("🎙️ JULIE:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    listener = sr.Recognizer()
    talk("🎧 Listening...")
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        voice = listener.listen(source)
    try:
        command = listener.recognize_google(voice)
        command = command.lower()
        print("🗣️ You said:", command)
    except sr.UnknownValueError:
        talk("Sorry bro, I didn’t catch that.")
        return ""
    except sr.RequestError:
        talk("Network issue with Google service.")
        return ""
    return command

def ask_gemini(query):
    try:
        response = model.generate_content(query)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {str(e)}"


def run_julie():
    command = take_command()
    if not command:
        return

    if "play" in command:
        song = command.replace("play", "").strip()
        if song:
            engine.say(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)
        else:
            talk("You asked me to play something, but I didn’t catch the song name.")

    elif "time" in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"It’s {time} ⏰")

    elif "joke" in command:
        joke = pyjokes.get_joke()
        talk(joke)

    elif "who is" in command or "what is" in command or "tell me about" in command:
        topic = (
        command.replace("who is", "")
               .replace("what is", "")
               .replace("tell me about", "")
               .strip()
    )
        if topic:
            talk(f"Let me check about {topic} 🧠")
            reply = ask_gemini(f"{topic}")
            talk(reply)
        else:
            talk("I didn't catch the topic. Please say something like 'Tell me about Python'.")

    elif "open chrome" in command:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path):
            talk("Opening Chrome 🚀")
            os.startfile(chrome_path)
        else:
            talk("Chrome path not found 😬")

    elif "open code" in command or "open vs code" in command:
        engine.say("Opening VS Code 💻")
        os.system("code")

    elif "exit" in command or "stop" in command:
        talk("Okay bro, see you later 👋")
        sys.exit()

    else:
        talk("I heard you, but I don’t understand that yet 😅")

talk("Hii! I'm JULIE – your personal voice assistant...🤖")
while True:
    run_julie()
