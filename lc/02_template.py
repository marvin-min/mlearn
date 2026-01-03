from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

from lc.models import get_client

client = get_client()

def str_temp():
  template_str = "您是一位专业的程序员。\n对于信息{text}进行简单描述"
  fact_text = "langchain"
  prompt = PromptTemplate.from_template(template_str)

  rs = client.invoke(prompt.format(text=fact_text))
  print(rs)

def arr_temp():
  #roles: system, user, assistant（大模型应答消息，需要调用历史聊天的时候需要）
  chat_template = ChatPromptTemplate.from_messages(
    [
      ("system", "请将一下内容翻译成{language}"),
      HumanMessagePromptTemplate.from_template("{text}")
      # ('human', "{text}")
    ]
  )
  rs=client.invoke(chat_template.format(language="意大利", text="你好"))
  print(rs.content)
arr_temp()
