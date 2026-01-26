import mysql.connector
from typing import List, Dict, Any

def connect_db():
    try:
        conn = mysql.connector.connect(
            
            host="host.docker.internal",
            user="root",
            password="dat0377324546",
            database="DB_Student_Management_System"
        )

        if conn.is_connected():
            return conn

    except mysql.connector.Error as err:
        print(f"Lỗi kết nối MySQL: {err}")
        return None


def get_cursor(conn, dictionary: bool = False):
    """
    Trả về cursor từ connection hiện tại
    dictionary=True  -> dùng cho SELECT
    dictionary=False -> dùng cho INSERT/UPDATE/DELETE
    """
    if conn is not None and conn.is_connected():
        return conn.cursor(dictionary=dictionary)
    return None

def execute_query(
    conn,
    query: str,
    params: tuple | None = None
) -> List[Dict[str, Any]]:
    if conn is None or not conn.is_connected():
        return []

    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(query, params)
        return cur.fetchall()
    except mysql.connector.Error as err:
        print(f"Lỗi SQL: {err}")
        return []
    finally:
        cur.close()



def close_connection(conn):
    if conn is not None and conn.is_connected():
        conn.close()
        print("Đã đóng kết nối MySQL")


def execute_update(
    conn,
    query: str,
    params: tuple | None = None
) -> bool:

    if conn is None or not conn.is_connected():
        return False

    cur = conn.cursor()
    try:
        cur.execute(query, params)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Lỗi SQL: {err}")
        return False
    finally:
        cur.close()

def commit_transaction(conn, success: bool):
    """
    success=True  -> commit
    success=False -> rollback
    """
    if conn is None or not conn.is_connected():
        return

    if success:
        conn.commit()
    else:
        conn.rollback()

conn = connect_db()


