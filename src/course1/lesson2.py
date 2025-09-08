"""
# working with chat model => ChatOllama
# and chat history => in memory
""" 

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

# file messages storage
from langchain_community.chat_message_histories.file import FileChatMessageHistory

# set_debug(value=True)
set_verbose(value=True)

# llm = OllamaLLM(
#   model=config.llm_model,
#   base_url=config.llm_url,
#   stream=True,
#   temperature=0.7,
#   client_options={"proxies": None}

#   # verbose=
# )

# OllamaLLM => returns string when invoked
# ChatOllama => returns BaseMessage object
llm = ChatOllama(
  model=config.llm_model,
  base_url=config.llm_url,
  stream=True,
  temperature=0.8,
  client_options={"proxies": None}
)

# in memory chat history
chat_history = []

# initial system-message
system_message = SystemMessage(content="you are a helpful ai assistant.")
# append the first prompt to chat history
chat_history.append(system_message)

# chat loop 
while True:
  query = input("Enter your query. or /exit\n")

  if query.lower() == "/exit":
    print("Goodbye!")
    break

  # append user_query to chat_history
  chat_history.append(HumanMessage(content=query))

  # get ai response => based on chat_history
  stream = llm.stream(input=chat_history)

  # each ai response
  ai_response = ""

  # stream chunks of message
  for chunk in stream:
    content = chunk.content
    # concat each chunk of ai response
    ai_response += content

    print(content, end="", flush=True)

  # push each ai response into chat_history
  chat_history.append(AIMessage(content=ai_response))

  # print("\n")
  # print(ai_response)

  print("\n")

"""
# set_debug(value=True)
set_verbose(value=True)

# llm = OllamaLLM(
#   model=config.llm_model,
#   base_url=config.llm_url,
#   stream=True,
#   temperature=0.7,
#   client_options={"proxies": None}

#   # verbose=
# )

# OllamaLLM => returns string when invoked
# ChatOllama => returns BaseMessage object
llm = ChatOllama(
  model=config.llm_model,
  base_url=config.llm_url,
  stream=True,
  temperature=0.8,
  client_options={"proxies": None}
)

#list[AIMessage | HumanMessage | SystemMessage]
messages: LanguageModelInput = [
  SystemMessage(content="You are a math teacher."),
  HumanMessage(content="what is 7 times 8?"),
]

# now with ChatOllama => each chunk is an object
stream: BaseMessage = llm.stream(input=messages)

for chunk in stream:
  # get content from each chunk
  print(chunk.content, end="", flush=True)

# response: str = llm.invoke("what's up?")

# print(type(response))

"""