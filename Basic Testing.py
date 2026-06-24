from datetime import datetime, time, date
text_input = input("")
time_phrases = ["What is the time?", "What time is it?", "Do you know what the time is?", "Tell me the time",
                "Could you tell me the time?", "Can you tell me the time?", "Give me the time", "I need the time",
                "Time, please", "Show me the time"
            ]
for phrase in time_phrases:
    if phrase in text_input:
        time = datetime.now().strftime("%H:%M")
        print(f"The current time is {time}")
                
