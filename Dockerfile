# 使用官方 Python
FROM python

# 設置工作目錄
WORKDIR /app

# 複製 requirements.txt 到容器中
COPY requirements.txt .

# 安裝應用所需的依賴
RUN pip install -r requirements.txt

# 複製應用程式代碼到容器中
COPY . .

# 暴露應用所需的端口
EXPOSE 5000

# 設置容器啟動命令
CMD ["python", "app.py"]