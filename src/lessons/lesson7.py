from src.lessons.base import init_ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
#import random
from uuid import uuid4
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from langchain_core.chat_history import BaseChatMessageHistory

llm = init_ollama()

parser = StrOutputParser()

# in memory storage
store: any = {}

# store and retrieve in memory message
def get_session_history(session_id: str) -> BaseChatMessageHistory:
  print(store, session_id)
  # store a session if does not exists
  if session_id not in store:
    # store messages
    store[session_id] = InMemoryChatMessageHistory()
  
  return store[session_id]

# a runnable for debug
def debug_input(x: any):
  print("\n DEBUG \n")
  print(x)
  print("\n DEBUG END \n")

  # return input => to the next runnable
  return x

debug_input_runnable = RunnableLambda(func=debug_input)

# template = """
# role: you are a helpful assistant.

# here is our conversation so far:
# {history}

# User: {input}

# Assistant:
# """

# prompt1 = PromptTemplate.from_template(template=template1)

# prompt = PromptTemplate(
#   input_variables=["history", "input"],
#   template=template
# )

prompt = ChatPromptTemplate.from_messages([
  ("system", "role: you are a helpful assistant."),
  MessagesPlaceholder(variable_name="history"),
  ("human", "{input}")
])

# deprecated
# conversation memory => handles memory storage and injecting history
# memory: ConversationBufferMemory = ConversationBufferMemory(
#   # chat_memory=
#   # must match the template variable
#   memory_key="history",
#   # store raw text instead of message objects 
#   return_messages=False
# )

pipeline = debug_input_runnable | prompt | llm | parser 

#wrap the chain with memory
chain_with_memory = RunnableWithMessageHistory(
  runnable=pipeline,
  # memory=memory,
  get_session_history=get_session_history,
  input_messages_key="input",
  history_messages_key="history"
)

# per chat => in this case => each script run
session_id = uuid4()

while True:
  # get input 
  query = input("Enter your query, /exit\n")

  if query.lower() == "/exit":
    print("Goodbye!")
    break

  stream = chain_with_memory.stream({"input": query}, config={"configurable": {"session_id": session_id}})

  for chunk in stream:
    print(chunk, end="", flush=True)

  print("\n")