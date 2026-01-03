from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, FewShotPromptTemplate
from lc.models import get_client
# from langchain_core.globals import set_debug
# set_debug(True)
client = get_client()
examples = [
  {"sinput": "2+2", "soutput": "4", "sdescription":"加法运算"},
  {"sinput": "5-2", "soutput": "3", "sdescription":"减法运算"}
]

examples_prompt_tmplt_str ="算式:{sinput} 值: {soutput} 类型:{sdescription}"
prompt_sample = PromptTemplate.from_template(examples_prompt_tmplt_str)
prefix="你是一个数学专家,能够准确的说出算是的类型,"
suffix="现在给你算是:{input}, 值:{output}, 告诉我类型："
prompt = FewShotPromptTemplate(
  example_prompt=prompt_sample,
  examples=examples,
  prefix=prefix,
  suffix=suffix,
  input_variables=["input", "output"],
  example_separator="\n"
)

print(client.invoke(prompt.format(input="3*2", output="6")))
