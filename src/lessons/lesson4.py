
# more on Runnable

# a call fails => errorHandling & retry

# inspect how a pipeline works

# debug + callbacks

from langchain_core.runnables import RunnableLambda
import random

def sometimes_fails(x: int) -> int:
  if random.random() < 0.5:
    raise ValueError("sometimes error!")
  return x * 2

flaky_runnable = RunnableLambda(sometimes_fails)

# add retry behavior: try 3 times, exponential backoff

retry_runnable = flaky_runnable.with_retry(
  stop_after_attempt=3,
  wait_exponential_jitter=True
)

# no need for try and except
# print(retry_runnable.invoke(5))# 10

#=============
#bind a parameter permanently

def format_story(data: any, style="short") -> str:
  topic = data["topic"] or None
  if not topic:
    raise Exception("no topic!")

  return f"a {style} story about {topic}"

# create a runnable
story_runnable = RunnableLambda(format_story)

# bind a value to style param => this runnable always returns funny story
funny_story = story_runnable.bind(style="funny")

print(funny_story.invoke({"topic": "cats"}))

#================
# visualize graph

double_runnable = RunnableLambda(lambda x: x * 2)
square_runnable = RunnableLambda(lambda x: x ** 2)

pipeline = double_runnable | square_runnable

#export graph
# install => grandalf => then graph works
# graph = pipeline.get_graph()
# graph.print_ascii()

runnable = RunnableLambda(lambda x: {"number": x})

# add extra keys to output dict
extended = runnable.assign(double=lambda d: d["number"] * 2)

print(extended.invoke(5)) # {'number': 5, 'double': 10}

#===================
# enforce input/output types

from typing import TypedDict

class Input(TypedDict):
  text: str

class Output(TypedDict):
  length: int

runnable = RunnableLambda(lambda x: {"length": len(x["text"])})

typed_runnable = runnable.with_types(input_type=Input, output_type=Output)

try:
  print(typed_runnable.invoke({"text": "hello"})) #{'length': 5}

  # wrong input
  #print(typed_runnable.invoke({'sex': 1}))
except Exception as e:
  print("failed typed_runnable", e)

print("\n**************\n")

# error handling
from langchain_core.globals import set_debug
from langchain_core.tracers import ConsoleCallbackHandler

# global debug on
set_debug(True)

runnable = RunnableLambda(lambda x: x * 2)

# Attach callback to just this run
runnable.invoke(5, config={"callbacks": [ConsoleCallbackHandler()]})

"""
[chain/start] [chain:RunnableLambda] Entering Chain run with input:
{
  "input": 5
}
[chain/end] [chain:RunnableLambda] [0ms] Exiting Chain run with output:
{
  "output": 10
}
"""

# runs two tasks in parallel and => return a results dict
from langchain_core.runnables import RunnableParallel

# multiple runnables in parallel => return all their results in one dict

runnable_parallel = RunnableParallel(
  double=RunnableLambda(lambda x: x * 2),
  triple=RunnableLambda(lambda x: x * 3)
)

print(runnable_parallel.invoke(4))
"""
{
  "double": 8,
  "triple": 12
}
"""