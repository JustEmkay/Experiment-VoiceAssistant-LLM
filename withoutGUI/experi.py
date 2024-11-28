# Python Rich modules
from rich.console import Console
from rich.tree import Tree
from rich.live import Live
from rich.panel import Panel
from rich.theme import Theme
from rich import print
from rich.progress import track

# python default modules
from datetime import datetime
from time import sleep

# speach recognition modules
import speech_recognition as sr
import pyttsx3

# rich ui theme setup
custome_theme = Theme(
    {
        'info': 'bold cyan',
        'warning': 'red',
        'success': 'bold green'
    }
)

r = sr.Recognizer()
r.energy_threshold = 300

engine = pyttsx3.init() #object creation
rate = engine.getProperty("rate")
engine.setProperty('rate',125)
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id) 


class ChatTree:
    
    def __init__(self) -> list:
        
        self.root = Tree(Panel('[bold]CHATBOT'))
        
        self.data = [
            { 'assistant' : ['How can i help you??','27-11-2024, 10:25:01'] },
            { 'user' : ["tell me today's date?",'27-11-2024, 10:25:01'] },
            { 'assistant' : ["Today is Thursday.", '28-11-2024'] },
        ]
    
    def add_user_prompt(self, prompt: str) -> None:
        userMsg = {'user': [prompt, datetime.now().strftime('%m/%d/%Y, %H:%M:%S')]}
        self.data.append(userMsg)
    
    def add_assistant_response(self, response: str) -> None:
        assistMsg = {'assistant': [response, datetime.now().strftime('%m/%d/%Y, %H:%M:%S')]}
        self.data.append(assistMsg)
        
    def add_error_response(self, errorMSg: str) -> None:
        errorMsg = {'error': [errorMSg, datetime.now().strftime('%m/%d/%Y, %H:%M:%S')]}
        self.data.append(errorMsg)
        
           
    
        
    def build_tree(self):
        
        root = Tree(Panel('[bold]CHATBOT'))
        for chat in self.data[-6:]:
            for key, message in chat.items():
                
                if key == 'assistant':
                    color = "[bold red]"
                elif key == 'user':
                    color = "[bold green]"
                elif key == 'error':
                    color = '[bold grey0]'
                                    
                branch = root.add(f"{color}{key}")
                branch.add(
                    Panel(
                        f"{message[0]}",
                        subtitle=f"{message[1]}",
                        subtitle_align='right'
                        ))
                
                if key == 'assistant':
                    branch.add(
                        '[grey]Talk now'
                    )
        
        root.add(Panel("[bold]END OF CHAT"))
        
        return root
        
    

def main() -> None:
    
    console = Console()
    chat_tree = ChatTree()



    # with sr.Microphone() as source:
        # for i in track(range(5), description="Adjusting for ambient noise..."):
        #     sleep(1)
        # r.adjust_for_ambient_noise(source, duration=1)       
        # Use Live to dynamically update the tree in real-time

    with Live(console=console, auto_refresh= True) as live:

        
        while True:
            
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)      
                chat_tree.add_assistant_response(response= 'How can i helo you?')
                audio_text = r.listen(source, timeout=10, phrase_time_limit=10)
                live.update(chat_tree.build_tree())
                
                try:
                    text = r.recognize_google(audio_text)
                    # print("Text: " + text)
                    if text == 'stop assist':
                        engine.say("Command confirmed. Stopping assistance.")
                        break
                    
                    chat_tree.add_user_prompt(prompt= text)
                    engine.say(text)
                    live.update(chat_tree.build_tree())
                    
                    
                    
                except sr.RequestError as e:
                    # API was unreachable or unresponsive
                    error= f"Could not request results from Google Speech Recognition service; {e}"
                    chat_tree.add_error_response(errorMSg= error)
                    
                except sr.UnknownValueError:
                    # Speech was unintelligible
                    error= "Google Speech Recognition could not understand the audio"
                    chat_tree.add_error_response(errorMSg= error)
                
                except Exception as e:
                    chat_tree.add_error_response(errorMSg= f"Error: {str(e)}")
                    
                engine.runAndWait()
                engine.stop()
        
        


if __name__ == '__main__':
    main()