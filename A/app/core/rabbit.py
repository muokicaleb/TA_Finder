import json
import sys
import traceback
import pika
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


def add_followers(dictdata):
    try:
        channel, connection = create_channel_connection()
        channel.queue_declare(queue=rabbitmq_followers_queue_name, durable=True)

        channel.basic_publish(
                            exchange='',
                            routing_key=rabbitmq_followers_routing_key,
                            body=json.dumps(dictdata),
                            properties=pika.BasicProperties(
                                delivery_mode=2,  # make message persistent
                            ))


        connection.close()
        return True
    except:
        traceback.print_exc()

        return False

