

exec python ./notification.py &
printf "notification service started"
exec python ./amqp_setup.py
printf "amqp setup started"
exec python ./amqpConsumer.py
printf "amqp consumer started"