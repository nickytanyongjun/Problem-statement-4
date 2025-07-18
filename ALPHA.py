import speech_recognition as sr
import pyttsx3
import requests
import datetime
import webbrowser
import pyaudio


recognizer = sr.Recognizer()
tts = pyttsx3.init()
tts.setProperty('rate', 250)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"  

WAKE_WORD = "hey alpha" or "hit alpha" or "pete alpha" or "pet alpha"
wakeword = "alpha"

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
    with sr.Microphone() as source:
        print("Listening for wake word...")
        audio = recognizer.listen(source)

        

    try:
        query = recognizer.recognize_google(audio).lower()
        print(name +":", query)

        #normal tesk
        
        if wakeword in query: 
            if "time"in query or "what's the time" in query or "what is the time" in query  :
                 strTime = datetime.datetime.now().strftime("%H:%M")    
                 print(f"The time is {strTime}")
                 speak(f"The time is {strTime}")
                 
            if "youtube" in query:
                webbrowser.open("https://www.youtube.com/")
                print("opening youtube")
                speak("opening youtube")
        

            if "new tab" in query:
                webbrowser.open("www.google.com")
                print ("opening new tab")
                speak ("opening new tab")

            if "sign algauage" in query:
                webbrowser.open ("https://sign.mt/")
                



            if 'review' in query:
                speak("yes just paste the review content here and i will try to analyse and determine its real or fake but do note that this is analysis is base off my data and its not 100 percent accuarte")
                print("yes just paste the review content here and i will try to analyse and determine its real or fake but do note that this is analysis is base off my data and its not 100% accuarte")
                review = input("paste your email here: ")

                if "#1" or "100% more" or "Amazing customer service" or "best purchase ever" in review:
                    print("yes, the review given above could be a fake this is because it generate a sence of too good to be true ")
                    speak("yes, the review given above could be a fake this is because it generate a sence of too good to be true ")

                if "delicious" or "excellent" or "best ever" or "Highly recommendable product" or "Life changing experience" in review :
                    print("yes, the review given above could be a fake this is because the review is excessive prsising the product")
                    speak("yes, the review given above could be a fake this is because the review is excessive prsising the product")

                else:
                    print("it's a genuine review")
                    speak("it's a genuine review")
                    

        if WAKE_WORD in query:
            cleaned_query = query.replace(WAKE_WORD, '').strip()
            return cleaned_query if cleaned_query else None
        else:
            print("Wake word not detected.")
            return None

    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return None

def talk_to_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt + ("in one or two sentence and without using the symbol *"), 
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
    print("Say 'Alpha' to begin.")
    while True:
        user_input = listen_for_wake_word()
        if user_input:
            if user_input in ["exit", "quit", "stop"]:
                speak("Goodbye!")
                break
            response = talk_to_ollama(user_input)
            speak(response)
            
        