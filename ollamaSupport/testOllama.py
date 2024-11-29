from ollamaModule import *
from time import sleep

from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
from rich.theme import Theme
from rich import print
from rich.progress import track
from rich.prompt import Prompt
from rich.rule import Rule


custome_theme = Theme(
    {
        'info': 'bold cyan',
        'warning': 'red',
        'success': 'bold green'
    }
)


class llmOptions:
    
    def __init__(self) -> None:
        self.username : str = 'Manu'
        self.model_name : str = "llama3.2:1b " 
        self.memory : list[dict[str,str]] = []
        self.systemSettings : dict[str,str] = {}
        self.models : list = None


    def New_llmSettings(self, console) -> None:
        if not self.username and not self.model_name:
            
            NewSettings : bool = True
            
            while NewSettings:
                console.clear()
                print(Rule(title='Set Username and LLM model', style='white'))
                username = Prompt.ask('[cyan]Enter username[/cyan]')
                print( Panel(f"username set as [bold green]{username}",) )
                sleep(2)
                console.clear()
                markdown = ''
                for idx, model in enumerate(self.models, start=1):
                    markdown += f''' {idx}. {model} \n'''
                    
                print( Panel(markdown,title='[bold cyan]Model List') )
                modelnumber = Prompt.ask('Enter respective model number',
                                   choices=[ str(i) for i in range(1,len(self.models)+1)])
                
                model_name : str = self.models[int(modelnumber)-1]
                print(Panel(f"You selected [bold green]{model_name}[/bold green] as your LLM"))
                print(Rule())
                
                markdown = ''
                markdown += f'* [bold cyan]Username:[/bold cyan] [bold green]{username}[/bold green]\n'
                markdown += f'* [bold cyan]Model:[/bold cyan] [bold green]{model_name}'
    
                print( Panel(f"{markdown}",
                             title='[bold cyan]New Settings'))
                print( Panel(f"1.Ok\n2.Reset\n3.Cancel",))
                
                confirm = str(Prompt.ask( "Continue with these settings?",
                                 choices=['1','2','3']))
                
                if confirm == '1': #OK
                    self.model_name = model_name
                    self.username = username
                    print( '[bold cyan]Info:[/bold cyan] [green]Saving settings..' )
                    sleep(1)
                    NewSettings = False
                
                elif confirm == '2': #Reset
                    print( '[bold cyan]Info:[/bold cyan] Reseting Everything.' )
                    sleep(1)
                    continue
                
                elif confirm == '3': #Cancel
                    break
                  
    def llmsettings(self, console) -> None:
        self.New_llmSettings(console=console)
        
        console.clear()
        print(Panel(f"Username: {self.username}\nModel Name: {self.model_name}",
                    title='[bold cyan]User Settings',
                    title_align='left'))
        print(input('press enter to continues...'))

    def ChatwithLLM(self, console) -> None:
        
        self.New_llmSettings(console)
        
        if self.username and self.model_name:
            console.clear()
            modelnumber = Prompt.ask('chat',)
        
        
        
        


    def insert_response(self, response) -> None:
        
        self.memory.append({
            'role': 'assistant',
            'content': response
        })

    def insert_prompt(self, response) -> None:
        
        self.memory.append({
            'role': 'user',
            'content': response
        })

    def get_response():
        pass


    


def main() -> None:
    console = Console()
    llm = llmOptions()
    
    llmStatus = ollamaStatus()
    if llmStatus['status']:
        if llmStatus['models']:
            llm.models = llmStatus['models']
            
            console.print( "[bold green]Ollama running successfully[/bold green]" )
            sleep(1)
            while True:
                
                console.clear()
                
                
                console.print(Panel( "[bold red]Test ollama[/bold red] \
                            \n1. Chat with LLM \
                            \n2. Check stastus \
                            \n3. Settings      \
                            \n4. Exit()" ))
                option= input("Enter your option: ")

                if option == "1":
                    llm.ChatwithLLM(console= console)
                    
                elif option == "2":
                    print("---")
                    console.log(ollamaStatus()['models'])
                    input('press enter to continue..')
                
                elif option == "3":
                    llm.llmsettings(console= console)
                
                elif option == "4":
                    print("[bold cyan]info[/bold cyan] [bold italic yellow]Exiting the program.... ")
                    sleep(1)
                    break
                else:
                    console.log('Wrong option... ')
                    sleep(1)

        else:
            print(f'[bold orange]:warning: No Models Installed [/bold red]')        
                
    
    else:
        print(f"[bold red]:skull:{llmStatus['msg']}[/bold red]")        
            
            
    
if __name__ == "__main__":
    main()