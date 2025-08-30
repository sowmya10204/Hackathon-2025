# utils/text_utils.py
from typing import List

def chunk_text(text: str, max_chars: int = 3000) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start:start+max_chars]
        chunks.append(chunk)
        start += max_chars
    return chunks
