import tkinter as tk
from src.sql_blocker.gui import BlockerMonitorApp
from src.sql_blocker.logger import log_message

def main():
    root = tk.Tk()
    root.withdraw()

    app = BlockerMonitorApp(root)
    app.show_login()

    log_message(app, "SQL Blocker Monitor Initiated.")
    root.mainloop()