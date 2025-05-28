import mysql.connector
from mysql.connector import pooling

# 커넥션 풀 설정
dbconfig = {
    "host": "ondojung.mycafe24.com",
    "user": "ondojung",
    "password": "hyseo0207*",
    "database": "ondojung"
}

pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,  # 동시에 사용할 수 있는 최대 연결 수
    pool_reset_session=True,
    **dbconfig
)

def get_connection():
    return pool.get_connection()
