from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Finding:
    code: str
    severity: str
    path: str
    message: str
    fix: str = ""


@dataclass(slots=True)
class FileRecord:
    path: str
    size: int
    compressed_size: int | None = None


@dataclass(slots=True)
class ScanReport:
    target: str
    profile: str
    file_count: int = 0
    total_bytes: int = 0
    sha256: str = ""
    manifest: dict[str, str] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)
    files: list[FileRecord] = field(default_factory=list)

    @property
    def errors(self) -> int:
        return sum(item.severity == "ERROR" for item in self.findings)

    @property
    def warnings(self) -> int:
        return sum(item.severity == "WARNING" for item in self.findings)

    @property
    def status(self) -> str:
        if self.errors:
            return "FAIL"
        if self.warnings:
            return "REVIEW"
        return "READY"

    def to_dict(self, include_files: bool = False) -> dict[str, Any]:
        result = asdict(self)
        if not include_files:
            result.pop("files", None)
        result["status"] = self.status
        result["errors"] = self.errors
        result["warnings"] = self.warnings
        return result


@dataclass(slots=True)
class Source:
    target: Path
    records: list[FileRecord]
    findings: list[Finding]
    is_zip: bool

    def read(self, relative_path: str, limit: int) -> bytes | None:
        raise NotImplementedError

    def digest(self) -> str:
        raise NotImplementedError
