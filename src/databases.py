import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, registry, sessionmaker

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{os.environ['PG_USER']}:"
    f"{os.environ['PG_PASSWORD']}@"
    f"{os.environ['PG_HOST']}/"
    f"{os.environ['PG_DB']}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, echo_pool=False, pool_pre_ping=True)

mapper_registry = registry()
Base = mapper_registry.generate_base()


class SessionFactory:
    @staticmethod
    def create() -> Session:
        session: Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)()
        return session
