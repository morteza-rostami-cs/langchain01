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
# from langchain.memory import ChatMessageHistory, summary_buffer

# tools 
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType, AgentExecutor
from langchain_ollama import OllamaLLM
from typing import Iterator
from langchain_core.runnables.utils import AddableDict

llm: OllamaLLM = init_ollama()

parser: StrOutputParser = StrOutputParser()

# function/tool
def get_current_weather(location: str) -> str:
  return f"the current weather in {location} is sunny and 25°C."

# wrap the function as a tool
weather_tool: Tool = Tool(
  name="GetWeather",
  func=get_current_weather,#function with tool logic
  # llm decides to use tool or not =>based on description
  description="Use this tool to get the current weather for a given city."
)

# agent with tool
agent: AgentExecutor = initialize_agent(
  tools=[weather_tool],
  llm=llm,
  # agents decides when to call what tool
  agent="zero-shot-react-description",
  verbose=True,
  handle_parsing_errors=True
)

while True:
  # get input 
  query: str = input("Enter your query, /exit\n")

  if query.lower() == "/exit":
    print("Goodbye!")
    break
  
  try:
    # ask agent something that triggers the tool
    stream: Iterator[AddableDict] = agent.stream(input=query)

    for chunk in stream:
      print(chunk, end="", flush=True)

  except Exception as e:
    print("stream failed.", e)

  print("\n")