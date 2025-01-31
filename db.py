import sqlite3

def create_connection(db_file):
    """ Создает соединение с базой данных SQLite """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """ Создает таблицу в базе данных, если она еще не существует """
    sql = ''' CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                blocked BOOLEAN DEFAULT FALSE
            ); '''
    try:
        cur = conn.cursor()
        cur.execute(sql)
    except sqlite3.Error as e:
        print(e)

def add_blocked_column(conn):
    """ Добавляет столбец blocked в таблицу requests, если он еще не существует """
    sql = ''' ALTER TABLE requests ADD COLUMN blocked BOOLEAN DEFAULT FALSE; '''
    try:
        cur = conn.cursor()
        # Проверяем, существует ли столбец blocked
        cur.execute("PRAGMA table_info(requests);")
        columns = cur.fetchall()
        column_names = [column[1] for column in columns]
        if 'blocked' not in column_names:
            cur.execute(sql)
    except sqlite3.Error as e:
        print(e)

def create_request(conn, request):
    """ Вставляет новую запись в таблицу requests с проверкой уникальности """
    organization_name, email, phone = request
    cur = conn.cursor()

    # Проверяем, существует ли уже запись с таким email или phone
    cur.execute('''
    SELECT id FROM requests WHERE email = ? OR phone = ?
    ''', (email, phone))
    existing_record = cur.fetchone()

    if existing_record:
        print(f"Запись с email {email} или phone {phone} уже существует.")
        return None

    sql = ''' INSERT INTO requests(organization_name, email, phone)
              VALUES(?,?,?) '''
    cur.execute(sql, request)
    conn.commit()
    return cur.lastrowid

def get_all_requests(conn):
    """ Возвращает все записи из таблицы requests """
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests")
    rows = cur.fetchall()
    return rows

def block_user(conn, user_id):
    """ Блокирует пользователя по ID """
    sql = ''' UPDATE requests
              SET blocked = TRUE
              WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    conn.commit()

def unblock_user(conn, user_id):
    """ Разблокирует пользователя по ID """
    sql = ''' UPDATE requests
              SET blocked = FALSE
              WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    conn.commit()

def is_user_blocked(conn, user_id):
    """ Проверяет, заблокирован ли пользователь по ID """
    sql = ''' SELECT blocked FROM requests WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    result = cur.fetchone()
    return result is not None and result[0] == 1

def check_unique_request(conn, request):
    """ Проверяет, существует ли уже такая заявка в базе данных """
    organization_name, email, phone = request
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests WHERE organization_name=? AND email=? AND phone=?", (organization_name, email, phone))
    return cursor.fetchone() is not None