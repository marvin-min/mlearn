from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://python.langchain.com/en/latest/index.html")
data = loader.load()
print(data)