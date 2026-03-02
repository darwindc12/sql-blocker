import logging
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, 'spid.log')

logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S %p'
                    )

def log_message(app, message):
    timestamp = f"{datetime.now().strftime('%H:%M:%S')} | {message}"
    logging.info(message)

    if app and hasattr(app, 'textbox'):
        app.textbox.after(0, lambda: (
            app.textbox.insert('end', timestamp + "\n"),
            app.textbox.see("end")
        ))
    else:
        print(timestamp)


