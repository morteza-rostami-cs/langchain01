"""
# chains => parallel


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

# main prompt => to get the product features
get_features_prompt = ChatPromptTemplate(
  messages=[
    ("system", "You are an expert product reviewer."),
    ("human", "List the main features of the product: {product_name}"),
  ]
)

# define pros analysis step
def analyze_pros(features: str) -> ChatPromptValue:
  # prompt for getting pros fo product
  pros_template = ChatPromptTemplate(messages=[
    ("system", "you are an expert product reviewer."),
    ("human", "Given these features: {features}, list the pros of these features.")
  ])

  return pros_template.format_prompt(features=features)

def analyze_cons(features: str) -> ChatPromptValue:
  cons_template = ChatPromptTemplate(messages=[
    ("system", "you are an expert product reviewer."),
    ("human", "Given these features: {features}, list the cons of these features.")
  ])

  # just inject features into template and return
  return cons_template.format_prompt(features=features)

# runnables
pros_branch_runnable = RunnableLambda(lambda x: analyze_pros(features=x))
pros_branch_chain = pros_branch_runnable | llm | parser

cons_branch_runnable = RunnableLambda(lambda x: analyze_cons(features=x))
cons_branch_chain = cons_branch_runnable | llm | parser

# combine result of parallel branches
def combine_pros_cons(pros: any, cons: any) -> any:
  return f"pros:\n {pros}, \n\ncons: \n{cons}"

# runnable
merge_runnable = RunnableLambda(lambda x: combine_pros_cons(
  pros=x["pros"], 
  cons=x["cons"]))

# pipeline = prompt | llm | parser

# same thing as a chain
# pipeline = RunnableSequence(
#   first=get_features_prompt,
#   middle=[llm, parser], # middle parm => has to be a list of runnables
#   last=parser
# )

pipeline = (
  get_features_prompt 
  | llm
  | parser
  # run 2 tasks in parallel =: returns: dict: {pros, cons}
  | RunnableParallel(pros=pros_branch_chain, 
  cons=cons_branch_chain)
  # just print the output of parallel branch
  # use a tuple => to print and return
  | RunnableLambda(lambda output: (print(output), output)[1])
  # merge the result of parallel branches
  | merge_runnable
)

# chat loop 
while True:
  query = input("Enter a product name. or /exit\n")

  if query.lower() == "/exit":
    print("Goodbye!")
    break

  stream = pipeline.stream(
    input={"product_name": query},
  )

  # stream chunks of message
  for chunk in stream:
    print(chunk, end="", flush=True)

  print("\n")

