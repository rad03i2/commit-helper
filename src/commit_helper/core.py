from __future__ import annotations

from dataclasses import dataclass, asdict
import re
from typing import Iterable

TYPES = ("build", "chore", "ci", "docs", "feat", "fix", "perf", "refactor", "revert", "style", "test")
_HEADER = re.compile(r"^(?P<type>[a-z]+)(?:\((?P<scope>[A-Za-z0-9._/-]+)\))?(?P<breaking>!)?: (?P<description>.+)$")

@dataclass(frozen=True)
class CommitMessage:
    type: str
    description: str
    scope: str | None = None
    breaking: bool = False
    body: str | None = None
    footers: tuple[str, ...] = ()

    @property
    def header(self) -> str:
        scope = f"({self.scope})" if self.scope else ""
        bang = "!" if self.breaking else ""
        return f"{self.type}{scope}{bang}: {self.description}"

    def render(self) -> str:
        parts = [self.header]
        if self.body:
            parts.extend(["", self.body.strip()])
        if self.footers:
            parts.extend(["", *self.footers])
        return "\n".join(parts)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["footers"] = list(self.footers)
        data["header"] = self.header
        return data

@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    message: CommitMessage | None

    def to_dict(self) -> dict:
        return {"valid": self.valid, "errors": list(self.errors), "warnings": list(self.warnings), "message": self.message.to_dict() if self.message else None}

def compose(type_: str, description: str, *, scope: str | None = None, breaking: bool = False, body: str | None = None, footers: Iterable[str] = ()) -> CommitMessage:
    type_ = type_.strip().lower()
    description = description.strip()
    if type_ not in TYPES:
        raise ValueError(f"unsupported type: {type_}")
    if not description:
        raise ValueError("description must not be empty")
    if scope is not None:
        scope = scope.strip()
        if not scope or not re.fullmatch(r"[A-Za-z0-9._/-]+", scope):
            raise ValueError("scope may contain only letters, digits, '.', '_', '/', and '-'")
    footer_tuple = tuple(x.strip() for x in footers if x.strip())
    return CommitMessage(type_, description, scope, breaking, body.strip() if body else None, footer_tuple)

def parse(text: str) -> CommitMessage:
    normalized = text.replace("\r\n", "\n").strip()
    if not normalized:
        raise ValueError("commit message is empty")
    lines = normalized.split("\n")
    match = _HEADER.fullmatch(lines[0])
    if not match:
        raise ValueError("header does not follow '<type>(<scope>): <description>'")
    rest = lines[1:]
    sections: list[list[str]] = []
    current: list[str] = []
    for line in rest:
        if not line.strip():
            if current:
                sections.append(current); current = []
        else:
            current.append(line)
    if current: sections.append(current)
    body = "\n".join(sections[0]) if sections else None
    footers = tuple(line for section in sections[1:] for line in section)
    return CommitMessage(match["type"], match["description"], match["scope"], bool(match["breaking"]), body, footers)

def validate(text: str, *, max_header: int = 72, strict: bool = False) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        msg = parse(text)
    except ValueError as exc:
        return ValidationResult(False, (str(exc),), (), None)
    if msg.type not in TYPES:
        errors.append(f"unsupported type '{msg.type}'; choose one of: {', '.join(TYPES)}")
    if len(msg.header) > max_header:
        errors.append(f"header is {len(msg.header)} characters; maximum is {max_header}")
    if msg.description.endswith("."):
        warnings.append("description usually should not end with a period")
    if msg.description and msg.description[0].isupper():
        warnings.append("description conventionally starts with lowercase text")
    if msg.breaking and not any(f.lower().startswith("breaking change:") for f in msg.footers):
        warnings.append("breaking marker '!' is present without a BREAKING CHANGE footer")
    if strict and warnings:
        errors.extend(warnings); warnings = []
    return ValidationResult(not errors, tuple(errors), tuple(warnings), msg)
