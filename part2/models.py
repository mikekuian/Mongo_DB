from mongoengine import Document, StringField, BooleanField, EmbeddedDocument, EmbeddedDocumentField

class FullName(EmbeddedDocument):
    name = StringField(required=True)

class EmailAddress(EmbeddedDocument):
    address = StringField(required=True)

class EmailBody(EmbeddedDocument):
    body = StringField(required=True)

class Contact(Document):
    fullname = EmbeddedDocumentField(FullName)
    email_address = EmbeddedDocumentField(EmailAddress)
    email_body = EmbeddedDocumentField(EmailBody)
    is_sent = BooleanField(default=False)
