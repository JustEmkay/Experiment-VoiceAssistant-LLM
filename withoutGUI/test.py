import speech_recognition as sr
import pyttsx3
import time
# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()
r.energy_threshold = 300 # Optional: Adjust the energy threshold based on ambient noise levels

engine = pyttsx3.init(driverName= 'sapi5') #object creation
rate = engine.getProperty("rate")
engine.setProperty('rate',125)
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)  #changing index, changes voices. o for male

# Reading Microphone as source
with sr.Microphone() as source:
    print("Adjusting for ambient noise... Please wait.")
    r.adjust_for_ambient_noise(source, duration=1)

    while True:
    
        print("Talk now:")
        
        # Capture audio from the microphone
        try:
            audio_text = r.listen(source, phrase_time_limit=10)
            print("Processing...")
            text = r.recognize_google(audio_text)
            print("Text: " + text)
            if text == 'stop assist':
                break
            engine.say(text, str(rate))
            
            
            
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except sr.UnknownValueError:
            # Speech was unintelligible
            print("Google Speech Recognition could not understand the audio")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        finally:
            engine.runAndWait()    
            # engine.say("Command confirmed. Stopping assistance.")
    engine.stop()
       