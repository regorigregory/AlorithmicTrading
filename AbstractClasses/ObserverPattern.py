from abc import ABC, abstractmethod


class Subject(ABC):
    def __init__(self):
        self._observers: set = set()

    def attach(self, observer):
        if not observer in self._observers:
            self._observers.add(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, data):
        for observer in self._observers:
            observer.update(data)


class Observer(ABC):
    def observe(self, subject):
        subject.attach(self)

    @abstractmethod
    def update(self, data):
        pass
