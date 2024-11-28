from rich.console import Console
from rich.tree import Tree
from rich.live import Live
from time import sleep
from rich.panel import Panel
from rich import print
from rich.theme import Theme

from datetime import datetime

# rich ui theme setup
custome_theme = Theme(
    {
        'info': 'bold cyan',
        'warning': 'red',
        'success': 'bold green'
    }
)


class ChatTree:
    
    def __init__(self) -> list:
        self.data = [
            { 'assistant' : ['How can i help you??','27-11-2024, 10:25:01'] },
            { 'user' : ["tell me today's date?",'27-11-2024, 10:25:01'] },
            { 'assistant' : ["Today is Thursday.", '28-11-2024'] },
        ]
    
    def add_user_prompt(self, prompt: str) -> None:
        dictry = {'user': [prompt, datetime.now().strftime('%m/%d/%Y, %H:%M:%S')]}
        self.data.append(dictry)
    
    def add_assistant_response(self, response: str) -> None:
        dictry = {'assistant': [response, datetime.now().strftime('%m/%d/%Y, %H:%M:%S')]}
        self.data.append(dictry)
        
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
        
        root.add(Panel("[bold]END OF CHAT"))
        
        return root
        
    

def main() -> None:
    
    console = Console()
    chat_tree = ChatTree()

    # Use Live to dynamically update the tree in real-time
    with Live(console=console, refresh_per_second=4) as live:
        while True:
            
            chat_tree.add_user_prompt(prompt= 'thats cool')
            
            live.update(chat_tree.build_tree())
            sleep(2)
            
            chat_tree.add_assistant_response(response= 'do you want to knwo any thing else')
            
            live.update(chat_tree.build_tree())
            
    


if __name__ == '__main__':
    main()