from lc.models import get_client

msg = [
    # {"role": "system", "content": "翻译下面句子，如果是英文翻译成中文，如果是中文翻译成英文"},
    # {"role": "user", "content": "666"}
    ('system',"翻译下面句子，如果是英文翻译成中文，如果是中文翻译成英文"),
    ('human', "Hello, world!")
]
client = get_client()
rs = client.invoke(msg)
print(rs)
print("翻译结果:", rs.content)
