import psycopg2
from .settings import DB_SETTINGS

def connect_to_db():
    """
    Подключение к базе
    """
    connector = psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    return(cur, connector)

def commit(cur, connector):
    """
    Завершение сеанса, подтверждение изменений
    """
    #cur.close()
    connector.commit()