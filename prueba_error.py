import psycopg2
import sys

def try_connection(DB_config:dict):
    for DB in DB_config.keys():
        try: 
            conn = psycopg2.connect(database = DB,
                                user = DB_config[DB]['user'],
                                host = DB_config[DB]['host'],
                                password = DB_config[DB]['password'],
                                port = DB_config[DB]['port'])
        except psycopg2.OperationalError as e:
            print('Unable to connect! ' + DB + '\n{}'.format(e))
            sys.exit(1)
        else: 
            print('Connected! ' + DB )
            conn.close()