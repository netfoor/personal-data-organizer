from pathlib import Path
import re


_WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:([\\/].*)?$")


def normalize_input_path(value: str | Path) -> Path:
    """Normalize user-provided paths across Windows and Linux/WSL environments."""
    raw = str(value).strip().strip('"').strip("'")

    if not raw:
        return Path(raw)

    if _WINDOWS_DRIVE_RE.match(raw):
        drive_letter = raw[0].lower()
        remainder = raw[2:].replace("\\", "/").lstrip("/")
        wsl_path = f"/mnt/{drive_letter}"
        if remainder:
            wsl_path = f"{wsl_path}/{remainder}"
        return Path(wsl_path)

    return Path(raw.replace("\\", "/"))