from products.models import Product
import pika
import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()


paramas = pika.URLParameters(
    'amqps://fodwhzka:iOXY-F11dMTsqctaUO_tjxADn0wjUWUU@kebnekaise.lmq.cloudamqp.com/fodwhzka')

connection = pika.BlockingConnection(paramas)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased!')


channel.basic_consume(
    queue='admin', on_message_callback=callback, auto_ack=True)

print('Started consuming...')

channel.start_consuming()

channel.close()
