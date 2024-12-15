import pyttsx3


class Text2Speech:
    
    def __init__(swayam, driverName= None):
        swayam.engine= pyttsx3.init(driverName= 'sapi5')
        
        swayam.rate=  swayam.engine.getProperty("rate")
        swayam.voices= swayam.engine.getProperty('voices')
        swayam.volume = swayam.engine.getProperty('volume')
        
        swayam.engine.setProperty('volume', swayam.volume-0)
        swayam.engine.setProperty('rate',125)
        swayam.engine.setProperty('voice', swayam.voices[0].id)
    
        
    
    def say(swayam, text2Speack: str):
        swayam.engine.say(text2Speack)
        swayam.engine.runAndWait()
        swayam.engine.stop()
        

