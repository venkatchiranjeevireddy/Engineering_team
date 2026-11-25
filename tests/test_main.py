"""Unit tests for the crew entry point without network or Docker dependencies."""

import importlib
import sys
import types
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def entrypoint(monkeypatch):
    fake_crew_module = types.ModuleType("engineering_team.crew")
    fake_crew_module.EngineeringTeam = MagicMock()
    monkeypatch.setitem(sys.modules, "engineering_team.crew", fake_crew_module)
    monkeypatch.delitem(sys.modules, "engineering_team.main", raising=False)

    module = importlib.import_module("engineering_team.main")
    yield module, fake_crew_module.EngineeringTeam
    monkeypatch.delitem(sys.modules, "engineering_team.main", raising=False)


def test_run_creates_output_and_returns_kickoff_result(entrypoint, monkeypatch):
    module, team = entrypoint
    mkdir = MagicMock()
    monkeypatch.setattr(module.os, "makedirs", mkdir)
    monkeypatch.setattr(module.os.path, "isdir", lambda path: True)
    expected = object()
    team.return_value.crew.return_value.kickoff.return_value = expected

    result = module.run()

    assert result is expected
    mkdir.assert_called_once_with("output", exist_ok=True)
    team.return_value.crew.return_value.kickoff.assert_called_once_with(
        inputs={
            "requirements": module.requirements,
            "module_name": "accounts.py",
            "class_name": "Account",
        }
    )


def test_run_rejects_non_directory_output_before_kickoff(entrypoint, monkeypatch):
    module, team = entrypoint
    monkeypatch.setattr(module.os, "makedirs", MagicMock())
    monkeypatch.setattr(module.os.path, "isdir", lambda path: False)

    with pytest.raises(NotADirectoryError, match="output path"):
        module.run()

    team.assert_not_called()


def test_run_propagates_output_creation_failure_without_starting_crew(entrypoint, monkeypatch):
    module, team = entrypoint
    mkdir = MagicMock(side_effect=PermissionError("output directory is not writable"))
    monkeypatch.setattr(module.os, "makedirs", mkdir)

    with pytest.raises(PermissionError, match="not writable"):
        module.run()

    mkdir.assert_called_once_with("output", exist_ok=True)
    team.assert_not_called()


def test_run_propagates_kickoff_failure(entrypoint, monkeypatch):
    module, team = entrypoint
    monkeypatch.setattr(module.os, "makedirs", MagicMock())
    monkeypatch.setattr(module.os.path, "isdir", lambda path: True)
    kickoff = team.return_value.crew.return_value.kickoff
    kickoff.side_effect = RuntimeError("crew kickoff failed")

    with pytest.raises(RuntimeError, match="crew kickoff failed"):
        module.run()

    kickoff.assert_called_once()


@pytest.mark.parametrize("preexisting_output", [False, True])
def test_run_handles_real_output_directory(entrypoint, monkeypatch, tmp_path, preexisting_output):
    module, team = entrypoint
    monkeypatch.chdir(tmp_path)
    output_dir = tmp_path / "output"
    if preexisting_output:
        output_dir.mkdir()

    expected = object()
    team.return_value.crew.return_value.kickoff.return_value = expected

    assert module.run() is expected
    assert output_dir.is_dir()
    team.return_value.crew.return_value.kickoff.assert_called_once()


def test_run_preserves_existing_file_at_output_path(entrypoint, monkeypatch, tmp_path):
    module, team = entrypoint
    monkeypatch.chdir(tmp_path)
    output_file = tmp_path / "output"
    output_file.write_text("existing data", encoding="utf-8")

    with pytest.raises(FileExistsError):
        module.run()

    assert output_file.read_text(encoding="utf-8") == "existing data"
    team.assert_not_called()
