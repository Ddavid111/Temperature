import pika
import socket
import time

def wait_for_rabbitmq(host, port):
    while True:
        try:
            with socket.create_connection((host, port), timeout=3):
                return
        except OSError:
            print("RabbitMQ not available, waiting...")
            time.sleep(3)

wait_for_rabbitmq('rabbitmq', 5672)

def callback(ch, method, properties, body):
    print(f"Statistic: {body.decode()}")

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='temperatureStatistics')

channel.basic_consume(queue='temperatureStatistics',
                      on_message_callback=callback,
                      auto_ack=True)

print('Waiting for statistics...')
channel.start_consuming()