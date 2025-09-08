
from src.lessons.base import init_ollama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel, SimpleChatModel
from langchain_core.language_models import LanguageModelInput
from langchain_ollama import OllamaLLM

from langchain.globals import set_verbose, set_debug

# set_debug(value=True)
set_verbose(value=True)

llm: OllamaLLM = init_ollama()

#list[AIMessage | HumanMessage | SystemMessage]
messages: LanguageModelInput = [
  SystemMessage(content="You are a math teacher."),
  HumanMessage(content="what is 7 times 8?"),
]

stream: str = llm.invoke(input=messages)

for chunk in stream:
  print(chunk, end="", flush=True)

# response: str = llm.invoke("what's up?")

# print(type(response))