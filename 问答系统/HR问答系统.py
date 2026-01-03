from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import chromadb
from chromadb.config import Settings
from docx import Document
from models import get_normal_client, Constants

client = get_normal_client()


def extract_text_from_docx(file_name, min_line_length=1):
  """
   从 DOCX 文件中提取文字

   思路：
   1. 使用 python-docx 库读取文档
   2. 提取所有段落的原始文本
   3. 按空行分割并重组段落
   4. 过滤短行（假设为标题）
   5. 处理英文连字符情况

   参数：
   filename: DOCX文件路径
   min_line_length: 最小行长度，短于此长度的行将被视为段落分隔符

   返回：
   段落列表（每个元素为一个段落字符串）
   """
  texts = []
  paragraphs=[]
  buffer = ''
  document = Document(file_name)
  for para in document.paragraphs:
    texts.append(para.text)
  full_text = '\n'.join(texts)
  lines = full_text.split('\n')
  for line in lines:
    #处理有效行
    if(len(line)) >= min_line_length:
      #处理连字符
      if not line.endswith('.'):
        buffer += ' ' + line
      else:
        buffer = line.strip('-')
    elif buffer:
      paragraphs.append(buffer.strip())
      buffer = ''
  if buffer:
    paragraphs.append(buffer.strip())
  return paragraphs

paragraphs = extract_text_from_docx('人事管理流程.docx', 10)
print(paragraphs)

class MyVectorDBConnector:
  def __init__(self, collection_name, embedding_function):
    chroma_client = chromadb.Client(
      Settings(
        allow_reset=True,
        anonymized_telemetry=False,
          ))
    self.collection = chroma_client.get_or_create_collection(
      name=collection_name,
    )
    self.embedding_function = embedding_function

  def add_documents(self, documents):
    '''
    collection到文档中
    '''
    batch_size = 10
    for i in range(0, len(documents), batch_size):
      batch_docs = documents[i:i+batch_size]
      self.collection.add(
        embeddings=self.embedding_function(batch_docs),
        documents=batch_docs,
        ids=[f"id{i}" for i in range(i, i+len(batch_docs))]
      )
  def search(self, query, top_n):
    '''检索向量数据库'''
    results = self.collection.query(
      query_embeddings=self.embedding_function([query]),
      n_results=top_n,
      )
    return results
def get_embeddings(texts,model=Constants.EMBEDDING_MODEL.value):
  data =client.embeddings.create(input=texts,model=model).data
  return [x.embedding for x in data]

vector_db = MyVectorDBConnector('hr_db', get_embeddings)
vector_db.add_documents(paragraphs)
def get_completion(prompt, model = Constants.LLM_MODEL.value):
  messages=[{'role':'user',"content": prompt}]
  response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0
  )
  return response.choices[0].message.content

prompt_template = """
你是一个问答机器人。
你的任务是根据下述给定的已知信息回答用户问题。
确保你的回复完全依据下述已知信息。不要编造答案。
如果下述已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。

已知信息:
__INFO__

用户问：
__QUERY__

请用中文回答用户问题。
"""
# 给Prompt 模板赋值
def build_prompt(prompt_template, **kwargs):
    '''将 Prompt 模板赋值'''
    prompt = prompt_template
    for k, v in kwargs.items():
        if isinstance(v, str):
            val = v
        elif isinstance(v, list) and all(isinstance(elem, str) for elem in v):
            val = '\n'.join(v)
        else:
            val = str(v)
            # 返回转换为大写的字符串副本
        prompt = prompt.replace(f"__{k.upper()}__", val)
    return prompt

# 定义 chat 函数
def rag_chat(vector_db,llm_api,user_query,n_results=2):
    # 1.检索
    search_results = vector_db.search(user_query, n_results)
    # 2.构建提示词模板build_prompt
    prompt =  build_prompt(prompt_template,info=search_results['documents'][0],query=user_query)
    # 3,调用LLM模型方法生成回答
    response=llm_api(prompt)
    return response
user_query =  '那些情况扣工资？'
response =  rag_chat(vector_db,get_completion,user_query)
print(response)