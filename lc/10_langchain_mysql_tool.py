from operator import itemgetter

from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.tools import TavilySearchResults, QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import re

from langchain_core.runnables import RunnablePassthrough

from lc.models import get_client,debug_mode
import pymysql
pymysql.install_as_MySQLdb()  # 这行是核心，让PyMySQL兼容mysqlclient接口
debug_mode(False)
client = get_client()

#langchain mysql
from langchain.agents import Tool

#写出langchain操作mysql数据库代码
username = "root"
password = "password"
MYSQL_URL = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8mb4'.format(username, password, "localhost", "3306", "awm")
db =SQLDatabase.from_uri(MYSQL_URL)

def get_table_names():
    return db.get_table_names()

get_table_name_tool = Tool(
  name="获取表名",
  func=get_table_names,
  description="获取数据库中所有表的表名",
)

class SQLCleaner(StrOutputParser):
  def parse(self, text: str) -> str:
    pattern = r'(?i)\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)\b[\s\S]*?;'
    match = re.search(pattern, text)

    if match:
      # 提取匹配的SQL，并去除首尾多余空白
      sql = match.group(0).strip()
      return sql
    else:
      # 如果没有找到以分号结束的语句，尝试匹配到文本末尾
      pattern_no_semicolon = r'(?i)\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)\b[\s\S]*'
      match = re.search(pattern_no_semicolon, text)
      if match:
        return match.group(0).strip()

sql_chain = create_sql_query_chain(client,db) | SQLCleaner()
# result = sql_chain.invoke({"question":"从文章表中查出第一条记录"})
# print("产生的sql语句:", result)
# print("*"*15)

# client_with_tools =client.bind_tools([get_table_name_tool])
# resp = client_with_tools.invoke([HumanMessage(content="请从文章表中查出第一行数据")])
# print(resp.content)
# print(resp.tool_calls)
execute_sql_tools = QuerySQLDataBaseTool(db=db)
answer_prompt = PromptTemplate.from_template(
        """给定以下用户问题，可用的SQL语句和SQL执行后的结果，回答用户问题：
        Question:{question}
        SQL Query:{query}
        SQL Result:{result}
        回答:""")
chain = (RunnablePassthrough.assign(query=sql_chain).assign(result=itemgetter('query')|execute_sql_tools)
         |answer_prompt|client|StrOutputParser())
result = chain.invoke({"question":"从文章表中查出第倒数第三条记录"})
print(result)