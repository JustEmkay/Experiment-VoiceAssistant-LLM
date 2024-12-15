from chromadb.utils import embedding_functions
from rich import print as pprint


default_ef = embedding_functions.DefaultEmbeddingFunction()

pprint(type(default_ef(['manu'])))
