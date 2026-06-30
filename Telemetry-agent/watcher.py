from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time

from parser import parse_log
from event_queue import event_queue


class LogHandler(FileSystemEventHandler):

    def __init__(self, service_name, file_path, node_id="local-node"):

        self.service_name = service_name

        self.file_path = file_path

        self.node_id = node_id

        self.last_position = 0

    def process_new_lines(self):

        try:

            with open(self.file_path,"r",encoding="utf-8",errors="ignore") as file:

                file.seek(self.last_position)

                lines = file.readlines()

                self.last_position = file.tell()

                for line in lines:

                    line = line.strip()

                    if not line:

                        continue

                    event = parse_log(self.service_name,line, self.node_id)
                    print("QUEUEING EVENT:")
                    print(event)
                    event_queue.put(event)

        except Exception as error:

            print(
                f"[WATCHER ERROR] "
                f"{self.service_name}: "
                f"{error}"
            )

    def on_modified(self, event):

        if event.src_path == self.file_path:

            self.process_new_lines()

# backend_url,api_key
def start_watcher(service_name,file_path, node_id="local-node"):

    handler = LogHandler(service_name,file_path, node_id)

    observer = Observer()

    handler.process_new_lines()

    observer.schedule(

        handler,

        path=file_path.rsplit("/",1)[0] if "/" in file_path else ".",

        recursive=False
    )

    observer.start()

    print(
        f"[WATCHING] "
        f"{service_name} -> "
        f"{file_path}"
    )

    try:

        while True:

            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()

    observer.join()