import abc

from jabberwocky.shared.domain.event_producer import EventProducer


class DispatcherEventProducer(EventProducer, abc.ABC):
    @abc.abstractmethod
    def dispatch(self) -> None: ...
