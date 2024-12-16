import sys # to import modules
sys.path.append('../')
from os import system


from RAGmodule.rag import RAG
from rich import print
from rich.prompt import Prompt
from rich.panel import Panel

import uuid

def saveChat(vDB, user_query, response) -> None:
    
    vDB.insertToDB( data= [{'id': str(uuid.uuid4()), 'text': user_query},
                           {'id': str(uuid.uuid4()), 'text': response},] )
    

def main()-> None:
    
    rag = RAG(model_name= 'llama3.2:1b',
              collection_name= 'test1')
    
    print("\n")
    print('[bold red]Assistant:[/bold red] How can I help you?')
    while True:
        
        user:str =Prompt.ask('[bold green]User[/bold green]')
        if user == 'exit':
            system('cls')

        response= rag.generate(user_query= user)
        if response['status']:
            saveChat(rag.vectorDB, user_query= user,
                     response= response['response']['message']['content'])
            print(f"[bold red]Assistant:[/bold red] {response['response']['message']['content']}")
            print("\n")
        
    
    
# main
if __name__ == '__main__':
    main()