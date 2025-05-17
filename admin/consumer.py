import pika

paramas = pika.URLParameters(
    'amqps://fodwhzka:iOXY-F11dMTsqctaUO_tjxADn0wjUWUU@kebnekaise.lmq.cloudamqp.com/fodwhzka')

connection = pika.BlockingConnection(paramas)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print("Received in admin queue")
    print(f'The message is: {body.decode()}')


channel.basic_consume(
    queue='admin', on_message_callback=callback, auto_ack=True)

print('Started consuming...')

channel.start_consuming()

channel.close()
