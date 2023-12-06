FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./transaction_management.py .
COPY ./invokes.py .
COPY ./amqp_setup.py .
CMD [ "python", "./transaction_management.py" ]