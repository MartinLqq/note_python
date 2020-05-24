class Publisher:

    def __init__(self):
        self._observers = dict()

    def register(self, observer):
        self._observers[observer.__class__.__name__] = observer

    def unrigister(self, observer):
        self._observers.pop(observer.name)

    def notify(self, msg):
        for _name, obs in self._observers.items():
            obs.do_somthing(msg)


class Martin:
    """Observer: Martin."""
    def do_somthing(self, msg):
        print('Martin received: ', msg)


class John:
    """Observer: John."""
    def do_somthing(self, msg):
        print('John received: ', msg)


if __name__ == '__main__':
    pub = Publisher()
    pub.register(Martin())
    pub.register(John())

    # 通知所有观察者
    pub.notify('time to eat')
    print()
    pub.notify('time to sleep')
