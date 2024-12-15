import ollama

import chromadb
from chromadb.utils import embedding_functions

from rich import print as pprint
import uuid
from time import sleep

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob



# cc = chromadb.PersistentClient( path='test_collection' )

# collection = cc.get_or_create_collection( name = 'test_collection' )


class VectorDB:

    def __init__( swayam ):
        
        swayam.vd= chromadb.PersistentClient(
            path= 'test_collection' )
        
        swayam.embedFunction= embedding_functions.DefaultEmbeddingFunction()
        
        swayam.collection= swayam.vd.get_or_create_collection(
            name= 'test_collection' )
    
    
    def isDuplicate(swayam, query: str, threshold: float= 0.1)-> bool:
        
        result= swayam.collection.query(
            query_texts= [query],
            n_results= 1,
            include= ["distances", "documents"]
        )
        pprint(result)
        if result:
            if  not result['distances'][0]:
                return False
            elif result['distances'][0][0] < threshold:
                return True
        return False
              
    def insertToDB(swayam, data: list[dict[str, str]] )-> str:
        
        ids: list[int]= []
        texts: list[str]= []
            
        for _ in data:
            if not swayam.isDuplicate(_['text']):
                ids.append( _['id'] )
                texts.append( _['text'] )
            
        if not texts:
            return 'Already in database.'
        
        embedded: list= swayam.embedFunction(texts)
        pprint(embedded)
        
        try:
            swayam.collection.upsert(
                documents= texts,
                ids= ids,
                embeddings= embedded
            )
            return 'Added collection.'

        except Exception as e:
            return f'Error: {e}'
        
    def search(swayam, query: str) -> str:
        
        result= swayam.collection.query(
            query_texts= [query],
            n_results= 5
        )
        
        return result
    
    
class OllamaLLM:
    
    def __init__(swayam,
                 model_name: str= None,
                 role = 'user'):
        
        swayam.model= model_name
        swayam.role= role
        
    def ollamaStatus(swayam) -> dict:

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
            
        
    def ollamaRequest(swayam, user_query: str, prompt_template: str= None):
        
        # PROMPT_TEMPLATE = f"""
        # Answer the question based only on the following :
        # {swayam.similarMemory(query= user_query)}
        # Answer the question based on the above context: {user_query}.
        # Provide a detailed answer.
        # Don’t justify your answers.
        # Don’t give information not mentioned in the CONTEXT INFORMATION.
        # Do not say "according to the context" or "mentioned in the context" or similar.
        # """
        if not swayam.model:
            result= swayam.ollamaStatus()
            return result
        
        
        try:
            response= ollama.chat(model= swayam.model,
                                  messages= [
                                      {
                                'role': 'system',
                                'content': prompt_template
                            },
                            {
                                'role' : swayam.role,
                                'content': user_query
                            }
                                  ])
            
            return {
                'status': True,
                'response': response 
            }
        
        except Exception as e:
            
            return {
                'status': False,
                'msg': e
            }
        
    

class RAG:
    
    def __init__(swayam, model_name: str= None):
        
        swayam.llm= OllamaLLM(model_name= model_name)
        swayam.vectorDB= VectorDB()
        
        swayam.nlp= spacy.load("en_core_web_sm")
        swayam.nlp.add_pipe('spacytextblob')
        
    def retrieve(swayam, user_query) -> list:
        
        vdb_response= swayam.vectorDB.search(query= user_query)
        
        indexList: list[int]= []
        
        for distances in vdb_response['distances']:
            for indx, distance in enumerate(distances):
                if round(distance, 2) <= 1:
                    indexList.append(indx)

        documents: list[str]= [vdb_response['documents'][0][indx] for indx in indexList]
        
        return documents
        # if distance >= 1 remove
    
    
    def sentiment_analysis(swayam, text) -> dict:
       
        doc = swayam.nlp(text)
        
        polarity: float= doc._.blob.polarity          # sentiment
        subjectivity: float= round(doc._.blob.subjectivity,2)  # subjectivity
        
        entities: dict[str,str]= {}
        
        for entity in doc.ents: # Extract Entities - Entiy lable : Entity  
            entities.update({entity.label_: entity.text}) 
            
        return {
            'text': text,
            'entities':  entities,
            'subjectivity': f"{'neutral' if not subjectivity else 'positive' if subjectivity > 0 else 'negative'}",
            'Sentiment': f"{'neutral' if not polarity else 'positive' if polarity > 0 else 'negative'}"
        }
        
    def augment(swayam, user_query: str) -> dict:
        
        retrieved: list= swayam.retrieve(user_query= user_query)
        
        augemented: list[dict]= [ swayam.sentiment_analysis(_) for _ in retrieved ]
        
        return augemented
        
    def generate(swayam, user_query: str):
        
        augmented_data: list[dict]= swayam.augment(user_query= user_query)
        
        pprint(augmented_data)
    
        formatted_context = "\n".join([
        f"- Sentence: {data['text']}, Sentiment: {data['Sentiment']}, Subjectivity: {data['subjectivity']}, Entities: {data['entities']}"
        for data in augmented_data
        ])
    
        PROMPT_TEMPLATE = f"""
        You are a Helpful AI assistant.
        Use Piece of context given inside Triple backtick to answer the user:
        
        ```{formatted_context}```
        
        Keep the answers concise.
    
        """
        
        response= swayam.llm.ollamaRequest( user_query= user_query,
                                 prompt_template= PROMPT_TEMPLATE)
        
        return response
    
    
rag = RAG(model_name= 'llama3.2:1b')
pprint(rag.generate("Can you tell me Manu's place?"))
# vdb= VectorDB()

# vdb.insertToDB([{'id':str(uuid.uuid4()), 'text': 'manu is a sadistic person'}])
# vdb.insertToDB([{'id':str(uuid.uuid4()), 'text':"i'am Manu's girlfriend"}])
# vdb.insertToDB([{'id':str(uuid.uuid4()), 'text':"i really happy to have Manu as my boyfriend"}])