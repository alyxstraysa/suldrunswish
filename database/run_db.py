import psycopg2

#DATABASE_URL = "postgres://bwstpsmrizpbuh:57c5c712c14d736dc83b089e0e56dff5484b95f7449146e6c7cc85f8feab119e@ec2-18-215-99-63.compute-1.amazonaws.com:5432/d3gpgos7j08m2g"

# conn = psycopg2.connect(DATABASE_URL, sslmode='require',
#                        database='d3gpgos7j08m2g', user='bwstpsmrizpbuh')

DATABASE_URL = "postgres://gikmffespagoaj:2b04fba400a6092cc243f1610ebf31ddc240e1dff43505cc79dca2ee2db38012@ec2-54-88-130-244.compute-1.amazonaws.com:5432/d2gqdjjcfip1cp"

conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                        database='d2gqdjjcfip1cp', user='gikmffespagoaj', password='2b04fba400a6092cc243f1610ebf31ddc240e1dff43505cc79dca2ee2db38012')


def create_tables(conn):
    command = (
        """
        DROP TABLE IF EXISTS inventory;

        CREATE TABLE IF NOT EXISTS char_list (
            char_id SERIAL PRIMARY KEY,
            char_name VARCHAR(255) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS char_list (
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


def add_character(conn):
    command = (
        """
        INSERT INTO characters (characterName, strength, dexterity, constitution, intelligence, charisma, wisdom, class, characterLevel, hitDie, experience, attackValue, savingThrow, slots, miracles, groups, raises, gold, encumbrance, movement, armorClass, initiativeBonus, languages)
        VALUES
        (
            'Suldrun',
            10,
            10,
            10,
            16,
            10,
            10,
            'Wise',
            1,
            1,
            0,
            10,
            7,
            1,
            '',
            '',
            0,
            '',
            0,
            30,
            0,
            0,
            'Common'
        );
        """
    )
    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    conn.commit()
    print("Character created...")


if __name__ == "__main__":
    add_character(conn)
