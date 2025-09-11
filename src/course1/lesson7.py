"""
# chains => branching


""" 

from langchain_core.output_parsers import StrOutputParser
from src.lessons.base import init_ollama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel, SimpleChatModel
from langchain_core.language_models import LanguageModelInput
from langchain_ollama import OllamaLLM, ChatOllama
from src.config.index import config
from langchain.globals import set_verbose, set_debug
from langchain_core.messages import BaseMessage
import os
import uuid
from langchain_core.runnables.base import RunnableSequence, RunnableParallel, RunnableLambda

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.branch import RunnableBranch

# file messages storage
from langchain_community.chat_message_histories.file import FileChatMessageHistory

from langchain_core.prompt_values import ChatPromptValue

# set_debug(value=True)
set_verbose(value=True)

llm = ChatOllama(
  model=config.llm_model,
  base_url=config.llm_url,
  stream=True,
  temperature=0.8,
  client_options={"proxies": None}
)

# string parser
parser = StrOutputParser()

positive_feedback_template = ChatPromptTemplate(
  messages=[
    ("system", "You are a helpful assistant."),
    ("human", "generate a thank you note for this positive feedback: {feedback}"),
  ]
)

negative_feedback_template = ChatPromptTemplate(
  messages=[
    ("system", "You are a helpful assistant."),
    ("human", "generate a response addressing this negative feedback: {feedback}"),
  ]
)

neutral_feedback_template = ChatPromptTemplate(
  messages=[
    ("system", "You are a helpful assistant."),
    ("human", "generate a thank you note for this positive feedback: {feedback}"),
  ]
)

escalate_feedback_template = ChatPromptTemplate(
  messages=[
    ("system", "You are a helpful assistant."),
    ("human", "generate a message to escalate this feedback to a human agent: {feedback}"),
  ]
)

# classify the feedback into a category
classification_template = ChatPromptTemplate(
  messages=[
    ("system", "You are a helpful assistant."),
    ("human", "Classify the sentiment of this feedback as positive, negative, neutral, or escalate: {feedback}."),
  ]
)

branches = RunnableBranch(
  (
    # if the out has positive
    lambda output:"positive" in output,
    positive_feedback_template | llm | parser, #positive chain
  ),
  (
    lambda output: "negative" in output,
    negative_feedback_template | llm | parser,# negative chain
  ),
  (
    lambda output: "neutral" in output,
    neutral_feedback_template | llm | parser, # neutral chain
  ),
  # else: default
  escalate_feedback_template | llm | parser,
)

# classification chain
classification_chain = classification_template | llm | parser

# so: based on classification_chain => it runs one of the branches
pipeline = classification_chain | branches

# chat loop 
while True:
  query = input("Enter a review. or /exit\n")

  if query.lower() == "/exit":
    print("Goodbye!")
    break

  stream = pipeline.stream(
    input={"feedback": query},
  )

  # stream chunks of message
  for chunk in stream:
    print(chunk, end="", flush=True)

  print("\n")

