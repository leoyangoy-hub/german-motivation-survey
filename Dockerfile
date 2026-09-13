FROM zauberzeug/nicegui:latest
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "app_nicegui.py"]