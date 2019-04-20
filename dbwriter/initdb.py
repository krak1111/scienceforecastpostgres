from dbwriter import connect
from dbwriter.init_commands import creating_commands, references

def main():

    (cur, connector) = connect.connect_to_db()
 
    print('Creating Tables')
    for command in creating_commands:
        cur.execute(command)
    print('Succesful!\nMade references')
    
    for command in references:
        cur.execute(command)
    print('Succesful!\nFill years')
    
    for year in range(2010, 2020):
        cur.execute(f"INSERT INTO years (year) VALUES({year})")
    print('Succesful!\nFill quarters')
    
    for quarter in range(1, 5):
        cur.execute(f"INSERT INTO quarters (name) VALUES('Q{quarter}')")
    print('Succesful!\nFill col_types')
    
    for col_type in ['bigram', 'trigram']:
        cur.execute(f"INSERT INTO collocation_types (type) VALUES('{col_type}')")
    print('Succesful!')
    connect.commit(cur, connector)

if __name__ == '__main__':
    main()
