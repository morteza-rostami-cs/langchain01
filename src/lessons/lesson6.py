from src.lessons.base import init_ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = init_ollama()

parser = StrOutputParser()

template1 = """
role: you are tasked with summering the given text.

text:
{text}
"""
prompt1 = PromptTemplate.from_template(template=template1)

template2 = """
role: you are tasked with creating a bullet pointed list of most important parts of the text summery.

summery:
{summery}
"""
prompt2 = PromptTemplate.from_template(template=template2)

# passing the result of one prompt into another
pipeline = prompt1 | llm | parser | prompt2 | llm | parser

stream = pipeline.stream({"text": "The rain hammered against the rusted tin roof like skeletal claws scratching at bone. Each drop was a scream swallowed by the suffocating grey fog. Inside, Elias huddled, his breath misting in the cold air.  He watched, through the greasy glass, as the storm raged on. Outside, a single figure moved, silhouetted against the downpour, their face obscured.  Elias knew he shouldn't follow. But curiosity, like a ravenous beast, gnawed at his gut."})

for chunk in stream:
  print(chunk, end="", flush=True)