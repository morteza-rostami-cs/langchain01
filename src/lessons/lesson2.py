
from src.lessons.base import init_ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = init_ollama()

#role: you are a helpful assistant. help me answering the query.
template = """
role: you are a writing assistant. help me to write a short story, about the topic! 

rules:
  - story has to to be MAX 100 tokens! NOT MORE!

topic: 
{topic}
"""

#input_variables=["topic"],
prompt = PromptTemplate.from_template(
  template=template
)

# | StrOutputParser()
chain = prompt | llm | StrOutputParser()

# get user input 
while True:
  # input
  topic = input("Enter a topic: , /exit\n")

  # user exit the loop
  if topic.lower() == "/exit":
    print("goodbye\n")
    break
  
  try:
    stream = chain.stream({"topic": topic})

    for chunk in stream:
      print(chunk, end="", flush=True)
  except Exception as e:
    print("failed streaming,", e)

  print("\n")
