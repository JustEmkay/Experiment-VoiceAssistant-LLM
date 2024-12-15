import pyttsx3
import speech_recognition as sr
from typing import Literal




class Text2Speech:
    
    def __init__(swayam, voiceStyle: Literal[0,1] = 0):
        swayam.engine= pyttsx3.init(driverName= 'sapi5')
        
        swayam.rate=  swayam.engine.getProperty("rate")
        swayam.voices= swayam.engine.getProperty('voices')
        swayam.volume = swayam.engine.getProperty('volume')
        
        swayam.engine.setProperty('volume', swayam.volume-0)
        swayam.engine.setProperty('rate',125)
        swayam.engine.setProperty('voice', swayam.voices[voiceStyle].id)
    
        
    
    def say(swayam, text2Speack: str):

        swayam.engine.say(text2Speack)
        swayam.engine.runAndWait()
        swayam.engine.stop()
        

class Voice2Text:
    
    def __init__(swayam):
        
        swayam.vt = sr.Recognizer()
        swayam.vt.energy_threshold= 300
        swayam.source= sr.Microphone()
            
        
    def listen(swayam, duration: int= 1, timeout: int= 5, phrase_time_limit= 5) -> dict: 
        
        with swayam.source:
            swayam.vt.adjust_for_ambient_noise(swayam.source, duration= duration)
            print("Say something!")
            audio_text= swayam.vt.listen(swayam.source,
                                        timeout= timeout,
                                        phrase_time_limit= phrase_time_limit)
            
            try:
                print("Processing...")
                text = swayam.vt.recognize_google(audio_text)
                print("Text: " + text)
                return {
                    'status': True,
                    'text': text
                }
                        
            except sr.RequestError as e:
                # API was unreachable or unresponsive
                error= f"Could not request results from Google Speech Recognition service; {e}"
                
            except sr.UnknownValueError:
                # Speech was unintelligible
                error= "Google Speech Recognition could not understand the audio"
            
            except Exception as e:
                error= f"Error: {str(e)}"
                
            return {
                'status': False,
                'text': error
            }
            
            
            
def test()-> None:
    
    t2p = Text2Speech()
    v2t = Voice2Text()
    
    hear= v2t.listen()
    if hear['status']:
        t2p.say(hear['text'])
        
    
    
    
if __name__ == '__main__':
    test()
    