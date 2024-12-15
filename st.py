from sentence_transformers import SentenceTransformer
from pprint import pprint

# Load a local embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Example text to embed
text = "manu"
embedding = embedder.encode(text).tolist()
pprint(embedding)