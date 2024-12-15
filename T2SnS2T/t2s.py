import pyttsx3
from typing import Literal

class Text2Speech:
    
    """
    A class for converting text to speech using the pyttsx3 library.

    Attributes:
        engine: The pyttsx3 engine instance for text-to-speech conversion.
        rate: The speech rate of the engine.
        voices: List of available voices.
        volume: The volume level of the engine.
    """
    
    def __init__(swayam, voiceStyle: Literal[0,1] = 0):
        
        """Initializes the Text2Speech engine with the specified voice style.

        Args:
            voiceStyle (Literal[0,1]): Selects the voice style (0 for male, 1 for female).
        """  
        swayam.engine= pyttsx3.init(driverName= 'sapi5')
        
        swayam.rate=  swayam.engine.getProperty("rate")
        swayam.voices= swayam.engine.getProperty('voices')
        swayam.volume = swayam.engine.getProperty('volume')
        
        swayam.engine.setProperty('volume', swayam.volume-0)
        swayam.engine.setProperty('rate',125)
        swayam.engine.setProperty('voice', swayam.voices[voiceStyle].id)
    
        
    
    def say(swayam, text2Speack: str):
        """
        Converts the given text to speech and plays it.

        Args:
            text2Speack (str): The text to be spoken.
        """
        swayam.engine.say(text2Speack)
        swayam.engine.runAndWait()
        swayam.engine.stop()
        