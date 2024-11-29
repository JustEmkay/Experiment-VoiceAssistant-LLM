import pyttsx3

# Initialize pyttsx3 TTS engine
speaker = pyttsx3.init('sapi5')
speaker.setProperty('rate', 120)  # Set speaking rate
voices = speaker.getProperty('voices')  # Get available voices
# Uncomment below line to use a different voice (e.g., female)
speaker.setProperty('voice', voices[1].id)


def speak(text):
    """
    Speak the given text using pyttsx3.
    """
    print("You typed:", text)
    speaker.say(text)
    speaker.isBusy()
    # speaker.runAndWait()  # Ensure the TTS engine finishes speaking


# Main loop
while True:
    if not speaker.runAndWait():  # Ensure the TTS engine finishes speaking
        user_input: str = input("User: ")  # Get user input
        if user_input.lower() == 'stop':  # Check for exit condition
            speak("Exiting program")
            break
        speak(user_input)  # Speak the user's input
