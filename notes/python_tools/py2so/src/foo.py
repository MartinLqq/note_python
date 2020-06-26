import datetime

from .bar import hello_bar


class DataCenter:

    def get_time(self):
        print(datetime.datetime.now())

    def write_data(self):
        print("hello!")

    def bar(self):
        hello_bar()
