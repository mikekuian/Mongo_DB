import pika
import json
from models import Contact
import connect  # This imports and initializes the MongoDB connection

def callback(ch, method, properties, body):
    contact_id = json.loads(body)
    contact = Contact.objects(id=contact_id).first()
    if contact:
        contact.update(is_sent=True)
        print(f"Processed contact {contact.fullname} with email {contact.email_address}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='emails', durable=True)

channel.basic_consume(queue='emails', on_message_callback=callback, auto_ack=False)
print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
