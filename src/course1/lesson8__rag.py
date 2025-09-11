"""
# RAG

pdf => chunks => embedding => store in vectorDb => retrieve/similarity search => feed relevant chunks to llm => output

""" 

from langchain_core.output_parsers import StrOutputParser
from src.lessons.base import init_ollama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel, SimpleChatModel
from langchain_core.language_models import LanguageModelInput
from langchain_ollama import OllamaLLM, ChatOllama
from src.config.index import config
from langchain.globals import set_verbose, set_debug
from langchain_core.messages import BaseMessage
import os
import uuid
from langchain_core.runnables.base import RunnableSequence, RunnableParallel, RunnableLambda

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.branch import RunnableBranch

# file messages storage
from langchain_community.chat_message_histories.file import FileChatMessageHistory

from langchain_core.prompt_values import ChatPromptValue

# embedding
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
import sys

# set_debug(value=True)
set_verbose(value=True)

# current file directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# one level up
# root_dir = os.path.dirname(p=current_dir)

# multiple levels back
root_dir = os.path.abspath(path=os.path.join(current_dir, os.pardir, os.pardir))

#adding folder storage path
file_storage_path = os.path.join(root_dir, "storage")

# path to the file we are loading
file_path = os.path.join(file_storage_path, "gtav.txt")

# storage: D:\workspace\ai\langchain01\src\storage
# print("storage:",file_storage_path)

# chroma_db directory
persistent_dir = os.path.join(root_dir, "db", "chroma_db")

# print(persistent_dir)
print(file_path)
# check if chrome_db dir exists
if not os.path.exists(persistent_dir):
  print("persistent directory does not exist.")

  # check if the file we are loading exists
  if not os.path.exists(file_path):
    raise FileNotFoundError(
      f"the file {file_path} does not exists. please check the path."
    )

  # load text content from the file
  loader = TextLoader(file_path=file_path)
  documents = loader.load()

if not len(documents):
  raise Exception("documents are empty")
  
print(documents)
sys.exit(1)


llm = ChatOllama(
  model=config.llm_model,
  base_url=config.llm_url,
  stream=True,
  temperature=0.8,
  client_options={"proxies": None}
)

# embed model
embedding = OllamaEmbeddings(
  base_url=config.llm_url,
  model=config.embed_model,
  temperature=0.6,
  client_options={"proxies": None}
)

# string parser
parser = StrOutputParser()

# chat loop 
while True:
  query = input("Enter a review. or /exit\n")

  if query.lower() == "/exit":
    print("Goodbye!")
    break

  stream = pipeline.stream(
    input={"feedback": query},
  )

  # stream chunks of message
  for chunk in stream:
    print(chunk, end="", flush=True)

  print("\n")

