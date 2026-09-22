import pytest
from commit_helper import compose, parse, validate

def test_compose_scoped_breaking_message():
    msg = compose("feat", "change API", scope="auth", breaking=True, body="Migration required.", footers=["BREAKING CHANGE: tokens changed"])
    assert msg.header == "feat(auth)!: change API"
    assert "BREAKING CHANGE" in msg.render()

def test_parse_basic():
    msg = parse("fix(parser): handle empty input")
    assert (msg.type, msg.scope, msg.description) == ("fix", "parser", "handle empty input")

def test_validate_rejects_unknown_type():
    result = validate("feature: add thing")
    assert not result.valid and "unsupported type" in result.errors[0]

def test_header_limit():
    result = validate("feat: " + "x" * 80)
    assert not result.valid

def test_warnings_and_strict_mode():
    assert validate("fix: Handle crash.").valid
    strict = validate("fix: Handle crash.", strict=True)
    assert not strict.valid and len(strict.errors) == 2

def test_breaking_footer_warning():
    result = validate("feat!: change API")
    assert result.valid and result.warnings

def test_invalid_scope():
    with pytest.raises(ValueError): compose("feat", "work", scope="bad scope")
