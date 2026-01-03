from sqlalchemy.engine import cursor

ALI_TONGYI_API_KEY_SYSVAR_NAME = "DASHSCOPE_API_KEY"
ALI_TONGYI_URL = "DASHSCOPE_BASE_URL"
ALI_TONGYI_RERANK = "gte-rerank-v2"
ALI_TONGYI_DEEPSEEK_R1 = "deepseek-r1"
ALI_TONGYI_EMBEDDING = "text-embedding-v3"
ALI_TONGYI_MAX_MODEL = "qwen-max-latest"
from dotenv import load_dotenv
load_dotenv()
from enum import Enum

class Constants(Enum):
  API_KEY_SYSVAR_NAME = ALI_TONGYI_API_KEY_SYSVAR_NAME
  BASE_URL = ALI_TONGYI_URL
  LLM_MODEL = ALI_TONGYI_MAX_MODEL
  EMBEDDING_MODEL = ALI_TONGYI_EMBEDDING
  RERANK_MODEL = ALI_TONGYI_RERANK
  REASONER_MODEL = ALI_TONGYI_DEEPSEEK_R1

import os
from langchain_openai import ChatOpenAI
from openai import OpenAI
import inspect

def get_normal_client(api_key=os.getenv(Constants.API_KEY_SYSVAR_NAME.value),
                      base_url=os.getenv(Constants.BASE_URL.value),
                      verbose=False,
                      debug=False):
  function_name = inspect.currentframe().f_code.co_name
  if(verbose):
    print(f"{function_name}:{base_url}")
  if(debug):
    print(f"{function_name}:{base_url},{api_key}")
  return OpenAI(api_key=api_key,base_url=base_url)