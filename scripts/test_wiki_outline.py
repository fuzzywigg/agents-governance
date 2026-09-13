#!/usr/bin/env python3
"""TOKENMAXX wiki-outline gate self-tests (dedicated slice — not mega-fixtures).

Deepens check_wiki_outline.py only: L2/L3/kill_switch + SECURITY.md/credential +
copilot/geryon + AGENTS-ECOSYSTEM/scratchpad + test_stewardship_gates.py topic
pins, Home ecosystem link / ## Out of scope / smtp.eth, PUBLISH .wiki.git +
docs/wiki + MEMORY, protocol-relative links, ATX H1 / empty-page pins, fenced
scheme strip, invent-chrome on PUBLISH, helper unit tests. No invent-product.
Wired into stewardship-checks.yml after the live-tree gates.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def _load_wiki_module():
    path = SCRIPTS / "check_wiki_outline.py"
    spec = importlib.util.spec_from_file_location("check_wiki_outline", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


WIKI = _load_wiki_module()


def run(script: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script)],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _seed_scripts(tmp: Path) -> Path:
    scripts_dir = tmp / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    for name in ("stewardship_common.py", "check_wiki_outline.py"):
        shutil.copy2(SCRIPTS / name, scripts_dir / name)
    return scripts_dir


def _good_pages() -> dict[str, str]:
    return {
        "Home.md": (
            "# Home\n\n"
            "[README](https://github.com/fuzzywigg/agents-governance/blob/main/README.md)\n"
            "[AGENTS-ECOSYSTEM](https://github.com/fuzzywigg/agents-governance/"
            "blob/main/AGENTS-ECOSYSTEM.md)\n"
            "[Badge](../badge-standard.md)\n"
            "[Overview](Overview.md)\n"
            "[Autonomy-Levels](Autonomy-Levels.md)\n"
            "[Repo-Stewardship](Repo-Stewardship.md)\n"
            "[Agent-Routing](Agent-Routing.md)\n"
            "[Security-Boundaries](Security-Boundaries.md)\n\n"
            "## Out of scope\n\nSecrets and invent product frameworks.\n\n"
            "Maintained by smtp.eth.\n"
        ),
        "PUBLISH.md": (
            "# PUBLISH\n\n```yaml\nstatus: ACTIVE\ncreated: \"2026-09-13\"\n"
            "purpose: x\ncloses: \"#16\"\n```\n\n"
            "In-repo source under docs/wiki; remote agents-governance.wiki.git.\n\n"
            "| `Home.md` | Home |\n| `Overview.md` | Overview |\n"
            "| `Autonomy-Levels.md` | Autonomy-Levels |\n"
            "| `Repo-Stewardship.md` | Repo-Stewardship |\n"
            "| `Agent-Routing.md` | Agent-Routing |\n"
            "| `Security-Boundaries.md` | Security-Boundaries |\n\n"
            "Do **not** push `PUBLISH.md`.\n"
            "Link Check and Markdown Lint. No secrets. No MEMORY dumps.\n"
        ),
        "Repo-Stewardship.md": (
            "# Repo\n\n[← Home](Home.md)\n\n"
            "markdown-lint link-check stewardship-checks\n"
            "run_stewardship_checks.sh relative links badge\n"
            "test_stewardship_gates.py\n"
            "actionlint on existing workflow paths\n"
            "AGENTS-ECOSYSTEM approval boundary\n"
            "no invent product\n"
        ),
        "Autonomy-Levels.md": (
            "# A\n\n[Home](Home.md)\n\nL0 L1 L2 L3 autonomy .kill_switch\n"
        ),
        "Security-Boundaries.md": (
            "# S\n\n[Home](Home.md)\n\nkill switch secret credential SECURITY.md\n"
        ),
        "Agent-Routing.md": (
            "# R\n\n[Home](Home.md)\n\nsurface routing copilot geryon\n"
        ),
        "Overview.md": (
            "# O\n\n[Home](Home.md)\n\ngovernance public AGENTS-ECOSYSTEM scratchpad\n"
        ),
    }


def _seed_tree(tmp: Path, *, mutate=None, extra_pages: tuple[str, ...] = ()) -> Path:
    scripts = _seed_scripts(tmp)
    wiki = tmp / "docs" / "wiki"
    pages = _good_pages()
    for name in extra_pages:
        pages[name] = f"# {name}\n\nextra\n"
    if mutate:
        mutate(pages)
    for name, body in pages.items():
        _write(wiki / name, body)
    return scripts


def assert_fail(script_path: Path, cwd: Path, needle: str) -> None:
    proc = run(script_path, cwd)
    blob = proc.stdout + proc.stderr
    if proc.returncode == 0:
        raise AssertionError(f"expected failure containing {needle!r}; got pass:\n{blob}")
    if needle.lower() not in blob.lower():
        raise AssertionError(f"expected needle {needle!r} in:\n{blob}")


def assert_pass(script_path: Path, cwd: Path) -> None:
    proc = run(script_path, cwd)
    blob = proc.stdout + proc.stderr
    if proc.returncode != 0:
        raise AssertionError(f"expected pass; got {proc.returncode}:\n{blob}")


# --- helper unit tests ---

def test_helper_has_atx_h1_ok() -> None:
    assert WIKI.has_atx_h1("# Title\n\nbody\n") is True


def test_helper_has_atx_h1_missing() -> None:
    assert WIKI.has_atx_h1("## Only h2\n") is False


def test_helper_has_atx_h1_empty_hash() -> None:
    assert WIKI.has_atx_h1("#\n") is False


def test_helper_page_is_empty_true() -> None:
    assert WIKI.page_is_empty("   \n\t\n") is True


def test_helper_page_is_empty_false() -> None:
    assert WIKI.page_is_empty("# X\n") is False


def test_helper_out_of_scope_heading_ok() -> None:
    assert WIKI.has_out_of_scope_heading("# H\n\n## Out of scope\n\nx\n") is True


def test_helper_out_of_scope_heading_casefold() -> None:
    assert WIKI.has_out_of_scope_heading("## OUT OF SCOPE\n") is True


def test_helper_out_of_scope_heading_prose_only() -> None:
    assert WIKI.has_out_of_scope_heading("out of scope without heading\n") is False


def test_helper_protocol_relative_true() -> None:
    assert WIKI.is_protocol_relative("//evil.example/x") is True


def test_helper_protocol_relative_false_https() -> None:
    assert WIKI.is_protocol_relative("https://example.com") is False


def test_helper_protocol_relative_false_path() -> None:
    assert WIKI.is_protocol_relative("/absolute/path") is False


def test_helper_iter_markdown_link_targets() -> None:
    targets = WIKI.iter_markdown_link_targets("[a](Home.md) ![b](x.png)")
    assert targets == ["Home.md", "x.png"]


def test_helper_iter_markdown_link_angle() -> None:
    targets = WIKI.iter_markdown_link_targets("[a](<../badge-standard.md>)")
    assert targets == ["../badge-standard.md"]


def test_helper_publishable_pages_count() -> None:
    assert len(WIKI.PUBLISHABLE_PAGES) == 6


def test_helper_publishable_includes_home() -> None:
    assert "Home.md" in WIKI.PUBLISHABLE_PAGES


def test_helper_operator_only() -> None:
    assert WIKI.OPERATOR_ONLY == "PUBLISH.md"


def test_helper_topic_autonomy_has_l2() -> None:
    assert "L2" in WIKI.PAGE_TOPIC_HINTS["Autonomy-Levels.md"]


def test_helper_topic_autonomy_has_l3() -> None:
    assert "L3" in WIKI.PAGE_TOPIC_HINTS["Autonomy-Levels.md"]


def test_helper_topic_autonomy_has_kill_switch() -> None:
    assert "kill_switch" in WIKI.PAGE_TOPIC_HINTS["Autonomy-Levels.md"]


def test_helper_topic_security_has_credential() -> None:
    assert "credential" in WIKI.PAGE_TOPIC_HINTS["Security-Boundaries.md"]


def test_helper_topic_security_has_security_md() -> None:
    assert "SECURITY.md" in WIKI.PAGE_TOPIC_HINTS["Security-Boundaries.md"]


def test_helper_topic_routing_has_copilot() -> None:
    assert "copilot" in WIKI.PAGE_TOPIC_HINTS["Agent-Routing.md"]


def test_helper_topic_routing_has_geryon() -> None:
    assert "geryon" in WIKI.PAGE_TOPIC_HINTS["Agent-Routing.md"]


def test_helper_topic_overview_has_ecosystem() -> None:
    assert "AGENTS-ECOSYSTEM" in WIKI.PAGE_TOPIC_HINTS["Overview.md"]


def test_helper_topic_overview_has_scratchpad() -> None:
    assert "scratchpad" in WIKI.PAGE_TOPIC_HINTS["Overview.md"]


def test_helper_topic_stewardship_has_selftests() -> None:
    assert "test_stewardship_gates.py" in WIKI.PAGE_TOPIC_HINTS["Repo-Stewardship.md"]


def test_helper_ecosystem_link_hints_nonempty() -> None:
    assert WIKI.ECOSYSTEM_LINK_HINTS


def test_helper_ci_hints_three() -> None:
    assert set(WIKI.STEWARDSHIP_CI_HINTS) == {
        "markdown-lint",
        "link-check",
        "stewardship-checks",
    }


def test_helper_readme_link_hints() -> None:
    assert any("README.md" in h for h in WIKI.README_LINK_HINTS)


def test_helper_badge_standard_hints() -> None:
    assert any("badge-standard" in h for h in WIKI.BADGE_STANDARD_HINTS)


# --- live tree ---

def test_live_tree_passes() -> None:
    assert_pass(SCRIPTS / "check_wiki_outline.py", ROOT)


def test_live_publishable_pages_exist() -> None:
    for name in WIKI.PUBLISHABLE_PAGES:
        assert (WIKI.WIKI / name).is_file(), name


def test_live_publish_exists() -> None:
    assert (WIKI.WIKI / WIKI.OPERATOR_ONLY).is_file()


# --- fixture reject / accept ---

def test_wiki_passes_good_fixture() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path)
        assert_pass(scripts / "check_wiki_outline.py", tmp_path)


def test_wiki_rejects_unexpected_page() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, extra_pages=("Extra.md",))
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "Unexpected")


def test_wiki_rejects_missing_home() -> None:
    def mutate(pages):
        del pages["Home.md"]
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "Home.md")


def test_wiki_rejects_missing_publish() -> None:
    def mutate(pages):
        del pages["PUBLISH.md"]
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "PUBLISH")


def test_wiki_rejects_missing_wiki_dir() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_scripts(tmp_path)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "docs/wiki")


def test_wiki_rejects_missing_topic_l2_0() -> None:
    def mutate(pages):
        pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('L2', "TOPIC_GONE", 1)
        if 'L2'.lower() != 'L2':
            pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('L2'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'L2')


def test_wiki_rejects_missing_topic_l3_1() -> None:
    def mutate(pages):
        pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('L3', "TOPIC_GONE", 1)
        if 'L3'.lower() != 'L3':
            pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('L3'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'L3')


def test_wiki_rejects_missing_topic_kill_switch_2() -> None:
    def mutate(pages):
        pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('kill_switch', "TOPIC_GONE", 1)
        if 'kill_switch'.lower() != 'kill_switch':
            pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('kill_switch'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'kill_switch')


def test_wiki_rejects_missing_topic_l0_3() -> None:
    def mutate(pages):
        pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('L0', "TOPIC_GONE", 1)
        if 'L0'.lower() != 'L0':
            pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('L0'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'L0')


def test_wiki_rejects_missing_topic_l1_4() -> None:
    def mutate(pages):
        pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('L1', "TOPIC_GONE", 1)
        if 'L1'.lower() != 'L1':
            pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('L1'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'L1')


def test_wiki_rejects_missing_topic_autonomy_5() -> None:
    def mutate(pages):
        pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('autonomy', "TOPIC_GONE", 1)
        if 'autonomy'.lower() != 'autonomy':
            pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('autonomy'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'autonomy')


def test_wiki_rejects_missing_topic_credential_6() -> None:
    def mutate(pages):
        pages['Security-Boundaries.md'] = pages['Security-Boundaries.md'].replace('credential', "TOPIC_GONE", 1)
        if 'credential'.lower() != 'credential':
            pages['Security-Boundaries.md'] = pages['Security-Boundaries.md'].replace('credential'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'credential')


def test_wiki_rejects_missing_topic_security_md_7() -> None:
    def mutate(pages):
        pages['Security-Boundaries.md'] = pages['Security-Boundaries.md'].replace('SECURITY.md', "TOPIC_GONE", 1)
        if 'SECURITY.md'.lower() != 'SECURITY.md':
            pages['Security-Boundaries.md'] = pages['Security-Boundaries.md'].replace('SECURITY.md'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'SECURITY.md')


def test_wiki_rejects_missing_topic_kill_8() -> None:
    def mutate(pages):
        pages['Security-Boundaries.md'] = pages['Security-Boundaries.md'].replace('kill', "TOPIC_GONE", 1)
        if 'kill'.lower() != 'kill':
            pages['Security-Boundaries.md'] = pages['Security-Boundaries.md'].replace('kill'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'kill')


def test_wiki_rejects_missing_topic_secret_9() -> None:
    def mutate(pages):
        pages['Security-Boundaries.md'] = pages['Security-Boundaries.md'].replace('secret', "TOPIC_GONE", 1)
        if 'secret'.lower() != 'secret':
            pages['Security-Boundaries.md'] = pages['Security-Boundaries.md'].replace('secret'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'secret')


def test_wiki_rejects_missing_topic_copilot_10() -> None:
    def mutate(pages):
        pages['Agent-Routing.md'] = pages['Agent-Routing.md'].replace('copilot', "TOPIC_GONE", 1)
        if 'copilot'.lower() != 'copilot':
            pages['Agent-Routing.md'] = pages['Agent-Routing.md'].replace('copilot'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'copilot')


def test_wiki_rejects_missing_topic_geryon_11() -> None:
    def mutate(pages):
        pages['Agent-Routing.md'] = pages['Agent-Routing.md'].replace('geryon', "TOPIC_GONE", 1)
        if 'geryon'.lower() != 'geryon':
            pages['Agent-Routing.md'] = pages['Agent-Routing.md'].replace('geryon'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'geryon')


def test_wiki_rejects_missing_topic_surface_12() -> None:
    def mutate(pages):
        pages['Agent-Routing.md'] = pages['Agent-Routing.md'].replace('surface', "TOPIC_GONE", 1)
        if 'surface'.lower() != 'surface':
            pages['Agent-Routing.md'] = pages['Agent-Routing.md'].replace('surface'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'surface')


def test_wiki_rejects_missing_topic_routing_13() -> None:
    def mutate(pages):
        pages['Agent-Routing.md'] = pages['Agent-Routing.md'].replace('routing', "TOPIC_GONE", 1)
        if 'routing'.lower() != 'routing':
            pages['Agent-Routing.md'] = pages['Agent-Routing.md'].replace('routing'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'routing')


def test_wiki_rejects_missing_topic_agents_ecosystem_14() -> None:
    def mutate(pages):
        pages['Overview.md'] = pages['Overview.md'].replace('AGENTS-ECOSYSTEM', "TOPIC_GONE", 1)
        if 'AGENTS-ECOSYSTEM'.lower() != 'AGENTS-ECOSYSTEM':
            pages['Overview.md'] = pages['Overview.md'].replace('AGENTS-ECOSYSTEM'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'AGENTS-ECOSYSTEM')


def test_wiki_rejects_missing_topic_scratchpad_15() -> None:
    def mutate(pages):
        pages['Overview.md'] = pages['Overview.md'].replace('scratchpad', "TOPIC_GONE", 1)
        if 'scratchpad'.lower() != 'scratchpad':
            pages['Overview.md'] = pages['Overview.md'].replace('scratchpad'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'scratchpad')


def test_wiki_rejects_missing_topic_governance_16() -> None:
    def mutate(pages):
        pages['Overview.md'] = pages['Overview.md'].replace('governance', "TOPIC_GONE", 1)
        if 'governance'.lower() != 'governance':
            pages['Overview.md'] = pages['Overview.md'].replace('governance'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'governance')


def test_wiki_rejects_missing_topic_public_17() -> None:
    def mutate(pages):
        pages['Overview.md'] = pages['Overview.md'].replace('public', "TOPIC_GONE", 1)
        if 'public'.lower() != 'public':
            pages['Overview.md'] = pages['Overview.md'].replace('public'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'public')


def test_wiki_rejects_missing_topic_test_stewardship_gates_py_18() -> None:
    def mutate(pages):
        pages['Repo-Stewardship.md'] = pages['Repo-Stewardship.md'].replace('test_stewardship_gates.py', "TOPIC_GONE", 1)
        if 'test_stewardship_gates.py'.lower() != 'test_stewardship_gates.py':
            pages['Repo-Stewardship.md'] = pages['Repo-Stewardship.md'].replace('test_stewardship_gates.py'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'test_stewardship_gates.py')


def test_wiki_rejects_missing_topic_run_stewardship_checks_sh_19() -> None:
    def mutate(pages):
        pages['Repo-Stewardship.md'] = pages['Repo-Stewardship.md'].replace('run_stewardship_checks.sh', "TOPIC_GONE", 1)
        if 'run_stewardship_checks.sh'.lower() != 'run_stewardship_checks.sh':
            pages['Repo-Stewardship.md'] = pages['Repo-Stewardship.md'].replace('run_stewardship_checks.sh'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'run_stewardship_checks.sh')


def test_wiki_rejects_missing_topic_badge_20() -> None:
    def mutate(pages):
        pages['Repo-Stewardship.md'] = pages['Repo-Stewardship.md'].replace('badge', "TOPIC_GONE", 1)
        if 'badge'.lower() != 'badge':
            pages['Repo-Stewardship.md'] = pages['Repo-Stewardship.md'].replace('badge'.lower(), "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'badge')


def test_wiki_rejects_home_ecosystem() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("AGENTS-ECOSYSTEM", "GONE").replace("agents-governance/blob/main/AGENTS-ECOSYSTEM.md", "gone")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'AGENTS-ECOSYSTEM')


def test_wiki_rejects_home_readme() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("README.md", "GONE.md")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'README')


def test_wiki_rejects_home_badge_link() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("../badge-standard.md", "../gone.md")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'badge')


def test_wiki_rejects_home_invent() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("invent", "GONE")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'invent')


def test_wiki_rejects_home_secret() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("Secrets", "GONE").replace("secret", "GONE")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'secret')


def test_wiki_rejects_home_out_of_scope_prose() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("Out of scope", "Elsewhere").replace("out of scope", "elsewhere")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'out of scope')


def test_wiki_rejects_home_out_of_scope_heading() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("## Out of scope", "## Elsewhere")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Out of scope')


def test_wiki_rejects_home_smtp() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("smtp.eth", "nobody")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'smtp.eth')


def test_wiki_rejects_home_h1() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("# Home", "## Home")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'H1')


def test_wiki_rejects_home_empty() -> None:
    def mutate(pages):
        pages["Home.md"] = "   \n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'empty')


def test_wiki_rejects_home_to_overview() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("[Overview](Overview.md)", "[Overview](gone.md)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Overview')


def test_wiki_rejects_home_to_routing() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("[Agent-Routing](Agent-Routing.md)", "[Agent-Routing](gone.md)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Agent-Routing')


def test_wiki_rejects_home_to_security() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("[Security-Boundaries](Security-Boundaries.md)", "[Security-Boundaries](gone.md)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Security-Boundaries')


def test_wiki_rejects_home_to_autonomy() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("[Autonomy-Levels](Autonomy-Levels.md)", "[Autonomy-Levels](gone.md)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Autonomy-Levels')


def test_wiki_rejects_home_to_stewardship() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("[Repo-Stewardship](Repo-Stewardship.md)", "[Repo-Stewardship](gone.md)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Repo-Stewardship')


def test_wiki_rejects_publish_wiki_git() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace(".wiki.git", ".gone.git").replace("wiki.git", "gone.git")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'wiki.git')


def test_wiki_rejects_publish_docs_wiki() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace("docs/wiki", "docs/gone")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'docs/wiki')


def test_wiki_rejects_publish_memory() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace("MEMORY", "GONE").replace("memory", "gone")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'MEMORY')


def test_wiki_rejects_publish_do_not_push() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace("Do **not** push `PUBLISH.md`.", "Push freely.")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'PUBLISH.md')


def test_wiki_rejects_publish_link_check() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace("Link Check", "GONE").replace("link-check", "gone")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Link Check')


def test_wiki_rejects_publish_markdown_lint() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace("Markdown Lint", "GONE").replace("markdown", "gone")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Markdown')


def test_wiki_rejects_publish_secrets() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace("No secrets", "GONE").replace("secrets", "gone")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'secret')


def test_wiki_rejects_publish_h1() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace("# PUBLISH", "## PUBLISH")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'H1')


def test_wiki_rejects_publish_empty() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = " \n "
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'empty')


def test_wiki_rejects_publish_home_row() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace("`Home.md`", "`Gone.md`")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Home.md')


def test_wiki_rejects_publish_overview_row() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace("`Overview.md`", "`Gone.md`")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Overview.md')


def test_wiki_rejects_publish_security_row() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace("`Security-Boundaries.md`", "`Gone.md`")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Security-Boundaries.md')


def test_wiki_rejects_stewardship_actionlint() -> None:
    def mutate(pages):
        pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace("actionlint", "GONE")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'actionlint')


def test_wiki_rejects_stewardship_relative() -> None:
    def mutate(pages):
        pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace("relative", "GONE")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'relative')


def test_wiki_rejects_stewardship_invent() -> None:
    def mutate(pages):
        pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace("invent", "GONE")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'invent')


def test_wiki_rejects_stewardship_ecosystem() -> None:
    def mutate(pages):
        pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace("AGENTS-ECOSYSTEM", "GONE")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'AGENTS-ECOSYSTEM')


def test_wiki_rejects_stewardship_markdown_lint() -> None:
    def mutate(pages):
        pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace("markdown-lint", "GONE")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'markdown-lint')


def test_wiki_rejects_stewardship_link_check() -> None:
    def mutate(pages):
        pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace("link-check", "GONE")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'link-check')


def test_wiki_rejects_stewardship_stewardship_checks() -> None:
    def mutate(pages):
        pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace("stewardship-checks", "GONE")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'stewardship-checks')


def test_wiki_rejects_overview_home() -> None:
    def mutate(pages):
        pages["Overview.md"] = pages["Overview.md"].replace("(Home.md)", "(Gone.md)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Home.md')


def test_wiki_rejects_autonomy_home() -> None:
    def mutate(pages):
        pages["Autonomy-Levels.md"] = pages["Autonomy-Levels.md"].replace("(Home.md)", "(Gone.md)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Home.md')


def test_wiki_rejects_security_home() -> None:
    def mutate(pages):
        pages["Security-Boundaries.md"] = pages["Security-Boundaries.md"].replace("(Home.md)", "(Gone.md)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Home.md')


def test_wiki_rejects_routing_home() -> None:
    def mutate(pages):
        pages["Agent-Routing.md"] = pages["Agent-Routing.md"].replace("(Home.md)", "(Gone.md)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Home.md')


def test_wiki_rejects_stewardship_home() -> None:
    def mutate(pages):
        pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace("(Home.md)", "(Gone.md)")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Home.md')


def test_wiki_rejects_overview_h1() -> None:
    def mutate(pages):
        pages["Overview.md"] = pages["Overview.md"].replace("# O", "## O")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'H1')


def test_wiki_rejects_autonomy_h1() -> None:
    def mutate(pages):
        pages["Autonomy-Levels.md"] = pages["Autonomy-Levels.md"].replace("# A", "## A")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'H1')


def test_wiki_rejects_security_h1() -> None:
    def mutate(pages):
        pages["Security-Boundaries.md"] = pages["Security-Boundaries.md"].replace("# S", "## S")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'H1')


def test_wiki_rejects_routing_h1() -> None:
    def mutate(pages):
        pages["Agent-Routing.md"] = pages["Agent-Routing.md"].replace("# R", "## R")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'H1')


def test_wiki_rejects_stewardship_h1() -> None:
    def mutate(pages):
        pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"].replace("# Repo", "## Repo")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'H1')


def test_wiki_rejects_overview_empty() -> None:
    def mutate(pages):
        pages["Overview.md"] = "\n  \n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'empty')


def test_wiki_rejects_autonomy_empty() -> None:
    def mutate(pages):
        pages["Autonomy-Levels.md"] = "\t"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'empty')


def test_wiki_rejects_http_link() -> None:
    def mutate(pages):
        pages["Overview.md"] = pages["Overview.md"] + "\n[bad](http://example.com)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'http://')


def test_wiki_rejects_http_link_home() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"] + "\n[bad](http://example.com)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'http://')


def test_wiki_rejects_js_scheme() -> None:
    def mutate(pages):
        pages["Overview.md"] = pages["Overview.md"] + "\n[bad](javascript:alert(1))\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'javascript')


def test_wiki_rejects_data_scheme() -> None:
    def mutate(pages):
        pages["Security-Boundaries.md"] = pages["Security-Boundaries.md"] + "\n[bad](data:text/html,x)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'data:')


def test_wiki_rejects_vbscript_scheme() -> None:
    def mutate(pages):
        pages["Agent-Routing.md"] = pages["Agent-Routing.md"] + "\n[bad](vbscript:msg)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'vbscript')


def test_wiki_rejects_file_scheme() -> None:
    def mutate(pages):
        pages["Autonomy-Levels.md"] = pages["Autonomy-Levels.md"] + "\n[bad](file:///etc/passwd)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'file:')


def test_wiki_rejects_protocol_relative() -> None:
    def mutate(pages):
        pages["Overview.md"] = pages["Overview.md"] + "\n[bad](//evil.example/x)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'protocol-relative')


def test_wiki_rejects_protocol_relative_home() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"] + "\n[bad](//evil.example/x)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'protocol-relative')


def test_wiki_rejects_http_publish() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"] + "\n[bad](http://example.com)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'http://')


def test_wiki_rejects_protocol_publish() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"] + "\n[bad](//evil.example)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'protocol-relative')


def test_wiki_rejects_js_publish() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"] + "\n[bad](javascript:x)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'javascript')


def test_wiki_rejects_stars_badge() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"] + "\n![stars](https://img.shields.io/github/stars/x)\n badge stars\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'stars')


def test_wiki_rejects_forks_badge() -> None:
    def mutate(pages):
        pages["Overview.md"] = pages["Overview.md"] + "\nbadge forks chrome\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'forks')


def test_wiki_rejects_codecov_badge() -> None:
    def mutate(pages):
        pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"] + "\n[![c](https://codecov.io/badge)](x)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'codecov')


def test_wiki_rejects_downloads_badge() -> None:
    def mutate(pages):
        pages["Agent-Routing.md"] = pages["Agent-Routing.md"] + "\nbadge downloads\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'downloads')


def test_wiki_rejects_twitter_badge() -> None:
    def mutate(pages):
        pages["Security-Boundaries.md"] = pages["Security-Boundaries.md"] + "\nbadge twitter\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'twitter')


def test_wiki_rejects_discord_badge() -> None:
    def mutate(pages):
        pages["Autonomy-Levels.md"] = pages["Autonomy-Levels.md"] + "\nbadge discord\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'discord')


def test_wiki_rejects_producthunt_badge() -> None:
    def mutate(pages):
        pages["Overview.md"] = pages["Overview.md"] + "\nbadge producthunt\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'producthunt')


def test_wiki_rejects_npm_badge() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"] + "\n[![n](https://img.shields.io/npm/v/x)](x)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'npm')


def test_wiki_rejects_pypi_badge() -> None:
    def mutate(pages):
        pages["Repo-Stewardship.md"] = pages["Repo-Stewardship.md"] + "\nbadge pypi/\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'pypi')


def test_wiki_rejects_coveralls_badge() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"] + "\nbadge coveralls\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'coveralls')


def test_wiki_rejects_publish_codecov() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"] + "\nbadge codecov\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'codecov')


def test_wiki_rejects_publish_stars() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"] + "\nbadge stars\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'stars')


def test_wiki_rejects_secret_pattern() -> None:
    def mutate(pages):
        pages["Overview.md"] = pages["Overview.md"] + "\nghp_" + ("a" * 40) + "\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "secret")


def test_wiki_rejects_secret_in_publish() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"] + "\ngithub_pat_" + ("b" * 40) + "\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "secret")


def test_wiki_rejects_private_key() -> None:
    def mutate(pages):
        pages["Security-Boundaries.md"] = (
            pages["Security-Boundaries.md"]
            + "\n-----BEGIN RSA PRIVATE KEY-----\n"
        )
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "PRIVATE KEY")


def test_wiki_accepts_fenced_http_example() -> None:
    def mutate(pages):
        pages["Overview.md"] = (
            pages["Overview.md"]
            + "\n```\n[bad](http://example.com)\n```\n"
        )
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_pass(scripts / "check_wiki_outline.py", tmp_path)


def test_wiki_accepts_fenced_js_example() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = (
            pages["PUBLISH.md"]
            + "\n```bash\necho '[x](javascript:alert(1))'\n```\n"
        )
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_pass(scripts / "check_wiki_outline.py", tmp_path)


def test_wiki_accepts_https_link() -> None:
    def mutate(pages):
        pages["Overview.md"] = (
            pages["Overview.md"]
            + "\n[ok](https://github.com/fuzzywigg/agents-governance)\n"
        )
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_pass(scripts / "check_wiki_outline.py", tmp_path)


def test_wiki_accepts_mailto() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"] + "\n[mail](mailto:ops@example.com)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_pass(scripts / "check_wiki_outline.py", tmp_path)


def test_wiki_rejects_missing_overview() -> None:
    def mutate(pages):
        del pages['Overview.md']
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Overview.md')


def test_wiki_rejects_missing_autonomy_levels() -> None:
    def mutate(pages):
        del pages['Autonomy-Levels.md']
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Autonomy-Levels.md')


def test_wiki_rejects_missing_repo_stewardship() -> None:
    def mutate(pages):
        del pages['Repo-Stewardship.md']
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Repo-Stewardship.md')


def test_wiki_rejects_missing_agent_routing() -> None:
    def mutate(pages):
        del pages['Agent-Routing.md']
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Agent-Routing.md')


def test_wiki_rejects_missing_security_boundaries() -> None:
    def mutate(pages):
        del pages['Security-Boundaries.md']
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'Security-Boundaries.md')


def test_wiki_rejects_l2_still() -> None:
    def mutate(pages):
        pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('L2', "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'L2')


def test_wiki_rejects_l3_still() -> None:
    def mutate(pages):
        pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('L3', "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'L3')


def test_wiki_rejects_kill_switch_still() -> None:
    def mutate(pages):
        pages['Autonomy-Levels.md'] = pages['Autonomy-Levels.md'].replace('kill_switch', "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'kill_switch')


def test_wiki_rejects_credential_still() -> None:
    def mutate(pages):
        pages['Security-Boundaries.md'] = pages['Security-Boundaries.md'].replace('credential', "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'credential')


def test_wiki_rejects_security_md_still() -> None:
    def mutate(pages):
        pages['Security-Boundaries.md'] = pages['Security-Boundaries.md'].replace('SECURITY.md', "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'SECURITY.md')


def test_wiki_rejects_copilot_still() -> None:
    def mutate(pages):
        pages['Agent-Routing.md'] = pages['Agent-Routing.md'].replace('copilot', "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'copilot')


def test_wiki_rejects_geryon_still() -> None:
    def mutate(pages):
        pages['Agent-Routing.md'] = pages['Agent-Routing.md'].replace('geryon', "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'geryon')


def test_wiki_rejects_ecosystem_still() -> None:
    def mutate(pages):
        pages['Overview.md'] = pages['Overview.md'].replace('AGENTS-ECOSYSTEM', "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'AGENTS-ECOSYSTEM')


def test_wiki_rejects_scratchpad_still() -> None:
    def mutate(pages):
        pages['Overview.md'] = pages['Overview.md'].replace('scratchpad', "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'scratchpad')


def test_wiki_rejects_selftests_still() -> None:
    def mutate(pages):
        pages['Repo-Stewardship.md'] = pages['Repo-Stewardship.md'].replace('test_stewardship_gates.py', "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'test_stewardship_gates.py')


def test_wiki_rejects_stew_ecosystem_still() -> None:
    def mutate(pages):
        pages['Repo-Stewardship.md'] = pages['Repo-Stewardship.md'].replace('AGENTS-ECOSYSTEM', "TOPIC_GONE", 1)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, 'AGENTS-ECOSYSTEM')


def test_wiki_rejects_home_ecosystem_still() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("AGENTS-ECOSYSTEM", "GONE")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "AGENTS-ECOSYSTEM")


def test_wiki_rejects_home_smtp_still() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("smtp.eth", "nobody")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "smtp.eth")


def test_wiki_rejects_publish_wiki_git_still() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace(".wiki.git", ".x.git").replace("wiki.git", "x.git")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "wiki.git")


def test_wiki_rejects_publish_docs_wiki_still() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace("docs/wiki", "docs/x")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "docs/wiki")


def test_wiki_rejects_publish_memory_still() -> None:
    def mutate(pages):
        pages["PUBLISH.md"] = pages["PUBLISH.md"].replace("MEMORY", "GONE")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "MEMORY")


def test_wiki_rejects_protocol_relative_still() -> None:
    def mutate(pages):
        pages["Overview.md"] += "\n[bad](//evil.example)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "protocol-relative")


def test_wiki_rejects_http_still() -> None:
    def mutate(pages):
        pages["Home.md"] += "\n[bad](http://example.com)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "http://")


def test_wiki_rejects_h1_still() -> None:
    def mutate(pages):
        pages["Overview.md"] = pages["Overview.md"].replace("# O", "## O")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "H1")


def test_wiki_rejects_empty_still() -> None:
    def mutate(pages):
        pages["Agent-Routing.md"] = "  \n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "empty")


def test_wiki_rejects_out_of_scope_heading_still() -> None:
    def mutate(pages):
        pages["Home.md"] = pages["Home.md"].replace("## Out of scope", "## Other")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_fail(scripts / "check_wiki_outline.py", tmp_path, "Out of scope")


def test_wiki_accepts_good_fixture_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path)
        assert_pass(scripts / "check_wiki_outline.py", tmp_path)


def test_wiki_accepts_https_still() -> None:
    def mutate(pages):
        pages["Repo-Stewardship.md"] += "\n[x](https://example.com)\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_pass(scripts / "check_wiki_outline.py", tmp_path)


def test_wiki_accepts_fenced_still() -> None:
    def mutate(pages):
        pages["Overview.md"] += "\n```\n[bad](//evil)\n```\n"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path, mutate=mutate)
        assert_pass(scripts / "check_wiki_outline.py", tmp_path)


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in tests:
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {fn.__name__}: {exc}", file=sys.stderr)
    if failed:
        print(f"Wiki-outline self-tests FAILED: {failed}/{len(tests)}", file=sys.stderr)
        return 1
    # Also confirm live tree once more for the printed count contract.
    live = run(SCRIPTS / "check_wiki_outline.py", ROOT)
    if live.returncode != 0:
        print(live.stdout + live.stderr, file=sys.stderr)
        return 1
    print(f"OK: wiki-outline gate self-tests passed ({len(tests)} cases + live tree)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
