import speech_recognition as sr



r = sr.Recognizer()
r.energy_threshold = 300 # Optional: Adjust the energy threshold based on ambient noise levels


with sr.Microphone() as source:
    while True:
        r.adjust_for_ambient_noise(source, duration=1)
        audio_text = r.listen(source, timeout=20, phrase_time_limit=10 )
        try:
            print("Processing...")
            text = r.recognize_google(audio_text)
            print("Text: " + text)
                    
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except sr.UnknownValueError:
            # Speech was unintelligible
            print("Google Speech Recognition could not understand the audio")
        except Exception as e:
            print(f"Error: {str(e)}")