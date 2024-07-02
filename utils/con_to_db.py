
from pymysql import connect

USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
PORT = 3306
DATABASE = 'house'


def query_data(sql_str):

    try:
        
        conn = connect(user=USERNAME, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)

        
        cur = conn.cursor()

        
        row_count = cur.execute(sql_str)

        
        conn.commit()

        
        result = cur.fetchall()

    except Exception as e:
        print(e)

    finally:
        
        cur.close()

        
        conn.close()

        return result










