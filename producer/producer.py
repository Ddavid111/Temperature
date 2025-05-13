import pika
import random
import time
import socket

def wait_for_rabbitmq(host, port):
    while True:
        try:
            with socket.create_connection((host, port), timeout=3):
                return
        except OSError:
            print("RabbitMQ not available, waiting...")
            time.sleep(3)

wait_for_rabbitmq('rabbitmq', 5672)

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='temperature')

while True:
    temp = random.randint(0, 100)
    channel.basic_publish(exchange='',
                          routing_key='temperature',
                          body=str(temp))
    print(f"Sent temperature: {temp}")
    time.sleep(2)