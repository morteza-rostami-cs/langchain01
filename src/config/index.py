from dotenv import load_dotenv
load_dotenv()

import os

LLM_MODEL = os.getenv("LLM_MODEL")
LLM_URL = os.getenv("LLM_URL")
EMBED_MODEL = os.getenv("EMBED_MODEL")

if not LLM_MODEL or not LLM_URL or not EMBED_MODEL:
  raise Exception("config:index missing env")

class Config:
  llm_url = LLM_URL
  llm_model = LLM_MODEL

  embed_model = EMBED_MODEL

# singleton
config = Config()