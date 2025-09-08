"""
# prompt template
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

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

# file messages storage
from langchain_community.chat_message_histories.file import FileChatMessageHistory

# set_debug(value=True)
set_verbose(value=True)

llm = ChatOllama(
  model=config.llm_model,
  base_url=config.llm_url,
  stream=True,
  temperature=0.8,
  client_options={"proxies": None}
)

# string parser
parser = StrOutputParser()

template = """
role: You are a joke teller.

tell me a joke about this topic: {topic}
"""

prompt = ChatPromptTemplate.from_template(template=template)

"""
also: 
messages = [
#use tuple => for string interpolation
("system", "you are a comedian. {could be some variable} "),
("human", "tell me a joke about {topic}"),

# can't do interpolation 
HumanMessage(content="tell me some jokes.")
]

"""

# what prompt returns 
#print(prompt.invoke({"topic": "cats"}))
"""
# so topic is replace with = cats

messages=[
  HumanMessage(content='\nrole: You are a joke teller.\n\ntell me a joke about this topic: cats\n', additional_kwargs={}, response_metadata={})
]
"""

pipeline = prompt | llm | parser

# chat loop 
while True:
  query = input("Enter joke topic. or /exit\n")

  if query.lower() == "/exit":
    print("Goodbye!")
    break

  stream = pipeline.stream(
    input={"topic": query},
  )

  # stream chunks of message
  for chunk in stream:
    print(chunk, end="", flush=True)

  print("\n")

