from operator import itemgetter

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import chain

from lc.models import get_client
from langchain_core.globals import set_debug
set_debug(True)
client = get_client()

tmplt = ChatPromptTemplate.from_template("{a} + {b}是多少？")
def lenth_func(text):
  return len(text)

def _multi_length_func(text,text2):
  return len(text) * len(text2)

@chain
def multi_length_func(_dict):
  return _multi_length_func(_dict["text"], _dict["text2"])

chain = tmplt | client

chain2 = ({
    "a": itemgetter("foo") | RunnableLambda(lenth_func),
    "b":  {"text": itemgetter("foo"), "text2":itemgetter("bar")} | multi_length_func
    } | chain
)
print(chain2.invoke({"foo": "123", "bar": "4567"}))