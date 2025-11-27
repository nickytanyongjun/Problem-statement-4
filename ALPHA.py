import speech_recognition as sr
import pyttsx3
import requests
import datetime
import webbrowser
import pyaudio
import pyautogui
import keyboard
import os
import time


recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
tts = pyttsx3.init()
tts.setProperty('rate', 200)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

WAKE_WORD = "hey alpha" or "hit alpha" or "pete alpha" or "alpha" or "alfa"


print("       ____      ___            ________        ____  ____             _____")
print("      /    |     |  |           |  ____ \       |  |  |  |            /    |")
print("     / ___ |     |  |           |  |  |  |      |  |  |  |           / ___ |")
print("    /  | | |     |  |           |  _____/       |  |__|  |          /  | | |")
print("   /  ____ |     |  |           | |             |  ____  |         /  ____ |")
print("  /  /   | |     |  |           | |             |  |  |  |        /  /   | |")
print(" /  /    | |     |  |_____      | |             |  |  |  |       /  /    | |")
print("/__/     |_| ()  |_______|  ()  |_|         ()  |_ |  |_ |  ()  /__/     |_|")

print("please enter your username")
name = input("username :")

correct = name == "nicky"


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning " + name)
    if hour>=12 and hour<18:
        speak("Good Afternoon " + name)
    if hour>=18 and hour<24:
        speak("Good Evening " + name)
    speak("how can i help you")


def speak(text):
    print("ALPHA:\n", text)
    tts.say(text)
    tts.runAndWait()


def listen_for_wake_word():
    print("Hold Ctrl + t to talk... release to stop.")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio_data = None

        while True:
            if keyboard.is_pressed("ctrl+t"):
                speak("Listening")
                try:
                    audio_data = recognizer.listen(source, phrase_time_limit=10) 
                except Exception as e:
                    speak("Error while listening:", e)
                    return None
                
                if not keyboard.is_pressed("ctrl+t"):
                    speak("stopped listening")
                    break
            else:
                continue

    if not audio_data:
        return None

    try:
        query = recognizer.recognize_google(audio_data).lower() 
        print(name + ":", query)

        
        if "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {strTime}")

        if "youtube" in query:
            webbrowser.open("https://www.youtube.com/")
            speak(query)

        if 'spam' in query:
            email = input("paste your email here: ")
            if "#1" in email or "100% more" in query:
                print("spam")
            else:
                print("not spam")

        if 'repeat' in query:
            msg = input("paste it here :")
            speak(msg)

        if 'my bedroom light' in query:
            pyautogui.press("winleft")
            time.sleep(0.5)
            pyautogui.typewrite("smartthings", interval=0.001)
            pyautogui.press("enter")
            time.sleep(2)
            pyautogui.click(x=363, y=215)
            print (query)
                
        if 'laptop' in query:
            pyautogui.press("winleft")
            time.sleep(0.5)
            pyautogui.typewrite("smartthings", interval=0.001)
            pyautogui.press("enter")
            time.sleep(2)
            pyautogui.click(x=733, y=220)
            speak(query)
                
        
 

        if WAKE_WORD in query:
            cleaned_query = query.replace(WAKE_WORD, '').strip()
            return cleaned_query if cleaned_query else None
        else:
            return None

    except sr.UnknownValueError:
        speak("could not understand audio")
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        speak("speech recognition error")
        print(f"Speech recognition error: {e}")
        return None


def talk_to_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt + (" in short"),
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            print("ALPHA error:", response.text)
            return "Something went wrong talking to ALPHA."
    except Exception as e:
        print("Request failed:", e)
        return "Failed to reach ALPHA."


# Main
if __name__ == "__main__":
    wishMe()
    print("Say 'Alpha' to begin. Hold Ctrl + T to activate mic.")
    while True:
        user_input = listen_for_wake_word()
        if user_input:
            if user_input in ["exit", "quit", "stop"]:
                speak("Goodbye!")
                break
            response = talk_to_ollama(user_input)
            speak(response)
