import json
from pathlib import Path


class DTCResolver:
    """Resolves DTC codes using the local JSON database."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path
        self._database = self._load_database()

    def _load_database(self) -> dict:
        with self._database_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def resolve(self, code: int) -> dict | None:
        """Return the DTC definition or None if it is unknown."""

        key = f"{code:06X}"

        return self._database.get(key)
