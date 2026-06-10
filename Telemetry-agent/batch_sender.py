import time

from sender import send_batch
from event_queue import event_queue

BATCH_SIZE = 50
BACKEND_URL = "http://127.0.0.1:8000/api/events/batch/"

def batch_sender_loop(api_key):

    while True:

        batch = []

        while (len(batch) < BATCH_SIZE and not event_queue.empty()):

            batch.append(event_queue.get())

        if batch:

            send_batch(BACKEND_URL,api_key,batch)

        time.sleep(2)