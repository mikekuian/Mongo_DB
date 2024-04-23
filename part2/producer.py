import pika
import json
from faker import Faker
from models import Contact, FullName, EmailAddress, EmailBody
import connect  # Ensure this initializes MongoDB correctly

fake = Faker()

def generate_fake_data(n):
    for _ in range(n):
        fullname = FullName(name=fake.name())
        email_address = EmailAddress(address=fake.email())
        email_body = EmailBody(body=fake.paragraph())
        contact = Contact(
            fullname=fullname,
            email_address=email_address,
            email_body=email_body,
            is_sent=False
        )
        contact.save()
        send_to_rabbitmq(str(contact.id))

def send_to_rabbitmq(contact_id):
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='emails', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='emails',
        body=json.dumps(contact_id),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )
    print(f"Sent {contact_id} to RabbitMQ")
    connection.close()

if __name__ == '__main__':
    generate_fake_data(10)  # Generate and send 10 fake contacts
