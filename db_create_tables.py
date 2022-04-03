from db_connection import query

def create_user_table():
    action = query("CREATE TABLE public.users"
                   "(user_id uuid PRIMARY KEY NOT NULL,"
                   "chat_id integer,"
                   "username text,"
                   "first_name text,"
                   "last_name text,"
                   "join_date timestamp with time zone)");
    return action

create_user_table()