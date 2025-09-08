from src.config.index import config
import os
import langchain
from langchain_ollama import OllamaLLM

# Disable proxies
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("ALL_PROXY", None)

# (optional, lowercase too, since some systems use them)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ.pop("all_proxy", None)

# turns off the stupid proxy
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

def main():
  # import src.lessons.lesson1
  # import src.lessons.lesson2
  # import src.lessons.lesson3
  # import src.lessons.lesson4
  # import src.lessons.lesson5
  # import src.lessons.lesson6
  # import src.lessons.lesson7
  # import src.lessons.lesson8
  # import src.lessons.lesson9
  # import src.lessons.lesson10
  # import src.lessons.lesson11
  # import src.course1.lesson1
  # import src.course1.lesson2
  # import src.course1.lesson3
  # import src.course1.lesson4
  # import src.course1.lesson5
  import src.course1.lesson6
  print("\nthis is the main file\n")

if __name__ == "__main__":
  main()