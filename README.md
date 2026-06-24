# JARVIS - Voice Assistant with Biometric Authentication

A personal voice assistant built in Python that combines **speech recognition**, **text-to-speech**, and **voice biometric authentication**. Inspired by JARVIS from Iron Man, this assistant can perform useful tasks through natural voice commands while verifying the user's identity.

## Features

- **Voice Biometric Authentication**  
  Uses voice embeddings (`resemblyzer`) to verify the speaker before executing sensitive commands.

- **Voice Command Recognition**  
  Listens for commands using Google Speech Recognition and responds using text-to-speech.

- **Built-in Commands**
  - Create new project folders via voice
  - Tell the current time and date
  - Convert numbers to Roman numerals
  - Basic conversational responses

- **Modular Architecture**  
  Clean separation between speech recognition, voice authentication, and command execution modules.

## Tech Stack

- **Python 3.8+**
- `speech_recognition` – Speech-to-text (Google)
- `pyttsx3` – Offline text-to-speech
- `resemblyzer` – Voice embeddings for speaker identification
- `pyaudio` – Audio input handling
- `numpy` – Numerical operations for voice comparison

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/jarvis-voice-assistant.git
   cd jarvis-voice-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional but recommended) Add your voice sample:
   - Record a short clear voice sample and generate an embedding.
   - Save it as `known_voices/your_name.npy`.

## Usage

Run the assistant:

```bash
python main.py
```

### Example Voice Commands

| Voice Command                         | Action                                      |
|---------------------------------------|---------------------------------------------|
| "What time is it?"                    | Tells current time and date                 |
| "Create a new folder called ProjectX" | Creates a folder named ProjectX             |
| "Convert 42 to Roman numerals"        | Returns "XLII"                              |
| "Who are you?"                        | Introduces itself                           |

> **Note**: Folder creation and other actions may require voice authentication depending on your setup.

## Project Structure

```
Virtual_Assistant/
├── main.py                 # Main command loop and logic
├── speech_module.py        # Speech recognition + Text-to-Speech
├── voice_auth.py           # Voice biometric verification using resemblyzer
├── known_voices/           # Folder containing .npy voice embeddings
│   └── aadhi.npy
├── utils/                  # Helper functions (Roman numerals, folder creation, etc.)
├── requirements.txt
└── README.md
```

## How It Works

1. The assistant continuously listens using `speech_recognition`.
2. When speech is detected, it transcribes the command.
3. If the command requires authentication, it records a short voice sample and compares the embedding against the stored reference using `resemblyzer` + cosine similarity.
4. If authentication passes (or is not needed), the command is executed.
5. The assistant responds using `pyttsx3`.
