import time
from datetime import datetime
from .monitor import monitor_blockers
from .logger import  log_message

running = False
stop_thread = False

def within_schedule(cfg):
    now = datetime.now().strftime('%H:%M')
    return cfg["schedule"]["start_time"] <= now <= cfg["schedule"]["stop_time"]

def scheduler_loop(app, cfg):
    global running, stop_thread

    while not stop_thread:
        try:
            interval = int(cfg["monitor"].get("kill_threshold", 60))
        except Exception:
            interval = 60

        log_message(app, f"Scheduler tick... (interval: {interval}s)")

        if within_schedule(cfg):
            if not running:
                log_message(app, f"Within schedule window - starting monitor.")
                running = True
                monitor_blockers(app, cfg)
            else:
                log_message(app, f"Outside schedule window - stopping monitor.")
                running = False

            time.sleep(interval)


