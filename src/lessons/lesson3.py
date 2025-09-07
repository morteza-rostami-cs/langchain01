
"""
## on Runnables and chain

# what is a Runnable ?

Runnable is the core abstraction (like: a interface) for => components that process data.

for eg:
llm | prompt | output parser | custom python function wrapped as components

# so: basically you make a "chain" using bunch of Runnables

chain = prompt | llm | parser and ....




"""

from langchain_core.runnables import RunnableLambda
import asyncio
import time

# a simple function => doubles a number
def double(x: int) -> int:
  return x * 2

# wrap the normal function in a Runnable object
double_runnable = RunnableLambda(double) # a langchain component

# synchronous: invoke
result = double_runnable.invoke(5)
print("sync invoke: ", result)

# async: invoke
async def async_runnable():
  result = await double_runnable.ainvoke(7)
  print("async invoke: ", result)

# some other parallel task
# async def task1():
#   time.sleep(10)
#   print("some other parallel tasks")

#batch and abatch => process multiple inputs
results = double_runnable.batch([1, 2, 3, 4])
print("batch: ", results) # batch:  [2, 4, 6, 8]

# stream and astream
# underlying function/component => has to support incremental output (generator)

print("\n**********\n")
# input / output schemas => don't know what to do with them!!
print(double_runnable.input_schema)
print(double_runnable.output_schema)
print(double_runnable.config_schema)

print("\n**********\n")

#  all async tasks
async def run_async():
  try:
    # invoke runnable
    await async_runnable()
    # some other async task
    #await task1()

    # async batch
    results = await double_runnable.abatch([2, 3, 4])
    print("async btach: ", results) #async btach:  [4, 6, 8]

    # astream_log => print log of internal object
    # async for event in double_runnable.astream_log(12):
    #   print("astream_log event: ", event)

    print("End of all async tasks")
  except Exception as e:
    print("some async task failed")

#asyncio.run(run_async())

print("\nafter async...\n")

#the rest of Runnable 

# composition with LCEL => langchain expression language

# RunnableSequence

# chaining runnables => step by step => output of one becomes input for the next one.

from langchain_core.runnables import RunnableSequence

# some runnables
add_by_one = RunnableLambda(func=lambda x: x + 1)
multi_by_two = RunnableLambda(lambda x: x * 2)

# chain Runnables
chain = add_by_one | multi_by_two 

res = chain.invoke(1)
print(res)#4

# also use RunnableSequence
chain2 = RunnableSequence(add_by_one, multi_by_two)
res2 = chain.invoke(2)
print(res2) #6

#===============
# RunnablePassthrough

from langchain_core.runnables import RunnablePassthrough

uppercase = RunnableLambda(lambda x: x.upper())

#combine with passthrough
pipeline = {
  # pass through => just passes the original value->maybe for debug
  "original": RunnablePassthrough(),
  "uppercase": uppercase,
}

res3 = pipeline | RunnableLambda(lambda d: d)
print(res3.invoke("hello"))
#{'original': 'hello', 'uppercase': 'HELLO'}

#============
from langchain_core.runnables.base import RunnableEach

double_runnable = RunnableLambda(lambda x: x * 2)

# applies a runnable to each element of a list
double_each = RunnableEach(bound=double_runnable)

#Run on a list
result = double_each.invoke([1, 2, 3, 4])
print(result) #[2, 4, 6, 8]

# async version
# await double_each.ainvoke([2, 3, 4])