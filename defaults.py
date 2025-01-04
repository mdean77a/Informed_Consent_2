# Defaults
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
import os
OPENAI_API_KEY = os.getenv("NEWKEY")
default_embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
default_location = ":memory:"
default_url = "http://localhost:6333"
default_llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY, streaming=True, temperature=0)