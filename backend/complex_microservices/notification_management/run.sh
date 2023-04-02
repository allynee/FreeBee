#!/bin/bash

exec python ./notification.py &
exec python ./amqp_setup.py
exec python ./amqpConsumer.py