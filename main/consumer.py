import pika
import json

from main import db, Product, app

paramas = pika.URLParameters(
    'amqps://fodwhzka:iOXY-F11dMTsqctaUO_tjxADn0wjUWUU@kebnekaise.lmq.cloudamqp.com/fodwhzka')

connection = pika.BlockingConnection(paramas)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print("Received in main queue")
    data = json.loads(body.decode())
    print(f'The message is: {data}')
    with app.app_context():
        if properties.content_type == 'product_created':
            product = Product(
                id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print('Product created')

        elif properties.content_type == 'product_updated':
            product = Product.query.get(data['id'])
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
            print('Product updated')

        elif properties.content_type == 'product_deleted':
            product = Product.query.get(data['id'])
            db.session.delete(product)
            db.session.commit()
            print('Product deleted')


channel.basic_consume(
    queue='main', on_message_callback=callback, auto_ack=True)

print('Started consuming...')

channel.start_consuming()

channel.close()
