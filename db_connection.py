import config
import psycopg2
import psycopg2.extras
import uuid,datetime
import logging

class User():
    id = uuid
    chat_id = int
    join_date = datetime
    username = str
    first_name = str
    last_name = str
    userAssets = list
    contact = str

def connect_to_db():
    try:
        conn = psycopg2.connect(dbname=config.dbname, user=config.user,
                                password=config.password, host=config.host)
        return conn
    except Exception as e:
        print(repr(e))

def update_db(conn, sql = None):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(repr(e))


def query(sql):
    conn = connect_to_db()
    try:
        records = update_db(conn,sql)
        return records
    except psycopg2.Error as e:
        logging.exception(e.pgerror)
        return None

def createUser(dct):
    user = User
    user.id = uuid.uuid4()
    user.chat_id = dct.from_user.id
    user.username = dct.from_user.username
    user.first_name = dct.from_user.first_name
    user.last_name = dct.from_user.last_name
    user.join_date = datetime.datetime.now()

    result = query("INSERT INTO public.users (user_id, chat_id, username, first_name, last_name, join_date)"
                      "VALUES ('{0}','{1}','{2}','{3}','{4}', '{5}')".format(user.id, user.chat_id, user.username, user.first_name,
                                                                  user.last_name, user.join_date))
    return result