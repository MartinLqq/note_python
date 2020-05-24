# watchdog

 一组API和shell实用程序，用于监视文件系统事件。 

简单使用:

```python
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```



自定义事件处理方法

```python
import sys
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileMonitor(FileSystemEventHandler):
    def on_moved(self, event):
        super(FileMonitor, self).on_moved(event)
        now_time = time.strftime(
            "[\033[32m INFO \033[0m]\033[34m %H:%M:%S \033[0m", time.localtime()
        )
        what = 'directory' if event.is_directory else 'file'
        print("{0} {1} Moved : from {2} to {3}".format(
            now_time, what, event.src_path, event.dest_path
        ))

    def on_deleted(self, event):
        super(FileMonitor, self).on_deleted(event)
        now_time = time.strftime(
            "[\033[32m INFO \033[0m]\033[34m %H:%M:%S \033[0m", time.localtime()
        )
        what = 'directory' if event.is_directory else 'file'
        print("{0} {1} Deleted : {2} ".format(now_time, what, event.src_path))

    def on_modified(self, event):
        super(FileMonitor, self).on_modified(event)
        now_time = time.strftime(
            "[\033[32m INFO \033[0m]\033[34m %H:%M:%S \033[0m", time.localtime()
        )
        what = 'directory' if event.is_directory else 'file'
        print("{0} {1} Modified : {2} ".format(now_time, what, event.src_path))
        
    def on_created(self, event):
        super(FileMonitor, self).on_moved(event)
        now_time = time.strftime(
            "[\033[32m INFO \033[0m]\033[34m %H:%M:%S \033[0m", time.localtime()
        )
        what = 'directory' if event.is_directory else 'file'
        print("{0} {1} Created : {2} ".format(now_time, what, event.src_path))


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = FileMonitor()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```



