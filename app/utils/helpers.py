import uuid
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())

def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="EE dd.MM.y HH:mm"
    return datetime.strftime(value, format)