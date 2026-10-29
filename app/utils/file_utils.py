import hashlib
import os
import re
import shutil
import uuid
from fastapi import UploadFile, HTTPException

from app.core.config import settings


def ensure_directories():
    """
    Create required directories if not present.
    """
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    sqlite_dir = os.path.dirname(settings.SQLITE_DB_PATH)
    if sqlite_dir:
        os.makedirs(sqlite_dir, exist_ok=True)

    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """
    Make file name safer for saving on disk.
    Example:
        'HR Policy (Final).pdf'
        -> 'HR_Policy_Final.pdf'
    """
    filename = filename.strip()
    filename = filename.replace(" ", "_")
    filename = re.sub(r"[^A-Za-z0-9._-]", "", filename)
    return filename


def get_file_extension(filename: str) -> str:
    """
    Return lowercase file extension.
    Example:
        test.PDF -> .pdf
    """
    return os.path.splitext(filename)[1].lower()


def validate_upload_file(file: UploadFile):
    """
    Validate:
    - filename exists
    - extension allowed
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a filename.")

    ext = get_file_extension(file.filename)
    if ext not in settings.SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: {ext}. "
                f"Allowed types: {', '.join(settings.SUPPORTED_EXTENSIONS)}"
            )
        )


def save_upload_file(file: UploadFile) -> str:
    """
    Save uploaded file to UPLOAD_DIR with unique safe filename.
    Returns saved file path.
    """
    validate_upload_file(file)
    ensure_directories()

    original_name = sanitize_filename(file.filename)
    ext = get_file_extension(original_name)

    base_name = os.path.splitext(original_name)[0]
    unique_name = f"{base_name}_{uuid.uuid4().hex[:8]}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_name)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Size validation after save
    file_size_bytes = os.path.getsize(file_path)
    max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024

    if file_size_bytes > max_size_bytes:
        os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds {settings.MAX_FILE_SIZE_MB} MB limit."
        )

    return file_path


def calculate_sha256(file_path: str) -> str:
    """
    Calculate SHA256 hash of a file.
    Used for duplicate detection.
    """
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()