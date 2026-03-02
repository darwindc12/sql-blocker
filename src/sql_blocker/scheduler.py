import threading
from datetime import datetime
from src.sql_blocker.monitor import monitor_blockers
from src.sql_blocker.logger import log_message


class Scheduler:
    """
    Handles background monitoring loop.
    """

    def __init__(self, app, cfg):
        self.app = app
        self.cfg = cfg
        self._stop_event = threading.Event()
        self._thread = None


    def _within_schedule(self):
        now = datetime.now().strftime("%H:%M")
        start_time = self.cfg["schedule"]["start_time"]
        stop_time = self.cfg["schedule"]["stop_time"]

        return start_time <= now <= stop_time


    def _run(self):
        log_message(self.app, "Scheduler started.")

        while not self._stop_event.is_set():

            try:
                interval = int(self.cfg["monitor"].get("kill_threshold", 60))
            except Exception:
                interval = 60

            if self._within_schedule():
                log_message(self.app, "⏱ Running monitor...")
                monitor_blockers(self.app, self.cfg)
            else:
                log_message(self.app, "Outside schedule window. Skipping monitor.")

            # Wait for interval seconds (but allow early stop)
            self._stop_event.wait(interval)

        log_message(self.app, "Scheduler stopped.")


    def start(self):
        if self._thread and self._thread.is_alive():
            log_message(self.app, "Scheduler already running.")
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()