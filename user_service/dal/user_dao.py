from common.database.repository import session_local


def get_user_dao():
    session = session_local()
    try:
        yield session
        session.commit()
    except Exception as err:
        session.rollback()
        raise err
    finally:
        session.close()
