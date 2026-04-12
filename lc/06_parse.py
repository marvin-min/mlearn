from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from lc.models import get_client
# from langchain_core.globals import set_debug
# set_debug(True)
client = get_client()

def arr_temp():
  #roles: system, user, assistant（大模型应答消息，需要调用历史聊天的时候需要）
  chat_template = ChatPromptTemplate.from_messages(
    [
      ("system", "请将一下内容翻译成{language}，用json输出,输入用origin,输出用output"),
      HumanMessagePromptTemplate.from_template("{text}")
      # ('human', "{text}")
    ]
  )
  # parser = StrOutputParser()
  parser = JsonOutputParser()
  chain = chat_template | client | parser
  return chain.invoke({"language": "英文", "text": "你是谁?"})

rs=arr_temp()
print(rs)
print(type(rs))