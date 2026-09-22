from commit_helper.cli import main

def test_compose_cli(capsys):
    assert main(["compose", "feat", "add export", "--scope", "cli"]) == 0
    assert capsys.readouterr().out.strip() == "feat(cli): add export"

def test_validate_cli(capsys):
    assert main(["validate", "--message", "fix: handle crash"]) == 0
    assert "valid" in capsys.readouterr().out

def test_invalid_cli(capsys):
    assert main(["validate", "--message", "not conventional"]) == 1
    assert "invalid" in capsys.readouterr().out

def test_json_cli(capsys):
    assert main(["validate", "--message", "docs: update readme", "--json"]) == 0
    assert '"valid": true' in capsys.readouterr().out
