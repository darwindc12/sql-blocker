from src.sql_blocker.utils.sql_utils import get_connection, find_head_blockers

# Put your real connection string here temporarily
conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=zcmchisserver2;DATABASE=smartapp8;UID=sa;PWD=MTBnimoso_2025"

conn = get_connection(conn_str)

if conn:
    print("Connection successful!")

    blockers = find_head_blockers(conn)

    if blockers:
        print("⚠Blockers detected:")
        for row in blockers:
            print(row)
    else:
        print("No blockers found.")

    conn.close()
else:
    print("Connection failed.")