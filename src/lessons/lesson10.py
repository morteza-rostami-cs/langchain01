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

template = """
role: you are a helpful assistant.

query:
{query}
"""

prompt = PromptTemplate.from_template(template=template)

# clean string output
# stringParser: StrOutputParser = StrOutputParser()

from langchain_core.output_parsers import CommaSeparatedListOutputParser

# parses the output as some list of strings
# parser = CommaSeparatedListOutputParser()

#pydantic => json like
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.output_parsers import OutputFixingParser

# define a schema
class Movie(BaseModel):
  title: str = Field(description="Title of the movie")
  year: int = Field(description="Release year")
  genre: str = Field(description="Main genre")

# pydantic parser
parser = PydanticOutputParser(pydantic_object=Movie)

# pydantic ready prompt and template

py_template = """
You are a helpful assistant. Extract the following details from the text below.
Return a **flat JSON object ONLY** with these fields: title, year, genre.

Movie information:
{movie_information}

Respond using this JSON format exactly:
{format_instructions}
"""

py_prompt = PromptTemplate(
  template=py_template, 
  input_variables=["movie_information"], 
  partial_variables={"format_instructions": parser.get_format_instructions()}
)

# rty to fix any formatting issue in json data further
fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

pipeline = py_prompt | llm | fixing_parser

while True:
  # get input 
  query: str = input("Enter Information about the movie, /exit\n")
 
  if query.lower() == "/exit":
    print("Goodbye!")
    break
  
  try:

    response = pipeline.invoke({
      "movie_information": query,
    })

    print(response)

    # for chunk in stream:
    #   print(chunk, end="", flush=True)

  except Exception as e:
    print("stream failed.", e)

  print("\n")

# llm returns the wrong JSON format!!!!!!!!!!!!!!!!!!
# so this code does not work