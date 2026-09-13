FROM python:3.10
WORKDIR /app

# 【终极绝招】直接把所有需要的库写在安装命令里，不再读取 requirements.txt，避免任何文件名/格式问题！
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple nicegui pandas numpy statsmodels

# 复制项目剩余文件
COPY . .

EXPOSE 8080
CMD ["sh", "-c", "python app_nicegui.py"]