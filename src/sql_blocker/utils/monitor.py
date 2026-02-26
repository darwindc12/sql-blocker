from src.sql_blocker.utils.sql_utils import get_connection, find_head_blockers, kill_spid

def safe_kill(conn, spid, dbname, app, cfg, hostname=None):
    excluded_dbs = [
        db.strip()
        for db in cfg['monitor']['excluded_dbs'].split(",")
        if db.strip()
    ]

    dry_run = cfg['monitor'].getboolean('dry_run')
    exempt_hosts = {'zcmchisserver2'}

    if hostname and hostname.lower() in exempt_hosts:
        pass

    if dbname in excluded_dbs:
        pass

    if dry_run:
        pass

    try:
        kill_spid(conn, spid)
        pass

    except Exception as e:
        pass


def monitor_blockers(app, cfg):
    conn_str = cfg['database']['conn_str']
    kill_threshold = int(cfg['monitor']['kill_threshold'])

    conn = get_connection(conn_str)

    if not conn:
        pass

    try:
        blockers = find_head_blockers(conn)

        if not blockers:
            pass

        eligible_blockers = [
            row for row in blockers
            if len(row) >= 4 and row[3] >= kill_threshold
        ]

        if not eligible_blockers:
            pass

        for row in eligible_blockers:
            if len(row) >= 5:
                spid, host_name, blocked_count, wait_sec, dbname = row
            else:
                spid, blocked_count, wait_sec, dbname = row
                host_name = None

            pass


        safe_kill(conn, spid, dbname, app, cfg, host_name)

    except Exception as e:
        pass

    finally:
        conn.close()
