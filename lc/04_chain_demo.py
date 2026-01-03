from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from lc.models import get_client
# from langchain_core.globals import set_debug
# set_debug(True)
client = get_client()
from langserve import add_routes

def arr_temp():
  #roles: system, user, assistant（大模型应答消息，需要调用历史聊天的时候需要）
  chat_template = ChatPromptTemplate.from_messages(
    [
      ("system", "请将一下内容翻译成{language}"),
      HumanMessagePromptTemplate.from_template("{text}")
      # ('human', "{text}")
    ]
  )
  parser = StrOutputParser()
  chain = chat_template | client | parser
  return chain
# arr_temp()
chain = arr_temp()
app = FastAPI(title="LangChain Demo", version="0.0.1", description="LangChain Demo")

add_routes(app,chain, path='/trans')

# POST /trans/invoke HTTP/1.1
# Host: 0.0.0.0:8000
# Content-Type: application/json
#
# {"input":{"language":"中文","text":"I am good"}}
if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)