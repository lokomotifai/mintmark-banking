"""The pack's conformance suite.

Green here means: the declarations are valid under the strict loader, a mint
produces the shapes the brief describes, no invented name collides with a real
institution, and the recipes can actually satisfy the coverage they promise.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from mintmark.annotate import ALL_LABELS
from mintmark.lexicons import load as load_denylist
from mintmark.mint import asset_dir, mint
from mintmark.packs.model import load_pack

ROOT = Path(__file__).resolve().parents[1]
PACK = load_pack(ROOT)
CORE_DENYLIST = load_denylist(asset_dir("denylist") / "institutions-tr.txt")


# The pack contains no engine code, and its Python imports only the public API.


def test_no_python_outside_tests_and_tools() -> None:
    offenders = [
        str(p.relative_to(ROOT))
        for p in ROOT.rglob("*.py")
        if p.is_file() and not str(p.relative_to(ROOT)).startswith(("tests/", "tools/", ".venv/"))
    ]
    assert not offenders, f"a pack carries no engine code, but found: {offenders}"


def test_tests_import_only_the_public_api() -> None:
    """A pack that reaches into a private core module has coupled itself to it."""
    import ast

    for path in sorted((ROOT / "tests").glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("mintmark._"), (
                    f"{path.name} imports a private core module: {node.module}"
                )


def test_no_dataset_is_committed_outside_samples() -> None:
    offenders = [
        str(p.relative_to(ROOT))
        for p in ROOT.rglob("*.jsonl")
        if not str(p.relative_to(ROOT)).startswith(("samples/", "tests/", ".venv/", "dist/"))
    ]
    assert not offenders, f"datasets are release artifacts, never committed: {offenders}"


# Identity and pins.


def test_the_pack_name_matches_the_repository() -> None:
    assert PACK.name == ROOT.name == "mintmark-banking"


def test_the_core_pin_has_a_closed_upper_bound() -> None:
    """An open pin lets a future core change what a published manifest reproduces."""
    assert PACK.requires_core.text == ">=0.1,<0.2"
    assert PACK.requires_core.contains("0.1.0")
    assert not PACK.requires_core.contains("0.2.0")


def test_the_locale_is_turkish() -> None:
    assert PACK.locale == "tr-TR"


# Record shapes the brief settles.


def test_the_four_structured_record_types_exist() -> None:
    names = {t.type_name for t in PACK.record_types}
    assert {"customer", "account", "card", "transaction"} <= names


def test_the_three_document_types_exist_with_their_evaluation_twins() -> None:
    names = {t.type_name for t in PACK.record_types}
    for base in ("complaint_ticket", "kyc_note", "support_transcript"):
        assert base in names
        assert f"{base}_eval" in names, "the evaluation twin carries the elevated density"


def test_accounts_are_one_to_three_per_customer_at_the_declared_weights() -> None:
    ref = next(f.ref for f in PACK.record_type("account").fields if f.type == "ref")
    assert ref.parent == "customer"
    assert ref.counts == (1, 2, 3)
    assert ref.weights == ("0.55", "0.30", "0.15")


def test_cards_may_be_absent_from_an_account() -> None:
    """0..2 per account. A test requiring every account to have a card is wrong."""
    ref = next(f.ref for f in PACK.record_type("card").fields if f.type == "ref")
    assert ref.counts[0] == 0


def test_the_counterparty_iban_is_nullable_at_the_declared_rate() -> None:
    field = next(f for f in PACK.record_type("transaction").fields if f.name == "counterparty_iban")
    assert field.nullable
    assert field.null_rate == "0.35"


def test_every_label_used_is_in_the_closed_taxonomy() -> None:
    known = {label.value for label in ALL_LABELS} | {"none"}
    for record_type in PACK.record_types:
        for field in record_type.fields:
            assert field.pii_label in known, (
                f"{record_type.type_name}.{field.name} uses {field.pii_label!r}"
            )


# Lexicons.


def test_at_least_twenty_four_fictional_bank_names() -> None:
    banks = PACK.lexicons["banks_fictional"]["values"]
    assert len(banks) >= 24, f"the brief settles at least 24, found {len(banks)}"


@pytest.mark.parametrize("name", sorted(p.stem for p in (ROOT / "lexicons").glob("*.yaml")))
def test_every_lexicon_entry_passes_the_denylist(name: str) -> None:
    document = yaml.safe_load((ROOT / "lexicons" / f"{name}.yaml").read_text(encoding="utf-8"))
    hits = [
        hit.render()
        for value in document.get("values", [])
        for hit in CORE_DENYLIST.scan(str(value))
    ]
    assert not hits, "\n".join(hits)


@pytest.mark.parametrize("name", sorted(p.stem for p in (ROOT / "lexicons").glob("*.yaml")))
def test_every_lexicon_carries_a_source_note(name: str) -> None:
    document = yaml.safe_load((ROOT / "lexicons" / f"{name}.yaml").read_text(encoding="utf-8"))
    assert len(document.get("source_note", "")) > 40, f"{name} has no real source note"


def test_the_pack_denylist_covers_the_core_one() -> None:
    """Packs may extend the list and may never shrink it."""
    extension = load_denylist(ROOT / "lexicons" / "denylist_extension.txt")
    assert extension.covers(CORE_DENYLIST), (
        f"missing from the pack list: {sorted(extension.missing_from(CORE_DENYLIST))[:5]}"
    )


def test_no_template_names_a_real_institution() -> None:
    text = "\n".join(
        p.read_text(encoding="utf-8") for p in sorted((ROOT / "templates").rglob("*.yaml"))
    )
    hits = [hit.render() for hit in CORE_DENYLIST.scan(text)]
    assert not hits, "\n".join(hits)


# Recipes.


def test_the_three_named_recipes_exist() -> None:
    assert set(PACK.recipes) == {"retail-baseline", "pii-eval", "anomaly-mix"}


def test_every_recipe_ships_with_the_safe_policy() -> None:
    """Reference datasets are always minted safe."""
    for name, recipe in PACK.recipes.items():
        assert recipe.identifier_policy == "safe", f"{name} does not pin the safe policy"


def test_the_evaluation_recipe_declares_a_target_for_every_label() -> None:
    targets = PACK.recipe("pii-eval").coverage_targets
    assert set(targets) == {label.value for label in ALL_LABELS}
    for label in ("PERSON", "HEALTH", "UNION"):
        assert targets[label] >= 300
    for label in ("TCKN", "VKN", "IBAN", "PAN", "PHONE", "EMAIL"):
        assert targets[label] >= 500


def test_the_reference_seeds_are_the_settled_ones() -> None:
    """Changing a seed silently invalidates a published manifest."""
    datasets = json.loads((ROOT / "docs" / "reference-datasets.json").read_text(encoding="utf-8"))
    assert datasets["retail-baseline"]["seed"] == "20260901"
    assert datasets["pii-eval"]["seed"] == "20260902"
    for name, entry in datasets.items():
        if name.startswith("_"):
            continue
        assert entry["identifier_policy"] == "safe", f"{name} is not pinned to safe"


# The mint itself.


@pytest.fixture(scope="module")
def minted(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("pack") / "run"
    mint(
        pack=ROOT,
        recipe="retail-baseline",
        seed=1,
        out=out,
        records={
            "customer": 120,
            "account": 200,
            "card": 90,
            "transaction": 600,
            "complaint_ticket": 40,
            "kyc_note": 30,
            "support_transcript": 30,
        },
        invocation="pytest",
    )
    return out


def test_a_mint_produces_every_declared_type(minted: Path) -> None:
    for record_type in PACK.record_types:
        assert (minted / f"{record_type.type_name}.jsonl").exists()


def test_documents_produce_sidecars(minted: Path) -> None:
    for name in ("complaint_ticket", "kyc_note", "support_transcript"):
        sidecar = minted / f"{name}.labels.jsonl"
        assert sidecar.exists()
        assert sidecar.read_text(encoding="utf-8").strip()


def test_a_minted_dataset_verifies(minted: Path) -> None:
    from mintmark.api import verify

    report = verify(minted)
    assert report.ok, report.problems
    assert report.checksum_valid_identifiers == 0


def test_no_real_institution_appears_in_minted_output(minted: Path) -> None:
    text = "\n".join(p.read_text(encoding="utf-8") for p in sorted(minted.glob("*.jsonl")))
    hits = [hit.render() for hit in CORE_DENYLIST.scan(text)]
    assert not hits, "\n".join(hits)


def test_every_reference_resolves(minted: Path) -> None:
    def ids(name: str, field: str) -> set[str]:
        return {
            json.loads(line)[field]
            for line in (minted / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }

    customers = ids("customer", "customer_id")
    accounts = ids("account", "account_id")
    for line in (minted / "account.jsonl").read_text(encoding="utf-8").splitlines():
        assert json.loads(line)["customer_id"] in customers
    for name in ("card", "transaction"):
        for line in (minted / f"{name}.jsonl").read_text(encoding="utf-8").splitlines():
            assert json.loads(line)["account_id"] in accounts


def test_pans_are_emitted_masked(minted: Path) -> None:
    for line in (minted / "card.jsonl").read_text(encoding="utf-8").splitlines():
        assert "*" in json.loads(line)["pan_masked"]


def test_the_anomaly_flag_never_disagrees_with_the_kind(tmp_path: Path) -> None:
    out = tmp_path / "anomaly"
    mint(
        pack=ROOT,
        recipe="anomaly-mix",
        seed=1,
        out=out,
        records={
            "customer": 60,
            "account": 100,
            "card": 40,
            "transaction": 2000,
            "complaint_ticket": 10,
            "kyc_note": 10,
            "support_transcript": 10,
        },
        invocation="pytest",
    )
    rows = [
        json.loads(line)
        for line in (out / "transaction.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert rows
    for row in rows:
        assert row["is_anomaly"] == (row["anomaly_kind"] != "none")
    kinds = {row["anomaly_kind"] for row in rows}
    assert kinds == {"none", "burst", "velocity", "round_amount_series", "dormant_reactivation"}


def test_packcheck_passes_against_the_pinned_core() -> None:
    """The conformance run a pack release may not be tagged without."""
    result = subprocess.run(
        [sys.executable, "-m", "mintmark.cli", "packcheck", str(ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


# Sample freshness.

SAMPLE_COUNTS = dict.fromkeys(
    [
        "customer",
        "account",
        "card",
        "transaction",
        "complaint_ticket",
        "kyc_note",
        "support_transcript",
    ],
    50,
)


def test_samples_regenerate_to_the_same_bytes(tmp_path: Path) -> None:
    """A sample that drifted from the declarations misrepresents them silently."""
    out = tmp_path / "regenerated"
    mint(
        pack=ROOT,
        recipe="retail-baseline",
        seed=1,
        out=out,
        records=SAMPLE_COUNTS,
        invocation="pytest",
    )
    drifted = []
    for committed in sorted((ROOT / "samples").glob("*.jsonl")):
        fresh = out / committed.name
        assert fresh.exists(), f"{committed.name} is committed but no longer produced"
        if committed.read_bytes() != fresh.read_bytes():
            drifted.append(committed.name)
    assert not drifted, (
        f"samples drifted: {drifted}. Regenerate with the command in samples/README.md."
    )


def test_samples_are_capped_at_fifty_records_per_type() -> None:
    """The contract's bound. A pack is declarations, not a dataset."""
    for path in sorted((ROOT / "samples").glob("*.jsonl")):
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert len(lines) <= 50, f"{path.name} carries {len(lines)} records"
        assert lines, f"{path.name} is empty and should not be committed"


def test_samples_carry_no_manifest() -> None:
    """Samples are illustrative. A manifest would make them look like a dataset."""
    assert not (ROOT / "samples" / "MINTMARK.json").exists()
    assert not (ROOT / "samples" / "SHA256SUMS").exists()


# The README's claims about its own contents.


README_EN = ROOT / "README.md"
README_TR = ROOT / "README.tr.md"


def test_the_readme_example_is_real_output_not_an_illustration() -> None:
    """A README that invents its example will invent a stale one eventually."""
    quoted = README_EN.read_text(encoding="utf-8")
    first = json.loads(
        (ROOT / "samples" / "complaint_ticket.jsonl").read_text(encoding="utf-8").splitlines()[0]
    )["body"]
    # The README wraps the excerpt, so compare on the distinctive values rather
    # than on the wrapped text.
    for token in first.split()[:6]:
        assert token in quoted, f"the README example does not match the sample: {token!r} missing"


def test_the_readme_states_the_counts_it_claims() -> None:
    banks = len(PACK.lexicons["banks_fictional"]["values"])
    text = README_EN.read_text(encoding="utf-8")
    assert f"{banks} invented bank names" in text or f"fictional%20banks-{banks}" in text, (
        f"the README's bank count has drifted from the {banks} actually declared"
    )
    assert f"record%20types-{len(PACK.record_types) - 3}" in text or "record types" in text


def test_both_readmes_exist_and_mirror_each_other() -> None:
    import re

    heading = re.compile(r"^(#{1,6})\s", re.MULTILINE)
    levels_en = [len(m.group(1)) for m in heading.finditer(README_EN.read_text(encoding="utf-8"))]
    levels_tr = [len(m.group(1)) for m in heading.finditer(README_TR.read_text(encoding="utf-8"))]
    assert levels_en == levels_tr, "the Turkish mirror has diverged in structure"


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_each_readme_declares_the_anomaly_limitation(path: Path) -> None:
    """The anomaly kinds are per-row labels, not temporal structures.

    Saying so is the difference between a fixture someone can trust and one that
    quietly overstates what it contains.
    """
    text = path.read_text(encoding="utf-8").lower()
    assert "per-row" in text or "satir bazli" in text or "satır bazlı" in text
    assert "evasion" in text or "atlatma" in text or "kacinma" in text or "kaçınma" in text


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_each_readme_names_the_release_that_actually_exists(path: Path) -> None:
    """A README may claim a release, and the claim has to be the right one.

    This replaced a test that asserted nothing was published, which was correct
    until something was. The failure it now guards is subtler and likelier: a
    version bump that leaves the README pointing at a tag nobody cut, or at an
    older one whose datasets no longer reproduce from these declarations.
    """
    text = path.read_text(encoding="utf-8")
    tag = f"v{PACK.version}"
    assert f"/releases/tag/{tag}" in text, (
        f"{path.name} does not point at {tag}, the version this pack declares"
    )
    stale = re.findall(r"/releases/tag/v(\d+\.\d+\.\d+)", text)
    assert set(stale) == {PACK.version}, (
        f"{path.name} names releases {sorted(set(stale))} while the pack is {PACK.version}"
    )


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_neither_readme_claims_the_engine_is_on_a_package_index(path: Path) -> None:
    """It is not, and the name there is unclaimed.

    Telling a reader to install by package name would install whatever somebody
    else eventually puts under that name.
    """
    text = path.read_text(encoding="utf-8").lower()
    assert "pypi.org/project" not in text
    assert "uv tool install mintmark\n" not in text
    assert "pip install mintmark" not in text


@pytest.mark.parametrize("path", [README_EN, README_TR], ids=["en", "tr"])
def test_each_readme_references_only_committed_assets(path: Path) -> None:
    import re

    for match in re.finditer(r"\((assets/[^)]+)\)", path.read_text(encoding="utf-8")):
        assert (ROOT / match.group(1)).exists(), f"{match.group(1)} is referenced but absent"


# What a version bump costs.


def test_the_pack_version_is_part_of_what_seeds_the_streams(tmp_path: Path) -> None:
    """Bumping the version changes every emitted byte for a fixed seed.

    The version is part of the pack digest and the digest seeds the streams, so
    version and content correspond exactly: two datasets carrying the same pack
    version cannot differ, and a bump is never a no-op for anyone holding a
    published manifest. Worth a test because it is surprising, and because the
    sample freshness failure it causes reads like a bug until you know why.
    """
    import shutil

    rolled_back = tmp_path / "rolled-back"
    shutil.copytree(
        ROOT,
        rolled_back,
        ignore=shutil.ignore_patterns(".venv", ".git", ".pytest_cache", "samples", "dist"),
    )
    manifest = rolled_back / "pack.yaml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            f"version: {PACK.version}", "version: 9.9.9"
        ),
        encoding="utf-8",
    )

    out = tmp_path / "probe"
    mint(
        pack=rolled_back,
        recipe="retail-baseline",
        seed=1,
        out=out,
        records={"customer": 20},
        invocation="pytest",
    )
    changed = (out / "customer.jsonl").read_bytes()
    committed = (ROOT / "samples" / "customer.jsonl").read_bytes()
    assert not committed.startswith(changed[:200]), (
        "a different pack version produced identical bytes, so the version is no "
        "longer part of the digest and two datasets can now share a version while "
        "differing in content"
    )
