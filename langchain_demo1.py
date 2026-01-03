import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="Qwen/Qwen2.5-72B-Instruct", api_key=os.getenv("SILICON_API_KEY"), base_url=os.getenv("SILICON_BASE_URL"))
from langchain_core.messages import HumanMessage
messages = [HumanMessage(content="你好，请介绍一下你自己。")]
response = llm.invoke("大模型有啥作用？你的版本是多少？")
print(response.content)