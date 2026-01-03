import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="Qwen/Qwen2.5-72B-Instruct", api_key=os.getenv("SILICON_API_KEY"), base_url=os.getenv("SILICON_BASE_URL"))
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个AI领域的专家。"),
    ("user", "{input}")
])
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
output_parser = JsonOutputParser()
chain = prompt | llm | output_parser
messages = [HumanMessage(content="你好，请介绍一下你自己。")]
response = chain.invoke({"input": "大模型的原理是什么？问题用question,回答用answer。请用json格式回答"})
print(f"Response type: {type(response)}")
if isinstance(response, dict):
    print(f"Response keys: {response.keys()}")
print(response.answer)