#实战项目1： 基于提示工程 TOT Paper 24点计算实战
# pip install openai
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

from game24_prompt import propose_prompt, value_prompt

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
client = OpenAI(api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",)

#model选用“qwen2.5-coder-3b-instruct”最快，“qwen-coder-plus-lates”其次，"qwen-max/turbo"等极慢
def chatgpt(prompt, model="qwen2.5-coder-3b-instruct") -> list:
    messages = [{"role": "user", "content": prompt}]
    outputs = []
    res = client.chat.completions.create(model=model, messages=messages)
    # print('res:',res)
    outputs.extend([choice.message.content for choice in res.choices])
    print('outputs:',outputs)
    return outputs
#第一轮计算
def first_think(input):
    #将输入的字符串以‘\n’，分割转换为列表
    proposals = chatgpt(propose_prompt.format(input=input))[0].split('\n')
    # print(len(proposals))
    # print(proposals)
    # # 每个元素后加上\n （为了拼接后续步骤）
    # # [2 + 8 = 10 (left: 8 10 14)\n,8 / 2 = 4 (left: 4 8 14)\n]
    proposals = [_ + '\n' for _ in proposals]
    print('first_think_proposals:',proposals)
    # # # 创建对应的index list
    ids = list(range(len(proposals)))
    print('first_think_ids:',ids)
    return (ids,proposals)
#分析
def first_evaluate(proposals):
    values = []
    for proposal in proposals:
        #proposal形如 '5 + 8 = 13 (left: 11 13)\n'，取出 left和 )之间的数字
        current_numbers = proposal.strip().split('\n')[-1].split('left: ')[-1].split(')')[0]
        print('first_evaluate_current_numbers:',current_numbers)
        if current_numbers in value_cache:
            values.append(0)
            print('continue loop and first_scores:', values)
            continue
        value_outputs = chatgpt(value_prompt.format(input=current_numbers))
        print(value_outputs,'first_evaluate_value_outputs')
        print('first_evaluate_current_numbers_2：',current_numbers)
        value_cache.append(current_numbers)
        print('value_cache:',value_cache)
        value = 0
        try:
            value = sum([float(_.split('\n')[-1].split('left: ')[-1]) for _ in value_outputs])
        except:
            pass
        values.append(value)
        print('first_values_2:', values)
        # 日志
        temp = proposal.replace("\n", "\\n")
        print(f"[{temp}] 得分: {value}")
    return values
#预测
def first_screen(ids,values):
    # 根据预测结果选择前5个最有可能到达24的候选项
    # 按照评级排序下一步动作的index 并记录对应的下一步动作
    select_ids = sorted(ids, key=lambda i: values[i], reverse=True)[:5]
    select_proposals = [proposals[select_id] for select_id in select_ids]
    print('first_screen_select_proposals:', select_proposals)
    return select_proposals

#剩下3个数

def second_think(select_proposals):
    # 获得可能的下一步动作
    proposals = []
    for proposal in select_proposals:
        # 从第一轮候选结果中取出数组 获取下一步
        # 2 * 3 = 6 (left: 2 2 6)\n -》 2 2 6
        current_numbers = proposal.strip().split('\n')[-1].split('left: ')[-1].split(')')[0]
        print('second_think_current_numbers：', current_numbers)
        # 2 + 2 = 4 (left: 4 6)\n
        # 2 * 2 = 4 (left: 4 6)\n
        # 6 - 2 = 4 (left: 2 4)\n
        p = chatgpt(propose_prompt.format(input=current_numbers))[0].split('\n')
        # 将第一步的结果和本次拼接
        # ['2 * 3 = 6 (left: 2 2 6)\n2 + 2 = 4 (left: 4 6)\n','2 * 3 = 6 (left: 2 2 6)\n6 - 2 = 4 (left: 2 4)\n']
        for item in p:
            proposals.append(proposal + item + '\n')

    ids = list(range(len(proposals)))
    print('second_think_ids：', ids)
    return (ids,proposals)

def second_evaluate(proposals):
    values = []
    for proposal in proposals:
        current_numbers = proposal.strip().split('\n')[-1].split('left: ')[-1].split(')')[0]
        print('second_evaluate_current_numbers：', current_numbers)
        if current_numbers in value_cache:
            # print(f"{current_numbers}已评估")
            values.append(0)
            print('continue loop and second_score:', values)
            continue
        # print(f"评估:{current_numbers}...")
        value_outputs = chatgpt(value_prompt.format(input=current_numbers))
        value_cache.append(current_numbers)
        value = 0
        try:
            print('second_evaluate_value_outputs',value_outputs)
            value = sum([float(_.split('\n')[-1].split('left: ')[-1]) for _ in value_outputs])
            print('second_evaluate_score:',value)
        except:
            pass
        values.append(value)
        # 日志
        temp = proposal.replace("\n", "\\n")
        print(f"[{temp}] 得分: {value}")
        print('second_evaluate_score:', values)
    return values

def second_screen(values):
    select_ids = sorted(ids, key=lambda i: values[i], reverse=True)[:5]
    select_proposals = [proposals[select_id] for select_id in select_ids]
    print('second_screen_select_proposals:', select_proposals)
    return select_proposals

#剩下2个数
def third_think(select_proposals):
    # 获得可能的下一步动作
    proposals = []
    for proposal in select_proposals:
        current_numbers = proposal.strip().split('\n')[-1].split('left: ')[-1].split(')')[0]
        p = chatgpt(propose_prompt.format(input=current_numbers))[0].split('\n')
        for item in p:
            proposals.append(proposal + item + '\n')
    return proposals

def third_evaluate(proposals):
    result = []
    for proposal in proposals:
        current_numbers = proposal.strip().split('\n')[-1].split('left: ')[-1].split(')')[0]
        if current_numbers == '24':
            result.append(proposal)
    return result

#是不是24，已经有结果
def GetResult(result):
    print(f"输入的数字为：{input}。")
    if len(result) == 0:
        print("无法获得24")
    else:
        print("获得24的算式有:")
        for r in result:
            print("=================")
            print(r)

# 程序主入口
if __name__ == '__main__':
    value_cache= []
    input = "5 8 11 13"
    print("第一轮：思考生成中......")
    ids,proposals = first_think(input)
    print("第一轮思考完毕，结果：",ids,proposals)

    print("第一轮：评估结果中......")
    values = first_evaluate(proposals)
    print("第一轮评估完毕，结果：", values)

    print("第一轮：筛选候选项......")
    select_proposals = first_screen(ids,values)
    print("第一轮候选项筛选完毕，结果：", select_proposals)

    print("第二轮：思考生成中......")
    ids,proposals = second_think(select_proposals)
    print('第二轮思考完毕，结果：',proposals)

    print("第二轮：评估结果中......")
    values = second_evaluate(proposals)
    print("第二轮评估完毕，结果：", values)

    print("第二轮：筛选候选项中......")
    select_proposals = second_screen(values)
    print("第二轮候选项筛选完毕，结果：", select_proposals)

    print("第三轮：思考生成中......")
    proposals= third_think(select_proposals)
    print("第三轮思考完毕，结果：",proposals)

    print("第三轮：评估结果中......")
    result = third_evaluate(proposals)
    print("第三轮评估完毕，结果：", result)

    print('获取最终结果结果......')
    GetResult(result)
