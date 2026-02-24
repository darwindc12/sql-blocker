import pyodbc


# Database Connection

def get_connection(conn_str):
    """
    Create and return a SQL Server connection.
    Returns None if connection fails.
    """
    try:
        conn = pyodbc.connect(conn_str, timeout=5)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


# Find Head Blockers


def find_head_blockers(conn):
    """
    Returns list of head blockers in the format:
    (spid, host_name, blocked_count, wait_sec, dbname)
    """

    query = """
    WITH blocking_info AS (
        SELECT
            r.session_id AS spid,
            s.host_name,
            COUNT(b.session_id) AS blocked_count,
            MAX(r.wait_time) / 1000 AS wait_sec,
            DB_NAME(r.database_id) AS dbname
        FROM sys.dm_exec_requests r
        JOIN sys.dm_exec_sessions s ON r.session_id = s.session_id
        LEFT JOIN sys.dm_exec_requests b
            ON r.session_id = b.blocking_session_id
        WHERE r.blocking_session_id = 0
        GROUP BY r.session_id, s.host_name, r.database_id
    )
    SELECT spid, host_name, blocked_count, wait_sec, dbname
    FROM blocking_info
    WHERE blocked_count > 0
    ORDER BY wait_sec DESC;
    """

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error retrieving blockers: {e}")
        return []
    finally:
        cursor.close()


# Kill SPID

def kill_spid(conn, spid):
    """
    Kill a SQL Server session by SPID.
    """

    try:
        cursor = conn.cursor()
        cursor.execute(f"KILL {spid}")
        conn.commit()
    except Exception as e:
        raise Exception(f"Failed to kill SPID {spid}: {e}")
    finally:
        cursor.close()