import speech_recognition as sr


class Voice2Text:
    
    """
    A class for converting voice input to text using the SpeechRecognition library.

    Attributes:
        vt: The SpeechRecognition Recognizer instance for voice-to-text conversion.
        source: The microphone source for capturing audio.
    """
    
    def __init__(swayam):
        
        """
        Initializes the Voice2Text instance with a microphone source.
        """
        
        swayam.vt = sr.Recognizer()
        swayam.vt.energy_threshold= 300
        swayam.source= sr.Microphone()
            
        
    def listen(swayam, duration: int= 1, timeout: int= 5, phrase_time_limit= 5) -> dict: 
        """
        Listens to the microphone input and converts it to text.

        Args:
            duration (int): Time in seconds to adjust for ambient noise. Default is 1 second.
            timeout (int): Maximum time to wait for speech input. Default is 5 seconds.
            phrase_time_limit (int): Maximum duration for speech input. Default is 5 seconds.

        Returns:
            dict: A dictionary with the following keys:
                - 'status' (bool): True if the conversion was successful, False otherwise.
                - 'text' (str): The converted text or error message.
        """
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
            