#!/bin/bash
set -e

HOST="rabbitmq"

until curl -sL "http://$HOST:15672" -o /dev/null
do
    echo "Waiting for RabbitMQ..."
    sleep 1
done

echo "RabbitMQ is ready!"

