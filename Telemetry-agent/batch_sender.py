import time

from sender import send_batch
from event_queue import event_queue

BATCH_SIZE = 50

def batch_sender_loop(backend_url,api_key):

    while True:

        batch = []

        while (len(batch) < BATCH_SIZE and not event_queue.empty()):

            batch.append(event_queue.get())

        if batch:

            send_batch(backend_url,api_key,batch)

        time.sleep(2)