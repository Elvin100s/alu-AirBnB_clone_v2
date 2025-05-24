#!/usr/bin/python3
"""Initialize models package."""
from os import getenv

# Debug: Print environment variables (optional)
print("[DEBUG] HBNB_TYPE_STORAGE:", getenv('HBNB_TYPE_STORAGE'))

try:
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        from models.engine.db_storage import DBStorage
        storage = DBStorage()
    else:
        from models.engine.file_storage import FileStorage
        storage = FileStorage()
    
    storage.reload()
    print("[DEBUG] Storage initialized:", type(storage).__name__)  # Debug
except ImportError as e:
    print("[ERROR] Failed to initialize storage:", e)
    raise
except Exception as e:
    print("[ERROR] Unexpected error:", e)
    raise
