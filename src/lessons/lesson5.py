from langchain.prompts import PromptTemplate
from src.lessons.base import init_ollama
from langchain_core.output_parsers import StrOutputParser

llm = init_ollama()

template = """
role: you are a story teller. given a topic and style, tell me a story.

rules:
  - story should be MAX 100 token! NOT MORE!

topic: 
{topic}

style:
{style}
"""

prompt = PromptTemplate(
  input_variables=["topic", "style"],
  template=template
)

parser = StrOutputParser()

from langchain_core.runnables import RunnableSequence

pipeline: RunnableSequence = prompt | llm | parser

stream = pipeline.stream({"topic": "rain", "style": "dark"})

for chunk in stream:
  print(chunk, end="", flush=True)

# we can format/inject values into template like this
# prompt_with_values: str = prompt.format(topic="fire", style="short")
# print(prompt_with_values)

# pass the process prompt into a llm
# stream = llm.stream(prompt_with_values)

# for chunk in stream:
#   print(chunk, end="", flush=True)

# pipeline: RunnableSequence = prompt | llm | parser

# print(type("sds"))

#stream = pipeline.stream()
