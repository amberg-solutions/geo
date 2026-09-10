import json
import os
from config import FILE_DIR

@staticmethod
def write_json(file_name: str, content: list | dict) -> None:
    file_path = os.path.join(FILE_DIR, file_name) 
    with open(file_path, "w", encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)