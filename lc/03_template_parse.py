from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

from lc.models import get_client

client = get_client()

def arr_temp():
  #roles: system, user, assistant（大模型应答消息，需要调用历史聊天的时候需要）
  chat_template = ChatPromptTemplate.from_messages(
    [
      ("system", "请将一下内容翻译成{language}，并造一个句子"),
      HumanMessagePromptTemplate.from_template("{text}")
      # ('human', "{text}")
    ]
  )
  parser = StrOutputParser()
  rs=client.invoke(chat_template.format(language="意大利", text="你好"))
  print(parser.invoke(rs))
arr_temp()
