import os

from gigmapr_processor.serializer import dump, load
from kombu import serialization

broker_url = os.getenv('BROKER_URL', 'redis://localhost:6379/0')
task_default_queue = 'gigmapr-processor'

result_backend = os.getenv('BACKEND_URL', 'elasticsearch://localhost:9200/gigmapr/_doc')
serialization.register('gigmapr_result', dump, load, 'application/python')
result_serializer = 'gigmapr_result'

task_annotations = {'*': {'rate_limit': '1/s'}}
