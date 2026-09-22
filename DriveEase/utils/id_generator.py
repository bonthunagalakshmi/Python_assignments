import re
from typing import Iterable


def next_identifier(prefix: str, existing_ids: Iterable[str], start: int = 1001) -> str:
    """Return the next unused PREFIX#### identifier."""
    numbers = []
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+)$", re.IGNORECASE)
    for value in existing_ids:
        match = pattern.match(str(value).strip())
        if match:
            numbers.append(int(match.group(1)))
    number = max(numbers, default=start - 1) + 1
    return f"{prefix}{number}"