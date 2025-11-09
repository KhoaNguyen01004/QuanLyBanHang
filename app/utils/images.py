import os
import re
from typing import Optional

_slug_regex = re.compile(r'[^a-z0-9]+')

IMAGE_DIR = os.path.join('static', 'images', 'items')
DEFAULT_IMAGE_REL = 'images/items/default.png'

SUPPORTED_EXTS = ['png', 'jpg', 'jpeg', 'webp', 'svg', 'gif']

def slugify(name: str) -> str:
    if not name:
        return 'item'
    name = name.lower().strip()
    name = _slug_regex.sub('-', name)
    name = re.sub(r'-{2,}', '-', name).strip('-')
    return name or 'item'

def normalize_stored_path(pic_path: str) -> str:
    # Normalize any stored DB value to relative path under images/
    if not pic_path:
        return ''
    if pic_path.startswith('images/'):
        return pic_path
    if pic_path.startswith('/static/images/'):
        return pic_path[len('/static/'):]
    # If it's just a filename, assume it lives in images/items/
    return f"images/items/{pic_path}"

def resolve_picture_path(pic_path: Optional[str], name: Optional[str]) -> str:
    # 1) If DB provided something, normalize and use it
    if pic_path:
        normalized = normalize_stored_path(pic_path)
        return normalized
    # 2) Try to infer from slug and available files
    if name:
        slug = slugify(name)
        for ext in SUPPORTED_EXTS:
            candidate = f"images/items/{slug}.{ext}"
            if os.path.exists(os.path.join('static', candidate)):
                return candidate
    # 3) Fallback
    return DEFAULT_IMAGE_REL

