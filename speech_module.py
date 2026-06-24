import speech_recognition as sr
import pyttsx3
r = sr.Recognizer()
engine = pyttsx3.init()
def SpeakText(command):
    engine.say(command)
    engine.runAndWait()
def listen_for_command():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = r.listen(source, timeout=10, phrase_time_limit=30)
            command = r.recognize_google(audio)
            command = command.lower()
            print(f"Recognized: {command}")
            return command
    except sr.WaitTimeoutError:
        print("Listening timed out — no speech detected.")
        return None
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
