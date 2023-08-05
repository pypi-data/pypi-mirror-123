

from abc import ABC, abstractmethod
from typing import Any, Callable, Union

class Listener(ABC):

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.update(*args, **kwds)
        return super().__call__(*args, **kwds)

    @abstractmethod
    def update(self, ev: Any) -> None:
        pass

Observer = Union[Listener, Callable]
