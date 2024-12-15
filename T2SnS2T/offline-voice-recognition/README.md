# Real-Time Speech Recognition with Vosk and PyAudio

## Overview
This script demonstrates real-time speech recognition using the Vosk library for speech-to-text conversion and PyAudio for capturing audio from a microphone. The program listens to your speech and prints the recognized text in real-time. It stops when you say "stop."

## Prerequisites
1. Install the required libraries:
   ```
   pip install vosk PyAudio
   ```
2. Download the [Vosk model](https://alphacephei.com/vosk/models) and place it in the same directory as the script. Ensure the model path matches the code (e.g., ```./vosk-model-small-en-us-0.15```).

## Usage

1.  Ensure your microphone is connected and configured properly.
2.  Run the script:
```
python your_script_name.py
```
3.  Speak into your microphone. The recognized text will be printed in real-time.
4.  Say **"stop"** to exit the program.

## Notes
*   Replace ```input_device_index=1``` with the correct index of your microphone. Use the PyAudio API to list all available devices.
*   Ensure the sample rate (```rate=16000```) matches your microphone's capabilities.