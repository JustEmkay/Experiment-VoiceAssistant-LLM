# Text-to-Speech and Voice-to-Text Utility

## Project Overview  
This Python script provides two simple and beginner-friendly classes, `Text2Speech` and `Voice2Text`, for converting text to speech and recognizing voice input. It is a great starting point for developers interested in voice assistant features or natural language processing.

---

## Features  
- Text-to-Speech conversion with support for switching between male and female voices.  
- Voice-to-Text recognition using Google's Speech Recognition API.  
- Adjustable configurations like speech rate, duration, and timeout for customization.  

## Setup Instructions  

### 1. Install Required Libraries  
Run the following command to install the dependencies:  
```
pip install pyttsx3 SpeechRecognition
```

### 2. TTS Driver Installation
Ensure you have the appropriate TTS driver installed for your operating system:

*   Windows: Install sapi5 (default for pyttsx3).
*   macOS: Use the nsss driver.
*   Linux: Install espeak (via your package manager, e.g., sudo apt install espeak).

### 3. Change the TTS Driver
To explicitly set the TTS driver in your script, modify the pyttsx3.init call:
```
import pyttsx3

engine = pyttsx3.init(driverName='espeak')  # Change to 'nsss' for macOS or 'sapi5' for Windows
```

### 4. Microphone Configuration
Ensure that your microphone is connected and working correctly.

---
## Usage

### 1. Text2Speech
Convert text to speech:

```
from your_script import Text2Speech

# Create a Text2Speech instance
tts = Text2Speech(voiceStyle=1)  # Use 0 for male, 1 for female voice

# Speak the text
tts.say("Hello, world!")

```

### 2. Voice2Text
Convert voice input to text:
```
from your_script import Voice2Text

# Create a Voice2Text instance
v2t = Voice2Text()

# Listen to the microphone and get the text
result = v2t.listen(duration=2, timeout=5, phrase_time_limit=10)
if result['status']:
    print("Recognized Text:", result['text'])
else:
    print("Error:", result['text'])

```

### 3. Dependencies
*   **pyttsx3**: For Text-to-Speech.
*   **SpeechRecognition**: For Voice-to-Text.

Install them using:
```
pip install pyttsx3 SpeechRecognition
```

### Notes
*   Ensure that your system has the appropriate TTS driver installed.
*   Background noise can affect the accuracy of speech recognition.