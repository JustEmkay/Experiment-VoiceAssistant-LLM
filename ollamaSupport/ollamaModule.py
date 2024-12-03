import ollama
from datetime import datetime
from pprint import pprint


def ollamaStatus() -> dict:

    try:
        result = ollama.list()
        models = [r['model'] for r in result['models'] if r['model'] != 'moondream:latest']
        return {
            'status' : True,
            'models' : models,
        }
        
    except Exception as e:
        return {
            'status' : False,
            'msg' : f"Error : {e}",
        }
        
    
def ollamaRequest(model_name: str,
                  role: str,
                  prompt: str,
                  JSONresponse: bool = None,
                  memory: str = None):
    ''' Return a dictionary with keys[status,response/msg]
    
        Parameters:
            model_name (str): llm model name.
            role (str): 'assistant', 'user' and 'system'.
            promptt (str): prompt from user to llm.
        
        Returns:
            dictionary (dict):
                status (bool): status of request.
                response (str): LLM response.
                msg (str): Error msg if status is False.
    '''


    data = {
        'username': "manu",
        'assistant': "joi",
        'today': datetime.now()
    }

    instruction = f''' 

    Act as a personal assistant, provide helpful and informative responses.
    I'll provide you with tasks, questions, and topics to discuss.Current date and
    time is {data['today']}. Please responses accordingly, suing a friendly and professional tone. 
    Keep track of our converstation and provide follow-up responses as needed.
    consider anything inside triple quotes as imformation. 
    
    
    '''

    try:    
        res = ollama.chat(model=model_name,
                          format= f'{"json" if JSONresponse else ""}',
                        messages=[
                            {
                                'role' : 'system',
                                'content' : instruction   
                            },
                            {
                                'role' : 'assistant',
                                'content' : memory 
                            },
                            {
                                'role' : role,
                                'content': prompt
                            }
                        ]
                    )

        # print(res['message']['content']) 
        print('____________________________')
        return {
            'status': True,
            "response" : res['message']['content']
            }

    except Exception as e:
        print('Error:',e)
        return {
            'status' : False,
            'msg' : e
        }
    
if __name__ == '__main__':
    
    print(ollamaRequest(model_name= 'llama3.2:1b',
                        role= 'user',
                        prompt= ' tell me about ram',
                        JSONresponse= False))