from . import connect
import os
import pickle
from multiprocessing import Pool


def add_column():
    (cur, connector) = connect.connect_to_db()
    cur.execute("""ALTER TABLE articles
                     ADD COLUMN IF NOT EXISTS abstract VARCHAR,
                     ADD COLUMN IF NOT EXISTS keywords VARCHAR ARRAY""")
    connect.commit(cur, connector)

def update(article):
    (cur, connector) = connect.connect_to_db()
    cur.execute("""UPDATE articles 
                     SET abstract = %s, keywords = %s
                       WHERE doi = %s""", (article['abstract'], article['keywords'], article['doi']))
    connect.commit(cur, connector)
    print(article['doi'])

def main(walking_path):
    for root, _, files in os.walk(walking_path):
        for file in files:
            file_path = os.path.join(os.getcwd(), root, file)
            with open(file_path, 'rb') as f:
                writen_dict = pickle.load(f)
            update_pool = Pool(10)
            update_pool.map(update, writen_dict['articles'])
            print('File: ', file, ' complete!')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    walking_path = os.path.join(os.getcwd(), 'pkl')
    # add_column()
    main(walking_path)
    