import pymysql

DB_CONFIG = {
    "host": "mysql.database.svc.cluster.local",
    "user": "receiveruser",
    "password": "receiverpassword",
    "database": "crud"
}

def get_messages_from_mysql():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, received_at FROM kafka_message")
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": row[0], "content": row[1], "received_at": row[2].strftime('%Y-%m-%d %H:%M:%S.%f')}
        for row in rows
    ]

def get_all_ids():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM kafka_message")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [str(row[0]) for row in rows]

def get_message_by_id(msg_id):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, received_at FROM kafka_message WHERE id = %s", (msg_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return {
            "id": row[0],
            "content": row[1],
            "received_at": row[2].strftime('%Y-%m-%d %H:%M:%S.%f')
        }
    return None
