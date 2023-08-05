from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.observer import Observer

class Observable(ABC):

    @abstractmethod
    def register(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def publish(self) -> None:
        pass

class SimpleObservable(Observable):

    _observers: List[Observer] = []

    def register(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def publish(self, ev: Any) -> None:
        for observer in self._observers:
            observer(ev)

class StateObservable(Observable):

    _state: int = None

    _observers: List[Observer] = []

    def register(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def publish(self) -> None:
        for observer in self._observers:
            observer(self._state)

class EventDispatcher(Observable):

    _observers: Dict[List[Observer]] = {}

    def register(self, observer: Observer, name: str) -> None:
        self._observers[name].append(observer)

    def detach(self, observer: Observer, name: str = None) -> None:
        self._observers[name].remove(observer)

    def publish(self, ev: Any) -> None:
        for observer in self._observers[ev.__name__]:
            observer(ev)
