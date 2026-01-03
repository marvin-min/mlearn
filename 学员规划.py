import gradio as gr
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def coach_student(qa1, qa2, qa3, qa4, qa5, model='qwen-plus'):
  instruction = """
  你是一位专业的大模型辅导老师，为学员提供个性化的学习建议，帮助他们更好地掌握大模型知识和技能。
  请回答的时候不要过多描述 言简意赅 
  """
  examples = """
         # 示例1
         Q：您现在在那个城市，是否在职，所从事的工作是什么？
         A：北京，在实习，算法工程师实习
         Q：对大模型有多少认知，了解多少原理与技术点？
         A：大模型应用到的基础深度学习知识都知道，cv方面比较熟悉，nlp方面不熟悉。常见的一些大模型相关术语了解，但不深入。
         Q：学习大模型的最核心需求是什么？
         A：目前工作需要用大模型进行训练，需要微调然后部署
         Q：是否有python编程基础或者其他编程基础，有没有写过代码？
         A：有Python基础，能看懂代码，但直接编写代码不熟练
         Q：每天能花多少时间用于学习，大致空闲时间点处于什么时段?
         A：周内中午12到2点，晚上9到11点。周末全天。
         Q：除以上五点外是否还有其他问题想要补充。如有请按照如下格式进行补充
         主要需要学习多模态大模型。纯nlp大模型不太需要。


         回复:作为一名在北京实习的算法工程师，对大模型在基础深度学习方面有一定的了解，
         对于计算机视觉（CV）领域比较熟悉，但在自然语言处理（NLP）方面还比较浅。
         使用大模型进行训练、微调并部署，这是你学习大模型的核心需求。你有 Python
         基础，能够理解代码，这对于大模型学习是个很好的基础，因为大模型使用到的
         主要编程语言就是 Python。你每天基本上都可以安排大约 3 个小时的学习时间，
         这样的安排有利于系统地学习以及去进行实践。此外，你主要需要学习多模态大
         模型，这使得你的学习更加有针对性。国内现在 AI 领域虽然处于起步阶段，但
         随着人工智能技术的快速发展，其应用前景非常广阔，凭借你的编程基础和明确
         的学习目标，转型为高效的 AI 工程师是完全可行的


         # 示例2
         Q：您现在在那个城市，是否在职，所从事的工作是什么？
         A：北京，在职，农业相关
         Q：对大模型有多少认知，了解多少原理与技术点？
         A：比较浅薄
         Q：学习大模型的最核心需求是什么？
         A：个人能力提升和业务需要
         Q：是否有python编程基础或者其他编程基础，有没有写过代码？
         A：有
         Q：每天能花多少时间用于学习，大致空闲时间点处于什么时段?
         A：3个小时左右，晚上18点以后
         Q：除以上五点外是否还有其他问题想要补充。如有请按照如下格式进行补充

         回复:作为在北京从事农业相关工作的同学，虽然你对大模型的认知程度比较浅，但你
         拥有 Python 编程基础并且写过代码，这对于学习大模型来说是很好的条件，因
         为 Python 是学习大模型的主要语言。推荐你看一下我们提供的预习课程来补充
         一下知识体系。个人能力提升和业务需要符合当前 AI 在农业领域的发展趋势。
         每天在晚上 18 点以后可以安排约 3 个小时的学习时间，这样的时间安排非常充
         裕。凭借你的编程背景和学习投入，转型为 AI 项目管理是可行的，国内现在 AI
         领域虽然处于起步阶段，但随着人工智能技术的快速发展，其应用前景非常广阔，
         现在正是学习并把握行业发展机遇的好时机。
     """
  user_input = f"""
     Q：您现在在那个城市，是否在职，所从事的工作是什么？
     A：{qa1}
     Q：对大模型有多少认知，了解多少原理与技术点？
     A：{qa2}
     Q：学习大模型的最核心需求是什么？
     A：{qa3}
     Q：是否有python编程基础或者其他编程基础，有没有写过代码？
     A：{qa4}
     Q：每天能花多少时间用于学习，大致空闲时间点处于什么时段?
     A：{qa5}
     """
  prompt = f"""
         {instruction}
         {examples}
         用户输入：
         {user_input}
     """
  print(prompt)
  messages = [{"role": "user", "content": prompt}, {"role": "user", "content": prompt}]
  response = client.chat.completions.create(model=model, messages=messages, temperature=0,n=4)
  return response.choices[0].message.content

with gr.Blocks() as demo:
  gr.Markdown("# 基于提示词工程的学员辅导系统")
  gr.Markdown("##为了给同学们做一个比较好的入学辅导，请根据如下问题准确进行回答！")
  questions = [
    "1. 您现在在那个城市，是否在职，所从事的工作是什么？",
    "2. 对大模型有多少认知，了解多少原理与技术点？",
    "3. 学习大模型的最核心需求是什么？",
    "4. 是否有python编程基础或其它编程基础，有没有写过代码？",
    "5. 每天能花多少时间用于学习，大致空闲时间处于什么时段？"
  ]
  q1_input = gr.Textbox(label=questions[0])
  q2_input = gr.Textbox(label=questions[1])
  q3_input = gr.Textbox(label=questions[2])
  q4_input = gr.Textbox(label=questions[3])
  q5_input = gr.Textbox(label=questions[4])
  submit = gr.Button("提交")
  results = gr.Textbox(label="辅导结果", placeholder="点击辅导按钮后显示结果", lines=10)
  submit.click(coach_student,inputs=[q1_input, q2_input, q3_input, q4_input, q5_input],outputs=results)
demo.launch(server_port=9090,share=True)