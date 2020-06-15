DATABASE_URL = "postgres://bwstpsmrizpbuh:57c5c712c14d736dc83b089e0e56dff5484b95f7449146e6c7cc85f8feab119e@ec2-18-215-99-63.compute-1.amazonaws.com:5432/d3gpgos7j08m2g"
conn = psycopg2.connect(DATABASE_URL, sslmode='require',
                        database='d3gpgos7j08m2g', user='bwstpsmrizpbuh')

create_tables(conn)
