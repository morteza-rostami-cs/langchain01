"""
# save chat history inside json file
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

# create a file for each chat_history
def get_chat_history(session_id: str) -> FileChatMessageHistory:
  # a json file path for each session
  file_path = f"./history/chat_history_{session_id}.json"

  # create file if does not exists
  os.makedirs(name=os.path.dirname(p=file_path), exist_ok=True)

  # return a file message chat history => maybe has all the messages and some methods, to add a message or something
  return FileChatMessageHistory(
    file_path=file_path,
    encoding="utf-8",
    ensure_ascii=False # allow non-ascii chars
  )

# returns a FileChatMessageHistory =>memory
def get_session_history(session_id: str) -> FileChatMessageHistory:
  return get_chat_history(session_id=session_id)

# create a new history/file => for each new session
session_id: str = uuid.uuid4()
# start a file memory session
# history = get_chat_history(session_id=session_id)

# print session info
# print(f"new chat history at: {history.file_path}")

# initial system-message
# system_message = SystemMessage(content="you are a helpful ai assistant.")
# append the first prompt to chat history
# history.add_message(system_message)

# prompt
prompt = ChatPromptTemplate.from_messages(messages=[
  ("system", "You are a helpful assistant. give a short answer to this query."),
  MessagesPlaceholder(variable_name="history"),
  ("human", "query: {query}")
])

# string parser
parser = StrOutputParser()

# build a chain 
pipeline = prompt | llm | parser

# create a runnable with message history
# this basically handles => adding new messages to memory
runnable_with_history = RunnableWithMessageHistory(
  runnable=pipeline,
  # pass a memory object => in this case a FileChatMessageHistory
  get_session_history=get_session_history,
  # user input
  input_messages_key="query",
  # where we inject history in prompt
  history_messages_key="history"
)

# chat loop 
while True:
  query = input("Enter your query. or /exit\n")

  if query.lower() == "/exit":
    print("Goodbye!")
    break

  # append user_query to chat_history
  #history.add_user_message(HumanMessage(content=query))

  # get ai response => based on chat_history
  # stream = llm.stream(input=history.messages)
  stream = runnable_with_history.stream(
    input={"query": query},
    # pass session_id here
    config={"configurable": {"session_id": session_id}}
  )

  # each ai response
  # ai_response = ""

  # stream chunks of message
  for chunk in stream:
    # content = chunk.content
    # concat each chunk of ai response
    # ai_response += content

    print(chunk, end="", flush=True)

  # push each ai response into chat_history
  #history.add_ai_message(AIMessage(content=ai_response))

  # print("\n")
  # print(ai_response)

  print("\n")

