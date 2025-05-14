import hashlib
from datetime import datetime

def generate_file_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def format_timestamp(ts: datetime) -> str:
    return ts.isoformat() + "Z"