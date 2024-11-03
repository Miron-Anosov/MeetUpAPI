"""Process with pictures."""

from pathlib import Path

import aiofiles

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
UPLOAD_DIR = PROJECT_ROOT / "temp_uploads"
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)


async def download_file(receiver_id: str, file: bytes, filename: str) -> str:
    """Save temp file to disk."""
    temp_path: Path = UPLOAD_DIR / f"{receiver_id}_{filename}"

    async with aiofiles.open(temp_path, "wb") as out_file:
        await out_file.write(file)

    return str(temp_path)
