from rich.live import Live
from rich.console import Console
from rich.layout import Layout
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.emoji import Emoji

from time import sleep

todos = [
    {'task':'go for a run', 'status': True},
    {'task':'Run 5km min', 'status': True},
    {'task':'Say i love you to juhi', 'status': False},
    {'task':'go to store', 'status': False},
    {'task':'kill bill', 'status': True},
    ]

def generateTable(heading: str, status: bool)-> Table:
    
    table = Table(title= heading)
    
    table.add_column(header= 'No.')
    table.add_column(header= 'Task title')
    table.add_column(header= 'Status')
    
    for idx, todo in enumerate(todos):
        if todo['status'] == status:
            table.add_row(str(idx), todo['task'], f"{ ':thumbsup:' if todo['status'] else ':thumbsdown:' }")
        
    return table
    


def createLayout()-> Layout:
    
    layout= Layout()
    
    layout.split(
        Layout(name= 'header', size= 3),
        Layout(name= 'body'),
        Layout(name= 'footer', size= 3)
    )
    
    layout['header'].update(Panel("Header"))
    layout['footer'].update(Panel("Footer"))
    
    layout['body'].split_column(
        Layout(name= 'todoList'),
        Layout(name= 'create', size= 3)
    )
    
    layout['todoList'].split_row(
        Layout(name= 'Pending'),
        Layout(name= 'Completed')
    )
    
    layout['Pending'].update(generateTable(heading= 'Pending', status= False))
    layout['Completed'].update(generateTable(heading= 'Completed', status= True))
    
    return layout



def main():
    
    console= Console()
    
    layout = createLayout()
    
    # console.print(createLayout())
    
    with Live(createLayout(), auto_refresh= True) as live:
        
        while True:
            layout['create'].update(Panel( s = Prompt.ask("enter Index") ))
            live.update(createLayout())
            sleep(1)
    
    
    
    
if __name__ == '__main__':
    main()