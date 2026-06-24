import speech_module as sm
import folder_creator as fc
import utils
import re
import random
from datetime import datetime
import string
import voice_auth

idle_responses = [
    "I am awaiting your command, sir.",
    "Standing by.",
    "Take your time, sir.",
    "I am here whenever you are ready."
]

Wake_Words = ["hey jarvis", "jarvis", "wake up jarvis"]

def is_wake_word(text):
    return any(phrase in text for phrase in Wake_Words)

def format_folder_name(raw_name):
    cleaned_name = re.sub(r'[\/:*?"<>|]', '', raw_name)
    words = cleaned_name.split()
    final_words = []
    for word in words:
        if word.isdigit():
            roman = utils.int_to_roman(int(word))
            final_words.append(roman.upper())
        else:
            final_words.append(word.capitalize())
    return " ".join(final_words)

def create_folder_command(command_text):
    if "create a project file" in command_text or "project file" in command_text:
        if "index as" in command_text:
            words = command_text.split("index as")
            folder_name = words[1].strip()
        else:
            sm.SpeakText("What should I name the project, sir?")
            folder_name_response = sm.listen_for_command()
            if folder_name_response:
                folder_name = folder_name_response.strip()
            else:
                sm.SpeakText("Sorry, I did not catch the project name.")
                return
        formatted_folder_name = format_folder_name(folder_name)
        sm.SpeakText(f"Did you say to create the folder '{formatted_folder_name}'? Please say Yes or No.")
        confirmation = sm.listen_for_command()
        if confirmation and "yes" in confirmation.lower():
            print(f"Creating folder: {formatted_folder_name}")
            fc.create_project_folder(formatted_folder_name)
            sm.SpeakText(f"Sir, I have created your new project folder: '{formatted_folder_name}'")
        else:
            sm.SpeakText("Understood, I will not create the folder.")

    elif "convert" in command_text and "roman" in command_text:
        num_str = command_text.split("convert")[1].strip()
        try:
            num = int(num_str)
            roman = utils.int_to_roman(num)
            sm.SpeakText(f"The Roman numeral for {num} is {roman}.")
        except ValueError:
            sm.SpeakText("Sorry, I couldn't understand the number.")

def asking_for_time(command_text):
    command_text = command_text.lower().translate(str.maketrans('', '', string.punctuation))
    time_phrases = [
        "what is the time", "what time is it", "do you know what the time is", "tell me the time",
        "could you tell me the time", "can you tell me the time", "give me the time",
        "i need the time", "time please", "show me the time"
    ]
    for phrase in time_phrases:
        if phrase in command_text:
            current_time = datetime.now().strftime("%H:%M")
            sm.SpeakText(f"The current time is {current_time}")
            return True
    return False

# ------------------ MAIN LOOP ------------------
while True:
    print("Hello")
    command_text = sm.listen_for_command()
    print("Heard command:", command_text)

    if command_text:
        if is_wake_word(command_text):
            sm.SpeakText("Voice Authentication in progress...")
            voice_path = voice_auth.record_voice()
            new_embed = voice_auth.get_embedding(voice_path)
            known_embeds = voice_auth.load_known_embeddings()
            identified_name = voice_auth.identify_speaker(new_embed, known_embeds)

            if identified_name == "aadhi":
                sm.SpeakText("Yes sir, how may I help you?")
                command_text = sm.listen_for_command()
                if command_text:
                    if not asking_for_time(command_text):
                        create_folder_command(command_text)
                else:
                    sm.SpeakText("Sorry, I didn’t catch your command.")
            
            elif identified_name is not None:
                sm.SpeakText(f"Welcome back, {identified_name}. How may I help you?")
                command_text = sm.listen_for_command()
                if command_text:
                    if not asking_for_time(command_text):
                        create_folder_command(command_text)
                else:
                    sm.SpeakText("Sorry, I didn’t catch your command.")

            else:
                sm.SpeakText("New voice recognized, should I authenticate this sir?")
                confirmation = sm.listen_for_command()
                if confirmation and "yes" in confirmation.lower():
                    sm.SpeakText("Please state your name.")
                    name_response = sm.listen_for_command()
                    print("State your name")
                    if name_response:
                        name = name_response.strip()
                        sm.SpeakText(f"Is this your name? {name}")
                        name_confirm = sm.listen_for_command()
                        if name_confirm and "yes" in name_confirm.lower():
                            voice_auth.save_new_user(name, new_embed)
                            sm.SpeakText(f"{name} has been added. Creating a folder for you now.")
                            formatted_name = format_folder_name(name)
                            fc.create_project_folder(formatted_name)
                        else:
                            sm.SpeakText("Name confirmation failed. Cancelling authentication.")
                    else:
                        sm.SpeakText("No name received. Cancelling authentication.")
                else:
                    sm.SpeakText("Authentication denied.")
        else:
            print("Wake word not detected. Listening again...")
    else:
        random_idle = random.choice(idle_responses)
        sm.SpeakText(random_idle)
