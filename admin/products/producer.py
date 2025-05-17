import pika
import json
paramas = pika.URLParameters(
    'amqps://fodwhzka:iOXY-F11dMTsqctaUO_tjxADn0wjUWUU@kebnekaise.lmq.cloudamqp.com/fodwhzka')

connection = pika.BlockingConnection(paramas)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='', routing_key='main', body=json.dumps(body), properties=properties)
