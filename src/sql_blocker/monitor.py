from src.sql_blocker.utils.sql_utils import get_connection, find_head_blockers, kill_spid
from src.sql_blocker.logger import log_message

def safe_kill(conn, spid, dbname, app, cfg, hostname=None):
    excluded_dbs = [
        db.strip()
        for db in cfg['monitor']['excluded_dbs'].split(",")
        if db.strip()
    ]

    dry_run = cfg['monitor'].getboolean('dry_run')
    exempt_hosts = {'zcmchisserver2'}

    if hostname and hostname.lower() in exempt_hosts:
        log_message(app, f"Skipping SPID {spid} - Host '{hostname}' is exempt")
        return

    if dbname in excluded_dbs:
        log_message(app, f"Skipping SPID {spid} - DB '{dbname}' is excluded")
        return
    if dry_run:
        log_message(app, f"Dry Run would kill SPID {spid} on DB '{dbname}'")

    try:
        kill_spid(conn, spid)
        log_message(app,
                    f"Killed SPID {spid} on DB '{dbname}'"
                            f"(Host: {hostname or 'unknown'})"
                    )

    except Exception as e:
        log_message(app, f"Failed to kill SPID {spid}: {e}")


def monitor_blockers(app, cfg):
    conn_str = cfg['database']['conn_str']
    kill_threshold = int(cfg['monitor']['kill_threshold'])

    conn = get_connection(conn_str)

    if not conn:
        log_message(app, "Database connection failed")
        return []

    try:
        blockers = find_head_blockers(conn)

        if not blockers:
            log_message(app, "No head blockers found")
            return

        eligible_blockers = [
            row for row in blockers
            if len(row) >= 4 and row[3] >= kill_threshold
        ]

        if not eligible_blockers:
            log_message(app, "No eligible blockers found")
            return

        for row in eligible_blockers:
            if len(row) >= 5:
                spid, host_name, blocked_count, wait_sec, dbname = row
            else:
                spid, blocked_count, wait_sec, dbname = row
                host_name = None

            log_message(
                app,
                f"SPID {spid} blocking {blocked_count} session(s)"
                        f"for {wait_sec} sec(s) on DB '{dbname}'"
                        f"(Host: {host_name or 'unknown'})"
            )


            safe_kill(conn, spid, dbname, app, cfg, host_name)

    except Exception as e:
        log_message(app, f"Failed to kill SPID {spid}: {e}")

    finally:
        conn.close()
