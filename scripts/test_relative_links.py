#!/usr/bin/env python3
"""TOKENMAXX relative-link gate self-tests (dedicated slice — not mega-fixtures).

Deepens check_relative_links.py only: empty mailto:/tel: payloads, backslash
path separators, ASCII control chars, whitespace-only fragments, plus
github_slug / fragment_resolves / should_skip helpers and classic
scheme/escape/fragment edges. No invent-product surface.
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


def _load_rel_module():
    path = SCRIPTS / "check_relative_links.py"
    spec = importlib.util.spec_from_file_location("check_relative_links", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


REL = _load_rel_module()


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
    for name in ("stewardship_common.py", "check_relative_links.py"):
        shutil.copy2(SCRIPTS / name, scripts_dir / name)
    return scripts_dir


def _seed_tree(
    tmp: Path,
    readme: str = "# T\n\nSee [ok](ok.md).\n",
    extra: dict[str, str] | None = None,
) -> Path:
    scripts = _seed_scripts(tmp)
    _write(tmp / "README.md", readme)
    _write(tmp / "ok.md", "# Ok\n\n## Hello World\n\n## A & B\n\n## Code `x`\n")
    if extra:
        for rel, body in extra.items():
            _write(tmp / rel, body)
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

def test_helper_has_control_chars_tab() -> None:
    assert REL.has_control_chars("a\tb") is True


def test_helper_has_control_chars_nul() -> None:
    assert REL.has_control_chars("a\x00b") is True


def test_helper_has_control_chars_cr() -> None:
    assert REL.has_control_chars("a\rb") is True


def test_helper_has_control_chars_lf() -> None:
    assert REL.has_control_chars("a\nb") is True


def test_helper_has_control_chars_clean() -> None:
    assert REL.has_control_chars("ab-ok_path.md") is False


def test_helper_empty_mailto() -> None:
    assert REL.empty_scheme_payload("mailto:") == "mailto"


def test_helper_empty_mailto_space() -> None:
    assert REL.empty_scheme_payload("mailto:   ") == "mailto"


def test_helper_empty_tel() -> None:
    assert REL.empty_scheme_payload("tel:") == "tel"


def test_helper_empty_tel_space() -> None:
    assert REL.empty_scheme_payload("TEL: ") == "tel"


def test_helper_mailto_ok() -> None:
    assert REL.empty_scheme_payload("mailto:ops@example.com") is None


def test_helper_tel_ok() -> None:
    assert REL.empty_scheme_payload("tel:+15551212") is None


def test_helper_https_not_empty_scheme() -> None:
    assert REL.empty_scheme_payload("https://example.com") is None


def test_helper_fragment_resolves_exact() -> None:
    assert REL.fragment_resolves("hello-world", {"hello-world"}) is True


def test_helper_fragment_resolves_via_slug() -> None:
    assert REL.fragment_resolves("Hello World", {"hello-world"}) is True


def test_helper_fragment_rejects_whitespace() -> None:
    assert REL.fragment_resolves("   ", {"hello"}) is False


def test_helper_fragment_rejects_empty() -> None:
    assert REL.fragment_resolves("", {"hello"}) is False


def test_helper_fragment_rejects_missing() -> None:
    assert REL.fragment_resolves("nope", {"hello"}) is False


def test_helper_github_slug_basic() -> None:
    assert REL.github_slug("Hello World") == "hello-world"


def test_helper_github_slug_ampersand() -> None:
    assert REL.github_slug("A & B") == "a--b"


def test_helper_github_slug_backticks() -> None:
    assert REL.github_slug("Code `x`") == "code-x"


def test_helper_github_slug_link_heading() -> None:
    assert REL.github_slug("[Click](https://x)") == "click"


def test_helper_github_slug_punctuation() -> None:
    assert REL.github_slug("Hello: World!") == "hello-world"


def test_helper_skip_files_owasp() -> None:
    assert "OWASP-AGENTIC.md" in REL.SKIP_FILES


def test_helper_skip_parts_git() -> None:
    assert ".git" in REL.SKIP_PARTS


def test_helper_skip_parts_node_modules() -> None:
    assert "node_modules" in REL.SKIP_PARTS


def test_helper_skip_prefixes_agents() -> None:
    assert any("agents" in p for p in REL.SKIP_PREFIXES)


def test_helper_safe_external_schemes() -> None:
    for s in ("https://", "mailto:", "tel:"):
        assert s in REL.SAFE_EXTERNAL_SCHEMES


def test_helper_md_link_re_captures() -> None:
    m = REL.MD_LINK_RE.search("[x](ok.md)")
    assert m and m.group(2) == "ok.md"


def test_helper_md_link_re_image() -> None:
    m = REL.MD_LINK_RE.search("![alt](img.png)")
    assert m and m.group(2) == "img.png"


def test_live_relative_links_pass() -> None:
    assert_pass(SCRIPTS / "check_relative_links.py", ROOT)


def test_fixture_good_passes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(tmp_path)
        assert_pass(scripts / "check_relative_links.py", tmp_path)


def test_rel_rejects_empty_mailto() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](mailto:)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty mailto',
        )

def test_rel_rejects_empty_mailto_space() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](mailto: )\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty mailto',
        )

def test_rel_rejects_empty_tel() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](tel:)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty tel',
        )

def test_rel_rejects_empty_tel_space() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](TEL:  )\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty tel',
        )

def test_rel_rejects_empty_mailto_angle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](<mailto:>)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty mailto',
        )

def test_rel_rejects_empty_tel_angle() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](<tel:>)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty tel',
        )

def test_rel_rejects_empty_mailto_mixed() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](MailTo:)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty mailto',
        )

def test_rel_rejects_empty_tel_mixed() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](TeL:)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty tel',
        )

def test_rel_rejects_backslash_parent() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](..\\..\\etc\\passwd)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'backslash',
        )

def test_rel_rejects_backslash_same() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](.\\ok.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'backslash',
        )

def test_rel_rejects_backslash_mixed() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](docs\\ok.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'backslash',
        )

def test_rel_rejects_encoded_backslash() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](ok%5cmd)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'backslash',
        )

def test_rel_rejects_tab_in_target() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](ok%09.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'control',
        )

def test_rel_rejects_cr_in_target() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](ok%0d.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'control',
        )

def test_rel_rejects_lf_in_target() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](ok%0a.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'control',
        )

def test_rel_rejects_nul_encoded() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](ok%00.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'NUL',
        )

def test_rel_rejects_whitespace_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## Hello\n\n[x](#%20%20)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'whitespace-only fragment',
        )

def test_rel_rejects_tab_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## Hello\n\n[x](#%09)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'control',
        )

def test_rel_rejects_cross_whitespace_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](ok.md#%20%20)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'whitespace-only fragment',
        )

def test_rel_rejects_javascript_alert1() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](javascript:alert(1))\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'javascript',
        )

def test_rel_rejects_javascript_alert1_v2() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](JAVASCRIPT:alert(1))\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'javascript',
        )

def test_rel_rejects_javascript_alert1_v3() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](Javascript:alert(1))\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'javascript',
        )

def test_rel_rejects_data_text_html_x() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](data:text/html,x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'data',
        )

def test_rel_rejects_data_text_html_x_v2() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](DATA:text/html,x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'data',
        )

def test_rel_rejects_data_text_html_x_v3() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](Data:text/html,x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'data',
        )

def test_rel_rejects_vbscript_msg() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](vbscript:msg)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'vbscript',
        )

def test_rel_rejects_vbscript_msg_v2() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](VBSCRIPT:msg)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'vbscript',
        )

def test_rel_rejects_vbscript_msg_v3() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](VbScript:msg)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'vbscript',
        )

def test_rel_rejects_file____etc_passwd() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](file:///etc/passwd)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'file',
        )

def test_rel_rejects_file____etc_passwd_v2() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](FILE:///etc/passwd)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'file',
        )

def test_rel_rejects_file____etc_passwd_v3() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](File:///etc/passwd)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'file',
        )

def test_rel_rejects_http___example_com() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](http://example.com)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'http://',
        )

def test_rel_rejects_http___example_com_v2() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](HTTP://example.com)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'http://',
        )

def test_rel_rejects_http___example_com_v3() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](HtTp://example.com)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'http://',
        )

def test_rel_rejects___evil_example_x() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](//evil.example/x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'protocol-relative',
        )

def test_rel_rejects_empty_parens() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x]()\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty',
        )

def test_rel_rejects_bare_hash() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](#)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty',
        )

def test_rel_rejects_whitespace_only_target() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](   )\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty',
        )

def test_rel_rejects_missing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](missing.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'broken',
        )

def test_rel_rejects_escape() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](../../etc/passwd)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'escapes',
        )

def test_rel_rejects_encoded_escape() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](%2e%2e/%2e%2e/etc/passwd)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'escapes',
        )

def test_rel_rejects_nested_escape() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](docs/../../../../etc/passwd)\n',
            extra={'docs/x.md': '# X\n'},
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'escapes',
        )

def test_rel_rejects_percent_nested() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](docs/%2e%2e/%2e%2e/etc/passwd)\n',
            extra={'docs/x.md': '# X\n'},
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'escapes',
        )

def test_rel_rejects_broken_image() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n![x](nope.png)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'broken',
        )

def test_rel_rejects_missing_nested() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](docs/nope.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'broken',
        )

def test_rel_rejects_missing_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## Hello\n\n[x](#missing)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'missing heading',
        )

def test_rel_rejects_cross_missing_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](ok.md#missing)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'missing heading',
        )

def test_rel_rejects_broken_sibling() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](./gone.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'broken',
        )

def test_rel_rejects_broken_parent_docs() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# Root\n\n[ok](ok.md)\n',
            extra={'docs/page.md': '# Docs\n\n[x](../gone.md)\n'},
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'broken',
        )

def test_rel_rejects_queryish_missing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](ok.md?x=1)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'broken',
        )

def test_rel_accepts_mailto() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](mailto:ops@example.com)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_mailto_upper() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](MAILTO:ops@example.com)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_mailto_mixed() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](MailTo:ops@example.com)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_tel() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](tel:+15551212)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_tel_upper() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](TEL:+15551212)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_https() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](https://example.com)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_https_upper() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](HTTPS://example.com)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_https_mixed() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](HtTpS://example.com)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## Hello World\n\n[x](#hello-world)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_ampersand_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## A & B\n\n[x](#a--b)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_cross_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](ok.md#hello-world)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_title_attr() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](ok.md "title")\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_angle_https() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](<https://example.com>)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_angle_relative() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](<ok.md>)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_angle_mailto() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](<mailto:a@example.com>)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_angle_tel() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](<tel:+15551212>)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_nested_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](docs/page.md)\n',
            extra={'docs/page.md': '# P\n'},
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_image() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n![x](img.png)\n',
            extra={'img.png': 'x'},
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_license() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](LICENSE)\n',
            extra={'LICENSE': 'MIT\n'},
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_same_dir() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](./ok.md)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_parent_existing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# Root\n\n[ok](ok.md)\n',
            extra={'docs/page.md': '# D\n\n[up](../ok.md)\n'},
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_fenced_broken() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n```\n[x](missing.md)\n```\n\n[ok](ok.md)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_tilde_fenced() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n~~~\n[x](missing.md)\n~~~\n\n[ok](ok.md)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_mailto_and_https() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[m](mailto:a@b.com)\n[w](https://example.com)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_tel_with_title() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[c](tel:+15551212 "phone")\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_numbered_heading() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## Section 1\n\n[x](#section-1)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_underscore_heading() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## hello_world\n\n[x](#hello_world)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_colon_heading() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## Hello: World\n\n[x](#hello-world)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_tilde_heading() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## Hello~World\n\n[x](#helloworld)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_asterisk_heading() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## Hello*World\n\n[x](#helloworld)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_hash_heading() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## Hello#World\n\n[x](#helloworld)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_image_title() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n![x](img.png "t")\n',
            extra={'img.png': 'x'},
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_nested_image() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n![x](docs/a.png)\n',
            extra={'docs/a.png': 'x'},
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_docs_nested_fragment() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# Root\n\n[ok](ok.md)\n',
            extra={'docs/page.md': '# P\n\n## Topic\n\n[x](#topic)\n'},
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_skips_owasp() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[ok](ok.md)\n',
            extra={'OWASP-AGENTIC.md': '# O\n\n[x](missing.md)\n'},
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_skips_github_agents() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[ok](ok.md)\n',
            extra={'.github/agents/x.md': '# A\n\n[x](missing.md)\n'},
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_skips_node_modules() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[ok](ok.md)\n',
            extra={'node_modules/pkg/README.md': '# N\n\n[x](missing.md)\n'},
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_rejects_empty_mailto_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](mailto:)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty mailto',
        )

def test_rel_rejects_empty_tel_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](tel:)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty tel',
        )

def test_rel_rejects_backslash_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](a\\b.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'backslash',
        )

def test_rel_rejects_control_tab_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](a%09b.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'control',
        )

def test_rel_rejects_ws_frag_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## H\n\n[x](#%20)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'whitespace-only',
        )

def test_rel_rejects_js_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](javascript:1)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'javascript',
        )

def test_rel_rejects_data_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](data:x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'data',
        )

def test_rel_rejects_http_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](http://x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'http://',
        )

def test_rel_rejects_proto_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](//x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'protocol-relative',
        )

def test_rel_rejects_empty_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x]()\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty',
        )

def test_rel_rejects_escape_bs_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](..\\x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'backslash',
        )

def test_rel_rejects_missing_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](no.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'broken',
        )

def test_rel_rejects_frag_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## H\n\n[x](#nope)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'missing heading',
        )

def test_rel_rejects_file_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](file:///x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'file',
        )

def test_rel_rejects_vbs_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](vbscript:x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'vbscript',
        )

def test_rel_rejects_nul_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](x%00.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'NUL',
        )

def test_rel_rejects_cr_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](x%0d.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'control',
        )

def test_rel_rejects_lf_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](x%0a.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'control',
        )

def test_rel_rejects_empty_mailto_angle_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](<mailto:>)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty mailto',
        )

def test_rel_rejects_empty_tel_angle_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](<tel:>)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty tel',
        )

def test_rel_rejects_encoded_bs_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](x%5cy.md)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'backslash',
        )

def test_rel_rejects_cross_ws_frag_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](ok.md#%20)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'whitespace-only',
        )

def test_rel_rejects_js_titlecase_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](Javascript:1)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'javascript',
        )

def test_rel_rejects_data_titlecase_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](Data:x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'data',
        )

def test_rel_rejects_http_upper_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](HTTP://x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'http://',
        )

def test_rel_rejects_file_upper_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](FILE:///x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'file',
        )

def test_rel_rejects_vbs_upper_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](VBSCRIPT:x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'vbscript',
        )

def test_rel_rejects_pct_escape_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](%2e%2e/x)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'escapes',
        )

def test_rel_rejects_bare_hash_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](#)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty',
        )

def test_rel_rejects_image_missing_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n![x](no.png)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'broken',
        )

def test_rel_rejects_empty_mailto_mixed_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](MailTo:)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty mailto',
        )

def test_rel_rejects_empty_tel_mixed_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](TeL:)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'empty tel',
        )

def test_rel_rejects_tab_frag_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## H\n\n[x](#%09)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'control',
        )

def test_rel_rejects_cr_frag_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## H\n\n[x](#%0d)\n',
            extra=None,
        )
        assert_fail(
            scripts / "check_relative_links.py",
            tmp_path,
            'control',
        )

def test_rel_accepts_mailto_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](mailto:a@b.com)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_tel_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](tel:+1)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_https_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](https://ex.com)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_ok_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](ok.md)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_frag_ok_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## Hello World\n\n[x](#hello-world)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_angle_https_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](<https://ex.com>)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_angle_ok_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](<ok.md>)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_cross_frag_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n[x](ok.md#hello-world)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_fenced_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n```\n[bad](no.md)\n```\n\n[ok](ok.md)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

def test_rel_accepts_amp_frag_still() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        scripts = _seed_tree(
            tmp_path,
            readme='# T\n\n## A & B\n\n[x](#a--b)\n',
            extra=None,
        )
        assert_pass(scripts / "check_relative_links.py", tmp_path)

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
        print(f"Relative-link self-tests FAILED: {failed}/{len(tests)}", file=sys.stderr)
        return 1
    print(f"OK: relative-link gate self-tests passed ({len(tests)} cases + live tree)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
