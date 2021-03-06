import os,threading
import sys
import time,datetime
from pykafka import KafkaClient
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([BASE_DIR,])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nxp.settings")

import django

django.setup()
from webui.tasks import Http_info

def get_timestamp(timestring):
    tmp_timestamp=timestring.split('.')[0]
    timestamp = time.mktime(time.strptime(tmp_timestamp, '%Y-%m-%dT%H:%M:%S'))+28800
    return timestamp
def Insert_model(data):
    try:
        t_date_time=get_timestamp(data.get('@timestamp'))
        t_clientip=data.get('clientip')
        t_host=data.get('host')
        t_domain=data.get('http_host')
        t_status=int(data.get('status'))
        Http_info().apply_async(args=(t_domain,t_host,t_clientip,t_date_time,t_status))
        print "done"
    except Exception as e:
        print str(e)

def Kafka_consumer():
    client = KafkaClient(hosts="10.0.8.71:9092,10.0.8.72:9092,10.0.8.73:9092")
    topic = client.topics['django-nginx']
    balanced_consumer = topic.get_balanced_consumer(
    consumer_group='django-nginx',
    auto_commit_enable=True,
    zookeeper_connect='10.0.8.39:2181,10.0.8.40:2181,10.0.8.87:2181'
    )
    for message in balanced_consumer:
        if message is not None:
            Insert_model(json.loads(message.value))


if __name__ == "__main__":
    Kafka_consumer()