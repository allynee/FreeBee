FROM python:3-slim
WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD [ "sh", "-c", "python notification_management.py & python amqpConsumer.py" ]

