from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_community.chat_models import ChatGooglePalm
from operator import itemgetter

from decouple import config

from qdrant import vector_store

google_palm = ChatGooglePalm(
    api_key='YOUR_API_KEY',
    model='chat-bison',  
    temperature=0, 
)