import datetime
import os
from mongoengine import connect, Document, DateTimeField, StringField

connect(host=os.environ.get('MONGO_CONNECTION_STRING', 'mongodb://127.0.0.1:27017/'), db="lgt_admin")

class DelayedJob(Document):
    created_at = DateTimeField(required=True)
    scheduled_at = DateTimeField(required=True)
    job_type = StringField(required=True)
    data = StringField(required=True)
    jib = StringField(required=True)
    executed_at: DateTimeField(required=False)

    meta = { 'indexes': ['-scheduled_at', "jib"] }
