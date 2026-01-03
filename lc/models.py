import os
import dotenv
dotenv.load_dotenv()

from langchain_openai import ChatOpenAI
os.environ["LANGCHAIN_VERBOSE"] = "true"

DASHSCOPE_API_KEY=os.getenv("DASHSCOPE_API_KEY")
DASHSCOPE_BASE_URL=os.getenv("DASHSCOPE_BASE_URL")
DASHSCOPE_MODEL_NAME=os.getenv("DASHSCOPE_MODEL_NAME")
# # 验证环境变量
# print(f"API Key: {'已设置' if MODEL_API_KEY else '未设置'}")
# print(f"Base URL: {BASE_URL}")
# print(f"Model Name: {MODEL_NAME}")
def get_client(api_key=DASHSCOPE_API_KEY, base_url=DASHSCOPE_BASE_URL, model_name=DASHSCOPE_MODEL_NAME):
  client = ChatOpenAI(api_key=api_key,
                      base_url=base_url,
                      model=model_name)
  return client
