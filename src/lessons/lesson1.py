
from src.config.index import config
import langchain
from langchain_ollama import OllamaLLM

# create a llm
llm = OllamaLLM(
  model=config.llm_model,
  base_url=config.llm_url,
  stream=True,
  temperature=0.7,
  client_options={"proxies": None}

  # verbose=
)

stream = llm.stream("write a short story about a hot girl")

for chunk in stream:
  print(chunk, end="", flush=True)

#lang_version = langchain.__version__
#print(lang_version)