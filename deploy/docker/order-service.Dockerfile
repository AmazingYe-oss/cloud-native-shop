FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY services/order-service/requirements.txt /app/
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY services/order-service/ /app/
EXPOSE 8000
CMD [ "uvicorn","main:app","--host","0.0.0.0","--port","8000" ]