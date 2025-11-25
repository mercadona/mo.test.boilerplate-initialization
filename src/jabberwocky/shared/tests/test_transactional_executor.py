from unittest.mock import create_autospec

import pytest
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from databases import Base, SessionFactory
from jabberwocky.shared.infrastructure.dispatcher_event_producer import DispatcherEventProducer
from jabberwocky.shared.infrastructure.executor_session import ExecutorSession
from jabberwocky.shared.infrastructure.transactional_executor import TransactionalExecutor


class DummyModel(Base):
    __tablename__ = "dummy"

    name: Mapped[str] = mapped_column(String(6), primary_key=True)


class DummyAction:
    def __init__(self, session: ExecutorSession) -> None:
        self._session = session

    def execute(self) -> None:
        center_entity = DummyModel(name="dummy")
        self._session.add(center_entity)


class DummyErrorAction:
    def __init__(self, session: ExecutorSession) -> None:
        self._session = session

    def execute(self) -> None:
        center_entity = DummyModel(name="dummy")
        self._session.add(center_entity)
        raise NotImplementedError("Dummy error")


class DummyEventProducerAction:
    def execute(self) -> None: ...


@pytest.mark.integration
class TestTransactionalExecutor:
    def test_should_commit_data(self) -> None:
        test_session = SessionFactory.create()
        transactional_executor = TransactionalExecutor(SessionFactory.create())

        transactional_executor.run(lambda: DummyAction(transactional_executor.session).execute())

        with test_session.begin():
            my_model = test_session.query(DummyModel).filter_by(name="dummy").first()

            assert my_model is not None
            assert my_model.name == "dummy"

    def test_should_rollback_data(self) -> None:
        test_session = SessionFactory.create()
        transactional_executor = TransactionalExecutor(SessionFactory.create())

        with pytest.raises(NotImplementedError):
            transactional_executor.run(lambda: DummyErrorAction(transactional_executor.session).execute())

        with test_session.begin():
            my_model = test_session.query(DummyModel).filter_by(name="dummy").first()
            assert my_model is None

    def test_should_dispatch_events(self) -> None:
        mock_dispatcher_event_producer = create_autospec(DispatcherEventProducer, spec_set=True, instance=True)
        action = DummyEventProducerAction()
        transactional_executor = TransactionalExecutor(
            session=SessionFactory.create(), dispatcher_event_producer=mock_dispatcher_event_producer
        )

        transactional_executor.run(lambda: action.execute())

        mock_dispatcher_event_producer.dispatch.assert_called_once()

    def test_should_not_dispatch_events_when_no_given_event_dispatcher(self) -> None:
        action = DummyEventProducerAction()
        transactional_executor = TransactionalExecutor(session=SessionFactory.create())

        transactional_executor.run(lambda: action.execute())

    def test_should_raise_error_when_event_producer_is_not_available(self) -> None:
        transactional_executor = TransactionalExecutor(session=SessionFactory.create())

        with pytest.raises(ValueError):
            _ = transactional_executor.event_producer
