
from langchain_core.runnables import RunnableLambda, RunnableParallel



def add_one(x):
    return x + 1


def multiply_by_two(x):
    return x * 2

def square(x):
    return x * x


p1 = RunnableLambda(add_one)
mul_2 = RunnableLambda(multiply_by_two)
sq= RunnableLambda(square)

chain = p1 | mul_2 | sq

print(chain.invoke(1))

chain2 = p1 | RunnableParallel(mul_2=mul_2, sq=sq)
print(chain2.invoke(1))