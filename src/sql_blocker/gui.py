import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog

from src.sql_blocker.config import config, save_config, PASSCODE
from src.sql_blocker.scheduler import Scheduler



class BlockerMonitorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("SQL Blocker Monitor")
        self.root.geometry("850x600")

        # Initialize scheduler
        self.scheduler = Scheduler(self, config)

        # Tab setup
        self.tabs = ttk.Notebook(root)
        self.monitor_tab = ttk.Frame(self.tabs)
        self.config_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.monitor_tab, text="🧩 Monitor")
        self.tabs.add(self.config_tab, text="⚙️ Configuration")
        self.tabs.pack(expand=1, fill="both")

        self.tabs.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # Monitor Tab

        self.textbox = scrolledtext.ScrolledText(
            self.monitor_tab,
            width=100,
            height=25,
            bg="#1E1E1E",
            fg="#00FF00"
        )
        self.textbox.pack(padx=10, pady=(10, 5))

        button_frame = tk.Frame(self.monitor_tab)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="Start Monitor",
            command=self.start_monitor,
            bg="#4CAF50",
            fg="white"
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="Stop Monitor",
            command=self.stop_monitor,
            bg="#F44336",
            fg="white"
        ).pack(side=tk.LEFT, padx=10)

        # Footer
        footer_label = tk.Label(
            self.monitor_tab,
            text="⚙️ SQL Blocker Monitor\nIHOMP",
            font=("Segoe UI", 9, "italic"),
            fg="#AAAAAA",
            justify="center",
        )
        footer_label.pack(side=tk.BOTTOM, pady=10)

        # Configuration Tab (Locked)

        self.config_locked = True
        self.lock_message = tk.Label(
            self.config_tab,
            text="🔒 Configuration Locked\nEnter Passcode to Unlock",
            font=("Arial", 14),
            pady=100,
        )
        self.lock_message.pack()

        self.config_frame = None

    # Scheduler Controls

    def start_monitor(self):
        self.scheduler.start()

    def stop_monitor(self):
        self.scheduler.stop()

    # Config Tab Handling

    def on_tab_change(self, event):
        current_tab = event.widget.tab(event.widget.index("current"))["text"]

        if "Configuration" in current_tab and self.config_locked:
            entered = simpledialog.askstring(
                "Authorization Required",
                "Enter passcode to unlock configuration:",
                show="*"
            )

            if entered == PASSCODE:
                self.config_locked = False
                self.unlock_config_tab()
                messagebox.showinfo("Access Granted", "🔓 Configuration unlocked.")
            else:
                messagebox.showwarning("Access Denied", "❌ Incorrect passcode.")
                self.tabs.select(self.monitor_tab)

    def unlock_config_tab(self):
        self.lock_message.pack_forget()

        self.config_frame = tk.Frame(self.config_tab)
        self.config_frame.pack(padx=10, pady=10, fill="both", expand=True)

        f = self.config_frame

        # Connection String
        tk.Label(f, text="Connection String:").grid(row=0, column=0, sticky="e")
        self.conn_str_entry = tk.Entry(f, width=80)
        self.conn_str_entry.grid(row=0, column=1)
        self.conn_str_entry.insert(0, config["database"]["conn_str"])

        # Kill Threshold
        tk.Label(f, text="Kill Threshold (s):").grid(row=1, column=0, sticky="e")
        self.kill_entry = tk.Entry(f, width=10)
        self.kill_entry.grid(row=1, column=1, sticky="w")
        self.kill_entry.insert(0, config["monitor"]["kill_threshold"])

        # Save Button

        tk.Button(
            f,
            text="💾 Save Config",
            command=self.save_config_gui,
            bg="#2196F3",
            fg="white"
        ).grid(row=5, column=1, sticky="w", pady=15)

        tk.Button(
            f,
            text="Test Connection",
            command=self.test_connection_gui,
            bg="#4CAF50",
            fg="white"
        ).grid(row=6, column=1, sticky="w", pady=15)

    def save_config_gui(self):
        new_values = {
            "conn_str": self.conn_str_entry.get(),
            "kill_threshold": self.kill_entry.get(),
            "excluded_dbs": config["monitor"]["excluded_dbs"],
            "dry_run": config["monitor"]["dry_run"],
            "start_time": config["schedule"]["start_time"],
            "stop_time": config["schedule"]["stop_time"]
        }

        save_config(new_values)
        messagebox.showinfo("Saved", "Configuration saved successfully.")

    def test_connection_gui(self):

        conn_str = self.conn_str_entry.get().strip()
        if not conn_str:
            messagebox.showerror("Connection Error", "Please enter a connection string.")
            return

        from src.sql_blocker.tests.test_sql_utils import get_connection
        conn = get_connection(conn_str)
        if conn:
            messagebox.showinfo("Connection Successful", "Connection successful.")
            conn.close()
        else:
            messagebox.showerror("Connection Error", "Please enter a valid connection string.")