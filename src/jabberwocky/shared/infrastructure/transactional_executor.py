from collections.abc import Callable
from typing import TypeVar, cast

from sqlalchemy.orm import Session

from jabberwocky.shared.domain.event_producer import EventProducer
from jabberwocky.shared.infrastructure.dispatcher_event_producer import DispatcherEventProducer
from jabberwocky.shared.infrastructure.executor_session import ExecutorSession

T = TypeVar("T")


class TransactionalExecutor:
    def __init__(
        self,
        session: Session,
        dispatcher_event_producer: DispatcherEventProducer | None = None,
    ) -> None:
        self._session = session
        self._event_dispatcher = dispatcher_event_producer

    @property
    def session(self) -> ExecutorSession:
        return cast(ExecutorSession, self._session)

    @property
    def event_producer(self) -> EventProducer:
        if not self._event_dispatcher:
            raise ValueError("Event producer is not available")

        return self._event_dispatcher

    def run(self, _callable: Callable[[], T]) -> T:
        with self._session.begin():
            result = _callable()

        if self._event_dispatcher:
            self._event_dispatcher.dispatch()

        return result
