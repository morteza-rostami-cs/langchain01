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
import json

# tools 
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType, AgentExecutor
from langchain_ollama import OllamaLLM
from typing import Iterator
from langchain_core.runnables.utils import AddableDict

from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.runnables import Runnable, RunnableMap

# parses the output as some list of strings
# parser = CommaSeparatedListOutputParser()

#pydantic => json like
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.output_parsers import OutputFixingParser

# tools 
def get_current_weather(location: str) -> str:
  return F"the weather in {location} is rainy and 25c."

weather_tool = Tool(
  name="GetWeather",
  func=get_current_weather,
  description="Use this for queries about weather."
)

parser = StrOutputParser()

llm: OllamaLLM = init_ollama()

template_topic = """
Is the following text's main topic about weather?

text:
{text}

rules: 
  - response ONLY with a json object like this:
  - if: topic == weather => then extract and add a location field. else: no location field!
  {{ "weather": False or True, "topic": "weather or movies", "location": "landon" }}
"""

prompt_topic = PromptTemplate.from_template(template=template_topic)

# pipeline_topic = prompt_topic | llm | parser

# runs some runnables parallel
branch_runnable = RunnableMap(
  {"topic_decision": prompt_topic | llm | parser}
)

# topic = branch_runnable.invoke({"text": "what is the weather in landon today in london?"})

# topic = branch_runnable.invoke({"text": "What do you know about angelina jolie?"})

topic = branch_runnable.invoke({"text": "where is Iran?"})

print("------------\n")

try:
  raw = topic["topic_decision"]

  # print(repr(json_str))
  clean = raw.strip().removeprefix("```json").removesuffix("```").strip()

  json = json.loads(clean)
  # {'weather': True, 'topic': 'weather'}
except Exception as e:
  print("json failed!", e)

print(json)

# print(topic) # {'topic_decision': 'Yes \n'}

# condition based on llm output
if json["weather"]:
  result = weather_tool.invoke(json["location"])
  print("here your weather: ", result)
else:
  print(f"no weather data for this topic: {json["topic"]}")