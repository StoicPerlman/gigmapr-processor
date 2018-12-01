import os

broker_url = os.getenv('BROKER_URL', 'redis://localhost:6379/0')
task_default_queue = 'gigmapr-processor'

result_backend = os.getenv('BACKEND_URL', 'elasticsearch://localhost:9200/gigmapr/_doc')

task_annotations = {'*': {'rate_limit': '1/s'}}
