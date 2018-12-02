import json
import logging

from celery.backends.elasticsearch import ElasticsearchBackend
from kombu.utils.encoding import bytes_to_str

log = logging.getLogger(__file__)


class GigmaprBackend(ElasticsearchBackend):
    def __init__(self, *args, **kwargs):
        super(GigmaprBackend, self).__init__(*args, **kwargs)

    def _index(self, id, body, **kwargs):
        celery_result = body['result']
        job_result = celery_result['result']
        new_id = job_result.get('job_id', None)

        if not new_id:
            b = json.dumps(body)
            log.error(f'job_id missing: {b}')
            return

        new_body = {
            'status': celery_result['status'],
            'full_text': job_result.get('full_text', None),
            'city': job_result.get('city', None),
            'state': job_result.get('state', None),
            'post_date': job_result.get('post_date', None),
            'traceback': celery_result['traceback']
        }

        return self.server.index(
            id=new_id,
            index=self.index,
            doc_type=self.doc_type,
            body=json.dumps(new_body),
            **kwargs,
        )
