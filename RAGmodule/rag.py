import ollama

import chromadb
from chromadb.utils import embedding_functions

import uuid
from time import sleep

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

from rich import print as pprint

# ChromaDB control
class VectorDB:
    """
    Handles operations for a vector database using ChromaDB, including storing, 
    querying, and checking for duplicate entries.

    Attributes:
        vd (PersistentClient): Persistent client for the ChromaDB database.
        embedFunction (EmbeddingFunction): Function to embed texts for vector storage.
        collection (Collection): The specific collection within the database being operated on.
    """
    

    def __init__( swayam, collection_name: str='test_collection' ):
        
        """
        Initializes the vector database and creates a collection.

        Args:
            collection_name (str): Name of the collection to be used or created in the database. 
                                   Defaults to 'test_collection'.
        """
         
        swayam.vd= chromadb.PersistentClient(
            path= collection_name )
        
        swayam.embedFunction= embedding_functions.DefaultEmbeddingFunction()
        
        swayam.collection= swayam.vd.get_or_create_collection(
            name= collection_name )
    
    def isDuplicate(swayam, query: str, threshold: float= 0.1)-> bool:
        """
        Checks if a given text is already stored in the database based on a similarity threshold.

        Args:
            query (str): The text to be checked for duplication.
            threshold (float): The similarity threshold to consider two entries as duplicates. 
                               Defaults to 0.1.

        Returns:
            bool: True if the query is a duplicate, False otherwise.
        """
        result= swayam.collection.query(
            query_texts= [query],
            n_results= 1,
            include= ["distances", "documents"]
        )

        if result:
            if  not result['distances'][0]:
                return False
            elif result['distances'][0][0] < threshold:
                return True
        return False
              
    def insertToDB(swayam, data: list[dict[str, str]] )-> str:
        """
        Inserts a list of text entries into the database if they are not duplicates.

        Args:
            data (list[dict]): A list of dictionaries, where each dictionary contains:
                               - 'id' (str): Unique identifier for the entry.
                               - 'text' (str): The text content to be stored.

        Returns:
            str: Message indicating whether data was added or already exists.
        """
        ids: list[int]= []
        texts: list[str]= []
            
        for _ in data:
            if not swayam.isDuplicate(_['text']):
                ids.append( _['id'] )
                texts.append( _['text'] )
            
        if not texts:
            return 'Already in database.'
        
        embedded: list= swayam.embedFunction(texts)

        
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
        """
        Searches the database for the most relevant documents to the provided query.

        Args:
            query (str): The text query for which to search.

        Returns:
            str: The query results including matching documents and their distances.
        """
        result= swayam.collection.query(
            query_texts= [query],
            n_results= 5
        )
        
        return result
    
    def all(swayam) -> dict:
        """
        Retrieves all documents from the current database collection.

        Returns:
            dict: A dictionary containing all documents in the collection.
        """
        all_collections= swayam.collection.get()
        
        return all_collections
    
    
# Communicattion betwee ollama models
class OllamaLLM:
    """
    Facilitates communication with Ollama language models for chat-based interactions.

    Attributes:
        model (str): The name of the Ollama model to use for communication.
        role (str): The role for the interaction (e.g., 'user', 'assistant').
    """

    def __init__(swayam,
                 model_name: str= None,
                 role = 'user'):
        """
        Initializes the Ollama language model for interaction.

        Args:
            model_name (str): Name of the language model. Defaults to None.
            role (str): Role of the model in the conversation. Defaults to 'user'.
        """        
        swayam.model= model_name
        swayam.role= role
        
    def ollamaStatus(swayam) -> dict:
        """
        Checks the availability of the Ollama service and retrieves a list of available models.

        Returns:
            dict: Contains the status and available models, or an error message if unsuccessful.
        """
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
        """
        Sends a query to the Ollama model and retrieves the response.

        Args:
            user_query (str): The user's input query.
            prompt_template (str): A template to customize the system's response. Defaults to None.

        Returns:
            dict: Contains the status and response from the model, or an error message if unsuccessful.
        """
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
        
        
# retrievel augemented generation pipeline
class RAG:
    """
    Implements a Retrieval-Augmented Generation (RAG) pipeline, integrating VectorDB and OllamaLLM
    for context-aware text generation.

    Attributes:
        llm (OllamaLLM): An instance of the OllamaLLM class for model interaction.
        vectorDB (VectorDB): An instance of the VectorDB class for database interaction.
        nlp (Language): A spaCy language model with sentiment analysis enabled.
    """
    def __init__(swayam, model_name: str= None,
                 collection_name: str= 'test_collection'):
        """
        Initializes the RAG pipeline with the specified language model.

        Args:
            model_name (str): Name of the language model. Defaults to None.
        """        
        swayam.llm= OllamaLLM(model_name= model_name)
        swayam.vectorDB= VectorDB(collection_name= collection_name)
        swayam.vectorDB
        swayam.nlp= spacy.load("en_core_web_sm")
        swayam.nlp.add_pipe('spacytextblob')
        
    def retrieve(swayam, user_query) -> list:
        """
        Retrieves relevant documents from the database based on the user's query.

        Args:
            user_query (str): The input query for retrieval.

        Returns:
            list: A list of relevant documents retrieved from the database.
        """
    
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
        """
        Performs sentiment analysis and entity extraction on a given text.

        Args:
            text (str): The text to analyze.

        Returns:
            dict: Contains sentiment, subjectivity, and named entities extracted from the text.
        """
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
        """
        Retrieves and augments relevant documents with sentiment analysis.

        Args:
            user_query (str): The input query for retrieval.

        Returns:
            dict: Augmented data including sentiment and entity information.
        """
        retrieved: list= swayam.retrieve(user_query= user_query)
        
        augemented: list[dict]= [ swayam.sentiment_analysis(_) for _ in retrieved ]
        
        return augemented
        
    def generate(swayam, user_query: str):
        """
        Combines retrieved data with language model responses for context-aware generation.

        Args:
            user_query (str): The user's input query.

        Returns:
            dict: The response generated by the language model based on retrieved data.
        """
        augmented_data: list[dict]= swayam.augment(user_query= user_query)
        
    
        formatted_context = "\n".join([
        f"- Sentence: {data['text']}, Sentiment: {data['Sentiment']}, Subjectivity: {data['subjectivity']}, Entities: {data['entities']}"
        for data in augmented_data
        ])
    
        PROMPT_TEMPLATE = f"""
        You are a Helpful AI assistant.
        Use Piece of context given to answer the user:
        
        {formatted_context}
        
        Keep the answers concise.
    
        """
        
        response= swayam.llm.ollamaRequest( user_query= user_query,
                                 prompt_template= PROMPT_TEMPLATE)
        
        return response
    
    
# rag = RAG(model_name= 'llama3.2:1b')
# pprint(rag.generate("Can you tell me Manu's place?"))
# vdb= VectorDB()
# pprint(vdb.all())

# vdb.insertToDB([{'id':str(uuid.uuid4()), 'text': 'manu is a sadistic person'}])
# vdb.insertToDB([{'id':str(uuid.uuid4()), 'text':"i'am Manu's girlfriend"}])
# vdb.insertToDB([{'id':str(uuid.uuid4()), 'text':"i really happy to have Manu as my boyfriend"}])