import pika
import time
import traceback
import json
from core.core import run
import os


rabbitmq_hostserver = os.getenv('RABBITMQ_HOSTSERVER')
rabbitmq_password = os.getenv('RABBITMQ_PASSWORD')
rabbitmq_username = os.getenv('RABBITMQ_USERNAME')
rabbitmq_followers_exchange = os.getenv('RABBITMQ_FOLLOWERS_EXCHANGE')
rabbitmq_followers_exchange_type = os.getenv('RABBITMQ_FOLLOWERS_EXCHANGE_TYPE')
rabbitmq_followers_queue_name = os.getenv('RABBITMQ_FOLLOWERS_QUEUE_NAME')
rabbitmq_followers_routing_key = os.getenv('RABBITMQ_FOLLOWERS_ROUTING_KEY')

def create_channel_connection():
    credentials = pika.PlainCredentials(rabbitmq_username,rabbitmq_password)
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_hostserver, credentials=credentials))
    channel = connection.channel()
    
    return channel, connection


def callback(ch, method, properties, body):
    #print(" [x] Received %r" % body.decode())
    #print(type(body.decode()))
    dict_data = json.loads(body.decode())
    try:
        _ = run(dict_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("Done")
    except:
        traceback.print_exc()
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    channel, connection = create_channel_connection()
    channel.queue_declare(queue=rabbitmq_followers_queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=rabbitmq_followers_queue_name, on_message_callback=callback)
    print("started")
    channel.start_consuming()