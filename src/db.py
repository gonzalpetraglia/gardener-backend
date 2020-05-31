from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_session_builder(
    user,
    password,
    host,
    port,
    db_name
):
    url = 'postgresql://{}:{}@{}:{}/{}'.format(
        user,
        password,
        host,
        port,
        db_name)

    @contextmanager
    def create_session():
        # an Engine, which the Session will use for connection
        # resources
        engine = create_engine(
            url
        )

        # create a configured "Session" class
        Session = sessionmaker(bind=engine)

        # create a Session
        session = Session()
        try:
            yield session

            session.commit()
        except Exception as e:

            session.rollback()
            raise e
        finally:
            session.close()
    return create_session
