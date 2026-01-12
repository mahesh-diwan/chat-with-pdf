from datetime import datetime

def timestamp():
    return datetime.now().strftime("%H:%M")
