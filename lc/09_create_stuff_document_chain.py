import os
import bs4
import sys

# 1. 配置环境
os.environ["USER_AGENT"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

# 自定义模块
from models import get_client, get_embeddings

def summarize_web_page(url):
  """
  核心业务逻辑：抓取 -> 切分 -> 向量化 -> 检索 -> 总结
  """
  print(f"\n🚀 开始处理 URL: {url}")

  # --- A. 灵活抓取 ---
  # 优先尝试针对 gov.cn 等网站的选择器，若失败则全量抓取
  loader = WebBaseLoader(
    web_path=url,
    # bs_kwargs=dict(parse_only=bs4.SoupStrainer(id="UCAP-CONTENT"))
  )
  docs = loader.load()

  if not docs or not docs[0].page_content.strip():
    print("⚠️ 无法通过特定 ID 抓取内容，切换为全页面抓取模式...")
    loader.bs_kwargs = {}
    docs = loader.load()

  # --- B. 智能切分 ---
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
  documents = text_splitter.split_documents(docs)
  print(f"✅ 文档加载成功，已切分为 {len(documents)} 个片段")

  # --- C. 向量化存储 ---
  # 这里我们使用内存模式。如果需要存硬盘，可添加 persist_directory="./db"
  vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=get_embeddings()
  )

  # --- D. 检索增强生成 (RAG) ---
  # 这里的 k=8 确保了覆盖率，减少信息丢失
  retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

  prompt = ChatPromptTemplate.from_messages(
    [
      ("system", "你是一个专业的文案总结助手。请根据以下上下文内容进行总结。\n\n上下文：\n{context}"),
      ("user", "任务：{input}\n\n注意：请分条目列出核心要点,保持客观准确。"),
    ]
  )

  # 组装 Chain
  combine_docs_chain = create_stuff_documents_chain(get_client(), prompt)
  rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

  # --- E. Debug：检索内容验证 ---
  input_query = "总结这篇文章的核心内容"
  relevant_docs = retriever.invoke(input_query)

  print("\n[Debug] 检索到的原始片段预览:")
  for i, doc in enumerate(relevant_docs):
    # 兼容 Python 3.12 以下版本的 f-string 写法
    content_snippet = doc.page_content[:60].replace('\n', ' ')
    print(f"  [{i}] {content_snippet}...")

  # --- F. 执行总结 ---
  print("\n✍️ 正在生成总结报告...")
  res = rag_chain.invoke({"input": input_query})
  return res["answer"]


# --- 程序入口 ---
if __name__ == "__main__":
  # 方案 1：手动修改这里的参数
  target_url = 'https://www.active.com/affiliate'

  # 方案 2：支持从命令行参数读取 (例如: python script.py https://example.com)
  if len(sys.argv) > 1:
    target_url = sys.argv[1]

  try:
    final_summary = summarize_web_page(target_url)
    print("\n" + "ID" + "=" * 20 + " AI 总结结果 " + "=" * 20)
    print(final_summary)
  except Exception as e:
    print(f"❌ 程序运行出错: {e}")