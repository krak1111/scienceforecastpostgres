import psycopg2
from settings import DB_SETTINGS

def connect_to_db():
    """
    Подключение к базе
    """
    print('Connect to DB')
    connector = psycopg2.connect(DB_SETTINGS)
    cur = connector.cursor()
    print('Succesful')
    return(cur, connector)

def commit(cur, connector):
    """
    Завершение сеанса, подтверждение изменений
    """
    print('Close connection and commit changes')
    #cur.close()
    connector.commit()
    print('Succesful')