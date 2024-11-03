"""Utilities for deleting files."""

import asyncio
from pathlib import Path


async def del_temp_file(file_path: str) -> bool:
    """Delete a temporary file."""
    file_path_ = Path(file_path)

    try:
        if not file_path_.exists():
            return True

        await asyncio.to_thread(file_path_.unlink)

        return True

    except OSError as e:
        print(f"Error delete file: {e}")
        return False

    except Exception as e:
        print(f"Panic {file_path}: {str(e)}")
        return False
