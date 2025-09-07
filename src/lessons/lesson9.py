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

# another tool => show the result of multiplication
def multiply_numbers(a: int, b: int) -> str:
  return f"the result of {a} x {b} is {a * b}"

# wrap the function as a tool
weather_tool: Tool = Tool(
  name="GetWeather",
  func=get_current_weather,#function with tool logic
  # llm decides to use tool or not =>based on description
  description="Use this tool to get the current weather for a given city."
)

multiply_tool: Tool = Tool(
  name="MultiplyNumbers",
  # get the query: 1 2 => break into an list => convert to int => unpack as arguments into the multiply_function
  func=lambda query: multiply_numbers(*map(int, query.split())),
  description="Use this tool when you need to multiply two numbers. Input format: 'num1 num2'",
)

# agent with tool
agent: AgentExecutor = initialize_agent(
  tools=[weather_tool, multiply_tool],
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

    # using two agents
    print(agent.invoke(input=query))

    # ask agent something that triggers the tool
    # stream: Iterator[AddableDict] = agent.stream(input=query)

    # for chunk in stream:
    #   print(chunk, end="", flush=True)

  except Exception as e:
    print("stream failed.", e)

  print("\n")