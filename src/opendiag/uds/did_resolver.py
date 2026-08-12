import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DIDDefinition:
    """Represents a diagnostic data identifier definition."""

    name: str
    type: str
    length: int


class DIDResolver:
    """Resolves diagnostic data identifiers from a JSON database."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path
        self._database = self._load_database()

    def _load_database(self) -> dict:
        with self._database_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def resolve(self, did: int) -> DIDDefinition | None:
        entry = self._database.get(f"{did:04X}")

        if entry is None:
            return None

        return DIDDefinition(
            name=entry["name"],
            type=entry["type"],
            length=entry["length"],
        )
