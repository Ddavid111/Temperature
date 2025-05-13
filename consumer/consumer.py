import pika
import socket
import time

def wait_for_rabbitmq(host, port):
    while True:
        try:
            with socket.create_connection((host, port), timeout=3):
                return
        except OSError:
            print("RabbitMQ nem elérhető, várakozás...")
            time.sleep(3)

wait_for_rabbitmq('rabbitmq', 5672)

high_temp_count = 0

def callback(ch, method, properties, body):
    global high_temp_count
    temperature = int(body)
    if temperature > 50:
        high_temp_count += 1
        print(f"[Processor] Magas hőmérséklet: {temperature} (Szám: {high_temp_count})")
        if high_temp_count == 10:
            ch.basic_publish(exchange='',
                             routing_key='temperatureStatistics',
                             body='10db Magas hőmérséklet üzenet feldolgozva')
            high_temp_count = 0

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='temperature')
channel.queue_declare(queue='temperatureStatistics')

channel.basic_consume(queue='temperature',
                      on_message_callback=callback,
                      auto_ack=True)

print('[Processor] Várakozás üzenetekre...')
channel.start_consuming()