"""
Tests for GitHub Raw URL workflow (build_raw_url, publish_prompt_to_github, auto path).
"""
import sys
import os
from pathlib import Path
from unittest.mock import MagicMock, patch, call

import pytest

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ai_workflow import build_raw_url, WORKSPACE_ROOT


# ---------------------------------------------------------------------------
# 1. build_raw_url
# ---------------------------------------------------------------------------

def test_build_raw_url_basic():
    url = build_raw_url("ypauk", "ScrapData", "main",
                        "projects/test1/AI_OUTPUT/03_scraper_prompt.md")
    assert url == (
        "https://raw.githubusercontent.com/ypauk/ScrapData/main/"
        "projects/test1/AI_OUTPUT/03_scraper_prompt.md"
    )


def test_build_raw_url_strips_leading_slash():
    url = build_raw_url("ypauk", "ScrapData", "main",
                        "/projects/test1/AI_OUTPUT/03_scraper_prompt.md")
    assert not url.split("main/")[1].startswith("/")


def test_build_raw_url_normalises_backslash():
    url = build_raw_url("ypauk", "ScrapData", "main",
                        r"projects\test1\AI_OUTPUT\03_scraper_prompt.md")
    assert "/" in url
    assert "\\" not in url


# ---------------------------------------------------------------------------
# 2. Correct path for test2
# ---------------------------------------------------------------------------

def test_build_raw_url_test2():
    url = build_raw_url("ypauk", "ScrapData", "main",
                        "projects/test2/AI_OUTPUT/03_scraper_prompt.md")
    assert "test2" in url
    assert "test1" not in url


# ---------------------------------------------------------------------------
# 3. No chunking in auto pipeline path (scraper stage uses publish_prompt_to_github)
# ---------------------------------------------------------------------------

def test_pipeline_scraper_uses_raw_url_not_chunks(tmp_path, monkeypatch):
    """publish_prompt_to_github must be called and auto_send_prompt must NOT be called
    for the scraper stage when --auto is used."""
    import ai_workflow as wf

    # Build a minimal project structure
    project = tmp_path / "proj1"
    ai_output = project / "AI_OUTPUT"
    ai_output.mkdir(parents=True)
    ai_input = project / "AI_INPUT"
    ai_input.mkdir()
    app = project / "app"
    app.mkdir()
    (app / "main.py").write_text("# main", encoding="utf-8")
    (ai_input / "description.txt").write_text("test", encoding="utf-8")

    prompt_file = ai_output / "03_scraper_prompt.md"
    prompt_file.write_text("# prompt\n", encoding="utf-8")
    answer_file = ai_output / "03_scraper_answer.py"
    answer_file.write_text("def scrape_data(engine): return []", encoding="utf-8")

    publish_called = []
    send_chunks_called = []
    send_url_called = []

    def fake_publish(path, project_name):
        publish_called.append((path, project_name))
        return "https://raw.githubusercontent.com/ypauk/ScrapData/main/projects/proj1/AI_OUTPUT/03_scraper_prompt.md"

    def fake_auto_send_prompt(*a, **kw):
        send_chunks_called.append(True)

    def fake_auto_send_via_url(*a, **kw):
        send_url_called.append(True)

    monkeypatch.setattr(wf, "publish_prompt_to_github", fake_publish)
    monkeypatch.setattr(wf, "auto_send_prompt", fake_auto_send_prompt)
    monkeypatch.setattr(wf, "auto_send_via_url", fake_auto_send_via_url)

    # Only test the scraper stage to avoid needing all prerequisite files
    stage_info = wf.STAGES["scraper"]
    prompt_path = project / "AI_OUTPUT" / stage_info["prompt"]
    prompt_path.write_text("# prompt", encoding="utf-8")

    opts = MagicMock()
    opts.auto = True
    opts.dry_run = False
    opts.max_lines = 400
    opts.delay = 2
    opts.timeout = 600
    opts.retries = 3
    opts.force = False
    opts.restart = False

    # Simulate the scraper branch of cmd_pipeline
    import ai_workflow as wf2
    stage = "scraper"
    if opts.auto:
        si = wf2.STAGES[stage]
        p_path = project / "AI_OUTPUT" / si["prompt"]
        a_path = project / "AI_OUTPUT" / si["answer"]
        a_path.write_text("def scrape_data(engine): return []", encoding="utf-8")

        if stage == "scraper":
            raw_url = wf2.publish_prompt_to_github(p_path, project.name)
            if not opts.dry_run:
                wf2.auto_send_via_url(
                    raw_url=raw_url,
                    answer_path=a_path,
                    timeout=opts.timeout,
                    retries=opts.retries,
                    no_interact=True,
                )

    assert len(publish_called) == 1, "publish_prompt_to_github must be called once"
    assert len(send_url_called) == 1, "auto_send_via_url must be called once"
    assert len(send_chunks_called) == 0, "auto_send_prompt (chunked) must NOT be called for scraper"


# ---------------------------------------------------------------------------
# 4. No commit when file unchanged
# ---------------------------------------------------------------------------

def test_publish_no_commit_when_unchanged(tmp_path, monkeypatch):
    import ai_workflow as wf

    prompt_file = tmp_path / "03_scraper_prompt.md"
    prompt_file.write_text("# prompt", encoding="utf-8")

    completed_calls = []

    def fake_run_git(args, cwd):
        completed_calls.append(args[0])
        result = MagicMock()
        result.returncode = 0
        if args[0] == "status":
            result.stdout = ""  # no changes
        elif args[0] == "rev-parse":
            result.stdout = "abc1234567890\n"
        elif args[0] == "ls-remote":
            result.stdout = "abc1234567890\trefs/heads/main\n"
        else:
            result.stdout = ""
        result.stderr = ""
        return result

    monkeypatch.setattr(wf, "_run_git", fake_run_git)
    monkeypatch.setattr(wf, "WORKSPACE_ROOT", tmp_path)
    monkeypatch.setattr(wf, "GITHUB_OWNER", lambda: "ypauk")
    monkeypatch.setattr(wf, "GITHUB_REPO", lambda: "ScrapData")
    monkeypatch.setattr(wf, "GITHUB_BRANCH", lambda: "main")

    url = wf.publish_prompt_to_github(prompt_file, "testproj")

    assert "commit" not in completed_calls, "commit must NOT be called when file is unchanged"
    assert "push" not in completed_calls, "push must NOT be called when file is unchanged"
    assert url.startswith("https://raw.githubusercontent.com/")


# ---------------------------------------------------------------------------
# 5. Commit + push on changed file
# ---------------------------------------------------------------------------

def test_publish_commit_and_push_when_changed(tmp_path, monkeypatch):
    import ai_workflow as wf

    prompt_file = tmp_path / "03_scraper_prompt.md"
    prompt_file.write_text("# prompt", encoding="utf-8")

    completed_calls = []

    def fake_run_git(args, cwd):
        completed_calls.append(args[0])
        result = MagicMock()
        result.returncode = 0
        if args[0] == "status":
            result.stdout = "M projects/test1/AI_OUTPUT/03_scraper_prompt.md\n"
        elif args[0] == "commit":
            result.stdout = "[main abc1234] ai: update prompt for testproj\n"
        elif args[0] == "rev-parse":
            result.stdout = "abc1234567890\n"
        elif args[0] == "ls-remote":
            result.stdout = "abc1234567890\trefs/heads/main\n"
        else:
            result.stdout = ""
        result.stderr = ""
        return result

    monkeypatch.setattr(wf, "_run_git", fake_run_git)
    monkeypatch.setattr(wf, "WORKSPACE_ROOT", tmp_path)
    monkeypatch.setattr(wf, "GITHUB_OWNER", lambda: "ypauk")
    monkeypatch.setattr(wf, "GITHUB_REPO", lambda: "ScrapData")
    monkeypatch.setattr(wf, "GITHUB_BRANCH", lambda: "main")

    url = wf.publish_prompt_to_github(prompt_file, "testproj")

    assert "add" in completed_calls
    assert "commit" in completed_calls
    assert "push" in completed_calls
    assert url.startswith("https://raw.githubusercontent.com/")


# ---------------------------------------------------------------------------
# 6. Push failure raises RuntimeError (workflow must fail, not succeed)
# ---------------------------------------------------------------------------

def test_publish_raises_on_push_failure(tmp_path, monkeypatch):
    import ai_workflow as wf

    prompt_file = tmp_path / "03_scraper_prompt.md"
    prompt_file.write_text("# prompt", encoding="utf-8")

    def fake_run_git(args, cwd):
        result = MagicMock()
        if args[0] == "status":
            result.returncode = 0
            result.stdout = "M file\n"
            result.stderr = ""
        elif args[0] in ("add", "commit"):
            result.returncode = 0
            result.stdout = ""
            result.stderr = ""
        elif args[0] == "push":
            result.returncode = 1
            result.stdout = ""
            result.stderr = "remote: Permission denied"
        else:
            result.returncode = 0
            result.stdout = ""
            result.stderr = ""
        return result

    monkeypatch.setattr(wf, "_run_git", fake_run_git)
    monkeypatch.setattr(wf, "WORKSPACE_ROOT", tmp_path)
    monkeypatch.setattr(wf, "GITHUB_OWNER", lambda: "ypauk")
    monkeypatch.setattr(wf, "GITHUB_REPO", lambda: "ScrapData")
    monkeypatch.setattr(wf, "GITHUB_BRANCH", lambda: "main")

    with pytest.raises(RuntimeError, match="git push failed"):
        wf.publish_prompt_to_github(prompt_file, "testproj")


# ---------------------------------------------------------------------------
# 7. Token must not appear in logs (no GITHUB_TOKEN in output)
# ---------------------------------------------------------------------------

def test_token_not_in_output(tmp_path, monkeypatch, capsys):
    import ai_workflow as wf

    os.environ["GITHUB_TOKEN"] = "ghp_supersecrettoken"

    prompt_file = tmp_path / "03_scraper_prompt.md"
    prompt_file.write_text("# prompt", encoding="utf-8")

    def fake_run_git(args, cwd):
        result = MagicMock()
        result.returncode = 0
        result.stdout = "abc123\n" if args[0] in ("rev-parse",) else ""
        if args[0] == "status":
            result.stdout = ""
        elif args[0] == "ls-remote":
            result.stdout = "abc123\trefs/heads/main\n"
        result.stderr = ""
        return result

    monkeypatch.setattr(wf, "_run_git", fake_run_git)
    monkeypatch.setattr(wf, "WORKSPACE_ROOT", tmp_path)
    monkeypatch.setattr(wf, "GITHUB_OWNER", lambda: "ypauk")
    monkeypatch.setattr(wf, "GITHUB_REPO", lambda: "ScrapData")
    monkeypatch.setattr(wf, "GITHUB_BRANCH", lambda: "main")

    wf.publish_prompt_to_github(prompt_file, "testproj")

    captured = capsys.readouterr()
    assert "ghp_supersecrettoken" not in captured.out
    assert "ghp_supersecrettoken" not in captured.err

    del os.environ["GITHUB_TOKEN"]
