import ollama


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
        
    
def ollamaRequest(model_name: str, role: str, prompt: str):

    try:    
        res = ollama.chat(model=model_name, 
                        messages=[
                            # {
                            #     'role' : 'system',
                            #     'content' : personality + "\n" + prevs_memories   
                            # },
                            {
                                'role' : role,
                                'content': prompt
                            }
                        ]
                    )

        return {
            'status': True,
            "response" : res['message']['content']
            }

    except Exception as e:
        print('Error at joi')
        return {
            'status' : False,
            'msg' : e
        }
    
