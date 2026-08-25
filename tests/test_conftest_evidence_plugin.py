"""Meta-tests for the article-evidence plugin in ``tests/conftest.py``.

Covers the G3-examiner recommendation R6 (2026-08-22, QUALITAS Wave 8c):
a SUBSET pytest run (``-k``, ``-m``, ``--lf``, explicit paths or node-ids)
must never overwrite the canonical ``docs/reports/article_evidence_report.json``
whose ``gate_G3`` verdict reflects a FULL-suite run.  Partial runs instead
emit ``article_evidence_report_partial.json`` carrying ``"partial": true``,
``"gate_G3": "NOT_EVALUATED_PARTIAL_RUN"`` and full invocation provenance.

Test layers:

1. Unit tests for ``_is_partial_collection`` over a matrix of fake configs
   (keyword, markexpr, ignore, deselect, cache-selection flags, node-id
   arguments, sub-path arguments, bare/full-tree invocations).
2. In-process tests of ``pytest_terminal_summary`` with both artifact paths
   monkeypatched into ``tmp_path`` so the real artifacts are never touched.
3. An end-to-end subprocess reproduction of the original R6 defect:
   ``PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_defects_s1.py -q``
   must leave the canonical report byte-identical and write the partial
   artifact.  A fixture snapshots the canonical bytes and defensively
   restores them if the guard under test ever regresses.

These tests exercise infrastructure, not Treatise articles: no
``@pytest.mark.article`` markers are used here.
"""

from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import subprocess
import sys
from types import SimpleNamespace
from typing import Any

import pytest

# Load tests/conftest.py explicitly by path under a private module name so
# these meta-tests never depend on sys.path ordering or on pytest's own
# ``conftest`` import.  The module is side-effect-free at import time (hooks
# only run when pytest calls them), so a second instance is harmless.
_TESTS_DIR = pathlib.Path(__file__).resolve().parent
_PROJECT_ROOT = _TESTS_DIR.parent
_SPEC = importlib.util.spec_from_file_location(
    "maxwell_evidence_conftest_under_test", _TESTS_DIR / "conftest.py"
)
_conftest = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_conftest)


# ── Fakes ──────────────────────────────────────────────────────────


def _fake_config(
    *,
    args: list[str] | None = None,
    keyword: str | None = None,
    markexpr: str | None = None,
    ignore: list[str] | None = None,
    deselect: list[str] | None = None,
    inv_dir: pathlib.Path | None = None,
    **flags: Any,
) -> SimpleNamespace:
    """Build a duck-typed stand-in for pytest's ``Config`` object.

    Exposes exactly the surface ``_is_partial_collection`` and
    ``_invocation_info`` read: ``config.option.{keyword,markexpr,ignore,
    deselect,lf,last_failed,nf,new_first,ff,failed_first}``, ``config.args``
    and (optionally) ``config.invocation_params.dir``.
    """
    option = SimpleNamespace(
        keyword=keyword,
        markexpr=markexpr,
        ignore=list(ignore) if ignore else [],
        deselect=list(deselect) if deselect else [],
        lf=False,
        last_failed=False,
        nf=False,
        new_first=False,
        ff=False,
        failed_first=False,
    )
    for name, value in flags.items():
        setattr(option, name, value)
    cfg = SimpleNamespace(option=option, args=list(args or []))
    if inv_dir is not None:
        cfg.invocation_params = SimpleNamespace(dir=pathlib.Path(inv_dir))
    return cfg


class _FakeReporter:
    """Duck-typed TerminalReporter capturing write_sep/write_line calls."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def write_sep(self, sep: str, title: str) -> None:
        self.calls.append(("sep", title))

    def write_line(self, line: str) -> None:
        self.calls.append(("line", line))

    @property
    def text(self) -> str:
        return "\n".join(payload for _, payload in self.calls)


# ── 1. Unit tests: _is_partial_collection ──────────────────────────


def test_bare_invocation_is_a_full_run() -> None:
    """``pytest`` with no args (testpaths=["tests"]) collects everything."""
    assert _conftest._is_partial_collection(_fake_config()) is False


def test_explicit_tests_root_argument_is_a_full_run() -> None:
    """Pointing pytest at the whole tests tree collects the full universe."""
    cfg = _fake_config(args=[str(_TESTS_DIR)])
    assert _conftest._is_partial_collection(cfg) is False


def test_relative_tests_root_argument_is_a_full_run() -> None:
    """``pytest tests`` from the project root resolves to the tests tree."""
    cfg = _fake_config(args=["tests"], inv_dir=_PROJECT_ROOT)
    assert _conftest._is_partial_collection(cfg) is False


@pytest.mark.parametrize(
    "kwargs",
    [
        {"keyword": "oersted"},
        {"markexpr": "article(675)"},
        {"ignore": ["tests/test_slow.py"]},
        {"deselect": ["tests/test_x.py::test_y"]},
        {"lf": True},
        {"last_failed": True},
        {"nf": True},
        {"new_first": True},
        {"ff": True},
        {"failed_first": True},
    ],
    ids=[
        "keyword",
        "markexpr",
        "ignore",
        "deselect",
        "lf",
        "last_failed",
        "nf",
        "new_first",
        "ff",
        "failed_first",
    ],
)
def test_selector_options_force_partial(kwargs: dict[str, Any]) -> None:
    """Every subset-selecting pytest option must trip the partial guard."""
    cfg = _fake_config(args=[str(_TESTS_DIR)], **kwargs)
    assert _conftest._is_partial_collection(cfg) is True


def test_node_id_argument_is_always_partial() -> None:
    cfg = _fake_config(args=["tests/test_x.py::test_y"], inv_dir=_PROJECT_ROOT)
    assert _conftest._is_partial_collection(cfg) is True


def test_subpath_argument_is_partial() -> None:
    """A single file (or subdirectory) argument is a subset run."""
    cfg = _fake_config(args=["tests/test_defects_s1.py"], inv_dir=_PROJECT_ROOT)
    assert _conftest._is_partial_collection(cfg) is True
    cfg_dir = _fake_config(args=["tests/articles"], inv_dir=_PROJECT_ROOT)
    assert _conftest._is_partial_collection(cfg_dir) is True


def test_detection_is_selector_based_not_map_size_based() -> None:
    """R6 design point: even with a COMPLETE article map, a ``-k`` run stays
    partial — and conversely a bare full run is full regardless of map size.
    Detection keys off the invocation selectors, never the coverage count,
    so a genuine full run that lost an article still fails gate_G3 loudly.
    """
    full_map = {n: [f"tests/test_a.py::test_{n}"] for n in range(667, 867)}
    partial_cfg = _fake_config(keyword="something")
    partial_cfg._article_map = dict(full_map)
    assert _conftest._is_partial_collection(partial_cfg) is True
    full_cfg = _fake_config()
    full_cfg._article_map = {}
    assert _conftest._is_partial_collection(full_cfg) is False


# ── 2. Unit tests: _invocation_info ────────────────────────────────


def test_invocation_info_records_provenance() -> None:
    cfg = _fake_config(keyword="abc", args=["tests/test_x.py"])
    info = _conftest._invocation_info(cfg)
    assert set(info) == {"argv", "args", "keyword", "markexpr", "cwd"}
    assert info["args"] == ["tests/test_x.py"]
    assert info["keyword"] == "abc"
    assert info["markexpr"] is None
    assert isinstance(info["argv"], list)
    assert isinstance(info["cwd"], str)


# ── 3. In-process terminal_summary branch tests (artifacts in tmp) ─


def test_terminal_summary_partial_run_leaves_canonical_untouched(
    monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path
) -> None:
    canonical = tmp_path / "article_evidence_report.json"
    partial = tmp_path / "article_evidence_report_partial.json"
    monkeypatch.setattr(_conftest, "_ARTICLE_REPORT", canonical)
    monkeypatch.setattr(_conftest, "_ARTICLE_REPORT_PARTIAL", partial)
    sentinel = {"gate_G3": "PASS", "articles_covered": 200}
    canonical.write_text(json.dumps(sentinel))

    cfg = _fake_config(keyword="defect")
    cfg._article_map = {700: ["tests/test_x.py::test_y"]}
    reporter = _FakeReporter()
    _conftest.pytest_terminal_summary(reporter, pytest.ExitCode.OK, cfg)

    # Canonical must be byte-identical (never opened for writing).
    assert json.loads(canonical.read_text()) == sentinel
    data = json.loads(partial.read_text())
    assert data["partial"] is True
    assert data["gate_G3"] == "NOT_EVALUATED_PARTIAL_RUN"
    assert data["articles_covered"] == 1
    assert data["evidence"] == {"700": ["tests/test_x.py::test_y"]}
    assert data["invocation"]["keyword"] == "defect"
    assert "PARTIAL RUN" in reporter.text


def test_terminal_summary_full_run_writes_canonical_with_pass(
    monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path
) -> None:
    canonical = tmp_path / "article_evidence_report.json"
    partial = tmp_path / "article_evidence_report_partial.json"
    monkeypatch.setattr(_conftest, "_ARTICLE_REPORT", canonical)
    monkeypatch.setattr(_conftest, "_ARTICLE_REPORT_PARTIAL", partial)

    cfg = _fake_config(args=[str(_TESTS_DIR)])
    cfg._article_map = {n: [f"tests/test_a.py::test_{n}"] for n in range(667, 867)}
    reporter = _FakeReporter()
    _conftest.pytest_terminal_summary(reporter, pytest.ExitCode.OK, cfg)

    assert not partial.exists(), "full runs must not write the partial artifact"
    data = json.loads(canonical.read_text())
    assert data["gate_G3"] == "PASS"
    assert data["partial"] is False
    assert data["articles_covered"] == 200
    assert data["articles_missing"] == []
    assert data["range"] == [667, 866]
    assert "invocation" in data
    # Pre-R6 key set preserved for downstream consumers.
    for key in (
        "range",
        "generated",
        "articles_covered",
        "total_marked_tests",
        "articles_missing",
        "gate_G3",
        "evidence",
    ):
        assert key in data


def test_terminal_summary_full_run_with_missing_article_still_fails(
    monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path
) -> None:
    """A full run that lost coverage of one article must emit gate_G3 FAIL —
    the guard must never mask a genuine regression as 'partial'."""
    canonical = tmp_path / "article_evidence_report.json"
    monkeypatch.setattr(_conftest, "_ARTICLE_REPORT", canonical)
    monkeypatch.setattr(_conftest, "_ARTICLE_REPORT_PARTIAL", tmp_path / "partial.json")

    cfg = _fake_config(args=[str(_TESTS_DIR)])
    cfg._article_map = {n: [f"t.py::t{n}"] for n in range(667, 866)}  # 866 gone
    reporter = _FakeReporter()
    _conftest.pytest_terminal_summary(reporter, pytest.ExitCode.OK, cfg)

    data = json.loads(canonical.read_text())
    assert data["gate_G3"] == "FAIL"
    assert data["articles_missing"] == [866]
    assert data["partial"] is False


@pytest.mark.parametrize(
    "exit_code", [pytest.ExitCode.USAGE_ERROR, pytest.ExitCode.INTERNAL_ERROR]
)
def test_terminal_summary_aborted_session_writes_nothing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path, exit_code: int
) -> None:
    canonical = tmp_path / "article_evidence_report.json"
    partial = tmp_path / "article_evidence_report_partial.json"
    monkeypatch.setattr(_conftest, "_ARTICLE_REPORT", canonical)
    monkeypatch.setattr(_conftest, "_ARTICLE_REPORT_PARTIAL", partial)

    cfg = _fake_config(keyword="whatever")
    cfg._article_map = {}
    reporter = _FakeReporter()
    _conftest.pytest_terminal_summary(reporter, exit_code, cfg)

    assert not canonical.exists()
    assert not partial.exists()
    assert reporter.calls == []


# ── 4. End-to-end reproduction of the R6 defect scenario ───────────


@pytest.fixture
def canonical_snapshot():
    """Snapshot the canonical report bytes; defensively restore on teardown.

    If the guard under test ever regresses and clobbers the canonical file,
    the assertions below fail AND the original bytes are restored so the
    repository is left exactly as it was found.
    """
    canonical = _conftest._ARTICLE_REPORT
    before = canonical.read_bytes() if canonical.exists() else None
    yield before
    after = canonical.read_bytes() if canonical.exists() else None
    if after != before:
        if before is None:
            canonical.unlink(missing_ok=True)
        else:
            canonical.write_bytes(before)


def test_subset_subprocess_run_does_not_clobber_canonical_report(
    canonical_snapshot: bytes | None,
) -> None:
    """Reproduce the original R6 defect scenario and prove it is guarded.

    Command under test is the exact reproduction from the G3 recommendation:
    ``PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_defects_s1.py -q``.
    Before the fix this rewrote the canonical report with ``covered 7/200``
    and ``gate_G3: FAIL``.  After the fix the canonical bytes are untouched
    and the side artifact carries the partial-run provenance instead.
    """
    env = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_defects_s1.py", "-q"],
        cwd=_PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=600,
    )
    assert (
        proc.returncode == 0
    ), f"subset run failed (rc={proc.returncode}):\n{proc.stdout}\n{proc.stderr}"

    canonical = _conftest._ARTICLE_REPORT
    after = canonical.read_bytes() if canonical.exists() else None
    assert after == canonical_snapshot, (
        "R6 regression: subset run overwrote the canonical article evidence "
        "report (gate_G3 clobbered by partial coverage)"
    )

    partial = _conftest._ARTICLE_REPORT_PARTIAL
    assert partial.exists(), "partial artifact was not emitted on subset run"
    data = json.loads(partial.read_text())
    assert data["partial"] is True
    assert data["gate_G3"] == "NOT_EVALUATED_PARTIAL_RUN"
    assert data["range"] == [667, 866]
    assert data["articles_covered"] < 200, "single-file run cannot cover all 200"
    assert "invocation" in data
    assert "test_defects_s1.py" in " ".join(data["invocation"]["args"]) or any(
        "test_defects_s1.py" in part for part in data["invocation"]["argv"]
    )
    # Guard banner visible in the terminal summary of the subset run.
    assert "PARTIAL RUN" in proc.stdout
