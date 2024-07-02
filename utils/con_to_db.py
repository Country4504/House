# 1. 从pymysql中导入connect函数
from pymysql import connect

USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
PORT = 3306
DATABASE = 'house'


def query_data(sql_str):

    try:
        # 连接数据库
        conn = connect(user=USERNAME, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)

        # 获取游标对象cursor
        cur = conn.cursor()

        # 使用游标对象来执行SQL语句
        row_count = cur.execute(sql_str)

        # 提交修改数据的SQL语句到数据库
        conn.commit()

        # 使用游标对象获取查询结果
        result = cur.fetchall()

    except Exception as e:
        print(e)

    finally:
        # 关闭游标
        cur.close()

        # 断开与数据库的连接
        conn.close()

        return result

#
# if __name__ == '__main__':
#     beijing_region = ['东城','西城','海淀','昌平','朝阳','顺义','通州','石景山']
#
#     import random
#     for i in range(1, 305):
#         addr = random.choice(beijing_region)
#         sql = 'update userinfo set addr="{}" where id = {}'.format(addr, str(i))
#         query_data(sql)
