import psycopg2


def create_tables(conn):
    command = (
        """
        DROP TABLE inventory;

        CREATE TABLE IF NOT EXISTS inventory (
            char_id SERIAL PRIMARY KEY,
            char_name VARCHAR(255) NOT NULL
        );
        """)
    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    conn.commit()
    print("Table created...")


def edit_tables(conn):
    command = (
        """
        ALTER TABLE inventory
        ADD COLUMN "backpack" int,
        ADD COLUMN "shoes" int,
        ADD COLUMN "belt_beltpouch" int,
        ADD COLUMN "bedroll" int,
        ADD COLUMN "clothes" int,
        ADD COLUMN "cloak" int,
        ADD COLUMN "std_rations" int,
        ADD COLUMN "small_sack" int,
        ADD COLUMN "waterskin" int;
        """
    )

    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    conn.commit()
    print("Inventory created...")


def list_tables(conn):
    command = (
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
    )


def add_inventory(conn):
    command = (
        """
        INSERT INTO inventory (char_name, backpack, shoes, belt_beltpouch,
        bedroll, clothes, cloak, std_rations, small_sack, waterskin)
        VALUES
            ('Valtyra', 1, 1, 1, 1, 2, 1, 7, 1, 1);
        """
    )
    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    conn.commit()
    print("Starting inventory generated...")
