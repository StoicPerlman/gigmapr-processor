import logging
import re

import requests
from bs4 import BeautifulSoup
from celery import Celery
from gigmapr_processor.backend import GigmaprBackend

app = Celery('gigmapr-processor')
app.config_from_object('gigmapr_processor.celeryconfig')

BASE_URL = 'https://job-openings.monster.com/'

log = logging.getLogger(__name__)


@app.task(
    name='gigmapr_processor.tasks.process_job',
    backend=GigmaprBackend(app=app, url=app.conf.result_backend))
def process_job(job_id, post_date, location):
    url = BASE_URL + job_id
    resp = requests.get(url)

    if resp.status_code == 200:
        bs = BeautifulSoup(resp.text, features='html.parser')
    else:
        log.error(f'Error processing job: {job_id}\n' \
                    + f'Response code: {resp.status_code}\n' \
                    + f'Body: {resp.text}')
        return

    full_text = bs.find(id='JobViewHeader').find('h1').get_text()
    full_text += bs.find(id="JobDescription").get_text()

    city, state = location.split(',')

    return {
        'job_id': job_id,
        'full_text': full_text,
        'city': city,
        'state': state,
        'post_date': post_date,
    }
