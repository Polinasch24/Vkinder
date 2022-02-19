import psycopg2 as pg


def create_db():

    with pg.connect('host=192.168.99.100 port=15432 dbname=vkinder user=postgres') as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vkinder_user (
                        id serial PRIMARY KEY,
                        first_name varchar(50) NOT NULL,
                        last_name varchar(50) NOT NULL,
                        age integer UNIQUE NOT NULL,
                        sity varchar(30) NOT NULL,
                        merital_status varchar(20) NOT NULL,
                        gender varchar(20) NOT NULL
                        """)


def add_user(user, cursor):
    cursor.execute("""
       INSERT into vkinder_user (id, first_name, last_name, age, sity, merital_status, gender) 
       values (%s, %s, %s, %s) 
       returning id  
       """, (user['id'], user['first_name'],
             user['last_name'], user['domain']))
    user_id = cursor.fetchone()[0]
    return candidate_id




if __name__ == '__main__':
    create_db()
    add_candidate()  # add

