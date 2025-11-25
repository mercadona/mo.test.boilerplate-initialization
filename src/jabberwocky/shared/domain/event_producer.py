import abc

from jabberwocky.shared.domain.event import Event


class EventProducer(abc.ABC):
    @abc.abstractmethod
    def publish(self, events: list[Event]) -> None: ...
