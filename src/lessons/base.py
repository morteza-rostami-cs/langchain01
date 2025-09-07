
from src.config.index import config
import langchain
from langchain_ollama import OllamaLLM

# return an ollama instance
def init_ollama() -> OllamaLLM:
  # create a llm
  llm = OllamaLLM(
    model=config.llm_model,
    base_url=config.llm_url,
    stream=True,
    temperature=0.7,
    client_options={"proxies": None}

    # verbose=
  )
  
  return llm

# stream ollama response
def stream_response(query: str, llm: OllamaLLM) -> None:
  stream = llm.stream(input=query, config=None)

  for chunk in stream:
    print(chunk, end="", flush=True)