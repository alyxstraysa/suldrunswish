import psycopg2


def create_tables(conn):
    command = (
        """
        CREATE TABLE IF NOT EXISTS inventory (
            char_id SERIAL PRIMARY KEY,
            char_name VARCHAR(255) NOT NULL
        )
        """)
    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    conn.commit()
    print("Table created...")
