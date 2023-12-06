FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY notification_management.py /usr/src/app/
COPY amqpConsumer.py /usr/src/app/
COPY amqp_setup.py /usr/src/app/
COPY invokes.py /usr/src/app/
CMD [ "sh", "-c", "python notification_management.py & python amqpConsumer.py" ]


# FROM python:3-slim
# WORKDIR /usr/src/app
# COPY requirements.txt ./
# RUN python -m pip install --no-cache-dir -r requirements.txt
# COPY ./notification_management.py ./amqpConsumer ./amqp_setup.py ./
# CMD [ "python", "notification_management.py", "amqpConsumer.py" ]



# FROM python:3-slim
# WORKDIR /app
# COPY requirements.txt ./
# RUN python -m pip install --no-cache-dir -r requirements.txt
# COPY . /app
# CMD [ "sh", "-c", "python amqpConsumer.py & python notification_management.py" ]



