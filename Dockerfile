# 使用官方Python镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（如果需要）
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements.txt并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口（如果你的应用是一个Web服务）
EXPOSE 8000

# 设置环境变量（根据需要调整）
ENV DASHSCOPE_API_KEY=""
ENV DASHSCOPE_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
ENV DASHSCOPE_MODEL_NAME="qwen-turbo"

# 运行应用
CMD ["python", "app.py"]