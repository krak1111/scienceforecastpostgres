import os
import pickle
import itertools
from multiprocessing import Pool

from dbwriter import connect

QUARTERS = itertools.cycle(('Q1', 'Q2', 'Q3', 'Q4'))

def get_quarter(date):
    """
    Возвращает в каком квартале выпущена статья
    """
    if int(date[:2]) < 4:
        return 'Q1'
    if int(date[:2]) < 7:
        return 'Q2'
    if int(date[:2]) < 10:
        return 'Q3'
    return 'Q4'


def is_year_journal(articles):
    for article in articles[:200]:
        if article['publication date'][:2] != '01':
            return False
    return True


def domains_writer(cur, writen_dict):
    """
    Запись всех доменнов журналаб возвращает id записанных или уже существующих поддоменов, указанных в журнале
    """
    # Запись супердомена
    cur.execute("SELECT id FROM primary_domains WHERE name = %s", (writen_dict['primary'],))  # запрос id супердомена
    ident = cur.fetchone()
    if ident is None:  # Если нет супердомена
        cur.execute("INSERT INTO primary_domains (name) VALUES %s RETURNING id", (writen_dict['primary']))  # запись в БД
        ident = cur.fetchone()
    primary_id = ident[0]

    # запись домена
    cur.execute("SELECT id FROM domains WHERE name = %s", (writen_dict['domain'], ))  # запрос id домена
    ident = cur.fetchone()
    if ident is None:  # если нет домена
        cur.execute("INSERT INTO domains (name, primary_id) VALUES (%s, %s) RETURNING id", (writen_dict['domain'], primary_id))  # запись в бд название домена и id супердомена родителя
        ident = cur.fetchone()
    domain_id = ident[0]
    
    # Проход по поддоменам. Их может быть несколько в одном журнале
    subdomains_id = []
    if type(writen_dict['subdomain']) == str:
        cur.execute("SELECT id FROM subdomains WHERE name = %s", (writen_dict['subdomain'],))
        ident = cur.fetchone()
        if ident is None:  # если нет домена
            cur.execute("INSERT INTO subdomains (name, domain_id) VALUES (%s, %s) RETURNING id", (writen_dict['subdomain'], domain_id))  # запись в бд название поддомена и id домена родителя
            ident = cur.fetchone()
        subdomains_id.append(ident[0])
        return subdomains_id

    for subdomain in writen_dict['subdomain']:
        cur.execute("SELECT id FROM subdomains WHERE name = %s" % (subdomain))
        ident = cur.fetchone()
        if ident is None:  # если нет домена
            cur.execute("INSERT INTO subdomains (name, domain_id) VALUES (%s, %s) RETURNING id", (subdomain, domain_id))  # запись в бд название поддомена и id домена родителя
            ident = cur.fetchone()
        subdomains_id.append(ident[0])

    return subdomains_id

def journal_writer(cur, journal_name):
    """
    Функция записи журнала, возвращает id записанного или уже существующего журнала
    """
    cur.execute("SELECT id FROM journals WHERE name = %s", (journal_name))
    if cur.fetchone() is None:  # если нет журнала
        cur.execute("INSERT INTO journals (name) VALUES (%s) RETURNING id", (journal_name))  # запись в бд название журнала
        return cur.fetchone()[0]
    return None

def article_writer(cur, article, journal_id):
    """
    Функция записи статьи возвращает id статьи
    """
    
    # запись статьи
    cur.execute("SELECT id FROM years WHERE year = %s", (article['year']))  # получение id года публикации
    year_id = cur.fetchone()[0]
    cur.execute("SELECT id FROM quarters WHERE name = %s;", (article['quarter']))  # получение id квартала публикации
    quarter_id = cur.fetchone()[0]
    cur.execute("""INSERT INTO articles (name, doi, abstract, keywords, pub_year_id, pub_quarter_id, journal_id) VALUES
                     (%s, %s, %s, %s, %s, %s, %s) RETURNING id""", (article['article name'], article['doi'], article['abstract'], article['keywords'], year_id, quarter_id, journal_id))

    return cur.fetchone()[0]

def collocations_writer(cur, bigrams, trigrams):
    """
    Функция записи словосочетаний возвращает список id словосочетаний
    """
    cur.execute("SELECT id FROM collocation_types WHERE type = 'bigram'")
    col_type_id = cur.fetchone()[0]
    collocations_id = []
    bigrams = set(bigrams)
    for bigram in bigrams:
        cur.execute("SELECT id FROM collocations WHERE collocation = %s" , (bigram))
        ident = cur.fetchone()
        if cur.fetchone() is None:
            cur.execute("INSERT INTO collocations (collocation, col_type_id) VALUES (%s, %s) RETURNING id;" , (bigram, col_type_id))
            ident = cur.fetchone()

        collocations_id.append(ident[0])

    cur.execute("SELECT id FROM collocation_types WHERE type = 'trigram';")
    col_type_id = cur.fetchone()[0]
    trigrams = set(trigrams)
    for trigram in trigrams:
        cur.execute("SELECT id FROM collocations WHERE collocation = %s", (trigram))
        ident = cur.fetchone()
        if ident is None:
            cur.execute("INSERT INTO collocations (collocation, col_type_id) VALUES (%s, %s) RETURNING id", (trigram, col_type_id))
            ident = cur.fetchone()
        collocations_id.append(ident[0])

    return collocations_id

def articles_collocations_writer(cur, article_id, collocations_id):
    """
    Функция записи взаимосвязей между статьей и словосочетаниями
    """
    for collocation_id in collocations_id:
        cur.execute("""INSERT INTO articles_collocations (article_id, collocation_id) VALUES
                         (%s, %s);""", (article_id, collocation_id))



def read_pickle(file_path):
    """
    Десериализация файла
    """
    with open(file_path, 'rb') as file:
        writen_dict = pickle.load(file)
    return writen_dict

def write_to_db(file_path):
    """
    Запись в БД
    """
    # запись журнала
    writen_dict = read_pickle(file_path)
    (cur, connector) = connect.connect_to_db()
    journal_id = journal_writer(cur, writen_dict['journal name'])
    if journal_id is None:
        print(f"Journal: {writen_dict['journal name']} is already exist")
        return True
    subdomains_id = domains_writer(cur, writen_dict)
    # матрица отношения сабдоменов и журналов
    for subdomain_id in subdomains_id:
        cur.execute("INSERT INTO subdomains_journals (subdomain_id, journal_id) VALUES (%s, %s)", (subdomain_id, journal_id))  # создание связи
    
    is_year_pub = is_year_journal(writen_dict['articles'])
    
    for article in writen_dict['articles']:

        # подготовка даты к записи
        if is_year_pub:
            article['quarter'] = next(QUARTERS) 
        else:
            article['quarter'] = get_quarter(article['publication date'])
        article['year'] = int(article['publication date'][3:])

        article_id = article_writer(cur, article, journal_id)

        collocations_id = collocations_writer(cur, article['bigrams'], article['trigrams'])

        articles_collocations_writer(cur, article_id, collocations_id)
    print(f"Journal: {writen_dict['journal name']} writen")
    connect.commit(cur, connector)


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    walking_path = os.path.join(os.getcwd(), 'pkl')
    file_list = []
    for root, _, files in os.walk(walking_path):
        if not files:
            continue
        
        for file in files:
            file_path = os.path.join(os.getcwd(), root, file)
            file_list.append(file_path)
    write_pool = Pool(15)
    write_pool.map(write_to_db, file_list)


if __name__ == '__main__':
    main()
