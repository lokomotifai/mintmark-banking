<p align="center">
  <img src="assets/brand/mintmark-logo.svg" width="112" height="112" alt="Mintmark">
</p>

<h1 align="center">Mintmark banking</h1>

<p align="center"><strong>Turkish retail banking data your test environment can hold without a KVKK conversation.</strong></p>

<p align="center">
  Customers, accounts, cards, transactions, and the free-text surfaces where<br>
  personal data actually hides: complaints, KYC notes, and support transcripts.
</p>

<p align="center">
  <a href="https://github.com/lokomotifai/mintmark-banking/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/lokomotifai/mintmark-banking/ci.yml?branch=main&amp;style=flat-square&amp;label=CI"></a>
  <img alt="Zero engine code" src="https://img.shields.io/badge/engine%20code-none-3C873A?style=flat-square">
  <a href="https://github.com/lokomotifai/mintmark-banking/releases/tag/v0.1.2"><img alt="Release v0.1.2" src="https://img.shields.io/badge/release-v0.1.2-3C873A?style=flat-square"></a>
  <a href="LICENSE"><img alt="Apache-2.0 license" src="https://img.shields.io/badge/license-Apache--2.0-3B3F46?style=flat-square"></a>
</p>

<p align="center">
  <a href="https://github.com/lokomotifai/mintmark"><img alt="Requires the Mintmark core" src="https://img.shields.io/badge/core-%3E%3D0.1%2C%3C0.2-17191F?style=flat-square"></a>
  <img alt="Seven record types" src="https://img.shields.io/badge/record%20types-7-17191F?style=flat-square">
  <img alt="Three recipes" src="https://img.shields.io/badge/recipes-3-17191F?style=flat-square">
  <img alt="26 fictional bank names" src="https://img.shields.io/badge/fictional%20banks-26-D11F26?style=flat-square">
  <img alt="Identifier policy safe" src="https://img.shields.io/badge/identifiers-checksum--invalid-D11F26?style=flat-square">
  <a href="README.tr.md"><img alt="Türkçe" src="https://img.shields.io/badge/belgeler-Türkçe-D11F26?style=flat-square"></a>
</p>

<p align="center">
  <a href="#mint-it-yourself"><strong>Mint it yourself</strong></a>
  ·
  <a href="#the-evaluation-set"><strong>The evaluation set</strong></a>
  ·
  <a href="#what-is-in-here-and-what-is-not"><strong>What is in here</strong></a>
  ·
  <a href="README.tr.md"><strong>Türkçe</strong></a>
</p>

---

> **This repository contains no engine code.** It is declarations and data:
> record shapes, lexicons, templates, and recipes. The engine that reads them
> lives in [mintmark](https://github.com/lokomotifai/mintmark) and is pinned here
> by a version range with a closed upper bound.

Turkish banks and fintechs cannot move production data into test, evaluation, or
AI pilot environments without KVKK exposure, and their vendors cannot reasonably
ask them to. This pack declares the data those environments need, and the engine
mints it: deterministic, span-labeled, and sealed by a manifest anyone can check.

**Version 0.1.2. Two reference datasets are published as assets on
[v0.1.2](https://github.com/lokomotifai/mintmark-banking/releases/tag/v0.1.2), each
carrying its own manifest and checksums.** What is true today: `packcheck` passes against
the pinned core, the test suite passes, and the evaluation recipe meets every one of its
eighteen coverage targets.

> [!IMPORTANT]
> **What this pack is not.** It is not anonymization of your banking data; it
> ingests none. It is not a compliance guarantee and not a legal safe harbor. The
> anomaly recipe is detector-side test data and this repository documents no
> evasion guidance of any kind. Generated phone numbers can coincide with
> assigned ones, because the Turkish numbering plan reserves no fictional range.
> This data is for testing systems. It is never for contacting anyone.
> What this
> does and does not mean under Turkish data protection law is set out in
> [docs/kvkk.md](docs/kvkk.md).

## What is in here, and what is not

![Diagram of the banking pack's record types: four structured types across the top, customer with person name, national identity number, date of birth, email, phone and address; account one to three per customer with an IBAN and a balance in kurus; card zero to two per account with an always-masked card number; and transaction many per account with an IBAN, an organization and a short document field. Below in red, three document types that each produce a label sidecar: complaint ticket, KYC note, and support transcript](assets/readme/record-map.png)

<p align="center"><sub><a href="assets/readme/record-map.svg">View the accessible SVG source</a></sub></p>

| In here | Not in here |
| --- | --- |
| Seven record types, three of which are free text | Any engine code. The only Python is under `tests/` and imports the public API alone |
| 26 invented bank names, scanned against a real-institution register in CI | Any real bank, merchant, or person. A collision fails the build |
| Three recipes, one of which is a labeled evaluation set | A dataset in git. Only bounded samples, capped at 50 records per type |
| Every identifier checksum-invalid by default | A corporate customer record type. This pack is retail, which is why tax numbers reach it through documents |

## Mint it yourself

```bash
uv tool install mintmark
git clone https://github.com/lokomotifai/mintmark-banking
cd mintmark-banking

mintmark packcheck .
mintmark mint --pack . --recipe retail-baseline --seed 20260901 --out ./run
mintmark verify ./run
```

Offline after dependency bootstrap. `packcheck` validates the declarations under
the strict loader, mini-mints them, and runs the invariant and denylist scans.

Want a look first, without minting anything? [`samples/`](samples/) carries fifty
records of every type, and a test regenerates them from a fixed seed and compares
by digest, so a sample that drifted from the declarations fails the build rather
than quietly misrepresenting them.

One complaint body, as emitted:

```
Sayin yetkili, Hasan Yılmaz adima kayitli hesabimla ilgili bir
sorun yasiyorum. kart konusunda defalarca basvurmama ragmen cozum
alamadim. Kimlik numaram 97978600710, hesabim
TR379999903250607630343066. Adresim Gültepe Mahallesi,
ulasilabilecegim numara +90 583 703 41 67. Konunun
degerlendirilmesini ve tarafima geri donus yapilmasini rica
ederim.
```

That is the first record in [`samples/complaint_ticket.jsonl`](samples/complaint_ticket.jsonl),
not an illustration written for the README. A test compares the two, so the
example cannot drift from what the pack actually emits.

Every value in it is synthetic, and the identity number fails its own check digit
rule. The sidecar for that document records a span for each of them.

## The evaluation set

The `pii-eval` recipe is the reason this pack exists in the shape it does. The
hushmark-tr model card asks adopters to evaluate a detector on representative
data before production use; this is that data for Turkish banking.

It declares a coverage target for every label and meets all eighteen:

| Label group | Target | Achieved |
| --- | --- | --- |
| PERSON, ADDRESS, ORG, DOB | 300 each | 2000 or more each |
| HEALTH, RELIGION, ETHNICITY, POLITICAL | 300 each | 482 to 529 |
| SEXUAL_LIFE, CRIMINAL, BIOMETRIC_REF, UNION | 300 each | 473 to 532 |
| TCKN, IBAN, PAN, PHONE, EMAIL | 500 each | 2000 or more each |
| VKN | 500 | 2074 |

That last row is worth a note. Every record type in this pack is retail, so there
is no corporate customer to carry a tax number in a field. VKN reaches the data
through document templates instead, in the phrasings where a tax number genuinely
appears in Turkish banking text: a disputed corporate mandate, a sole proprietor
confirming one during KYC, an invoice payment naming a merchant's.

The arithmetic behind the special-category rows is worth stating too, because it
is not obvious. Eight labels at 300 spans each is 2400 injections across 2000
documents, which is more than one per document. The baseline rate of 0.02 would
have produced about forty. The evaluation recipe therefore uses a separate
template family at a rate of one, with two special-category slots per document
and the labels spread evenly across the set. Baseline and evaluation templates
are separate sets rather than one set with a knob, so that a recipe cannot half
mix them.

## The three recipes

| Recipe | Shape | For |
| --- | --- | --- |
| **retail-baseline** | 10 000 customers, about 18 000 accounts, 9 000 cards, 250 000 transactions, and 2 800 documents | Filling a test environment with something that behaves like a portfolio |
| **pii-eval** | 2 000 documents, every label above its target | Measuring a detector's recall and precision on Turkish banking text |
| **anomaly-mix** | The baseline plus a labeled anomaly field on every transaction | Scoring a monitoring system against ground truth |

### A limitation of anomaly-mix, stated plainly

Every transaction carries `anomaly_kind` and `is_anomaly`, and the two never
disagree. But the four kinds are **per-row labels drawn at declared rates, not
genuine temporal structures**. A real burst is many transactions clustered in
time on one account; here it is a label.

That is a limit of the pack contract rather than an oversight: each field is
drawn from an independent stream, so a pack cannot declare a pattern that
correlates rows. Genuine temporal shapes need a core change, and it is recorded
as one. Use this recipe to check that your pipeline carries labels through
correctly. Do not use it to measure whether a detector finds real bursts.

## Identifiers cannot be real

Inherited from the core, and re-checked on the artifacts by `verify` rather than
promised:

- **TCKN** and **VKN** are computed correctly and then corrupted by a nonzero
  offset, so they fail the exact rule a validator applies.
- **IBAN** carries the bank code `99999`, verified absent from the published
  payment systems participant register. Even a validator-mode IBAN names no real
  institution.
- **PAN** begins with `9`, a major industry identifier no commercial card network
  uses, and is emitted masked.
- **EMAIL** sits only under names reserved by RFC 2606 and RFC 6761, which nobody
  can register.

Every reference dataset this repository publishes is minted with the safe policy.
A test asserts that for each of them.

## Fictional institutions, checked against real ones

The 26 bank names here follow a place-and-nature pattern rather than a
person-name one, because person-derived institution names collide with real
entities more often and can resemble a real person's business.

Every one is scanned in required CI against a denylist built from the published
participant register of licensed banks. A collision fails the build and names
both sides of it. A name that collides is removed, not defended.

The check runs over lexicons, templates, and minted output, so a real name cannot
enter through a template literal either.

## Repository map

```
pack.yaml           identity, the core pin, the allowed identifier policies
fields/             one file per record type, in generation order
recipes/            retail-baseline, pii-eval, anomaly-mix
templates/          baseline sets, and the separate evaluation sets
lexicons/           invented banks, products, counterparties, and the denylist
samples/            fifty records per type, regenerated from a fixed seed
vendor/             the core wheel required CI runs against, recorded by checksum
tests/              the conformance suite
docs/               the reference dataset record and engineering notes
```

## Develop the repository

```bash
uv sync
uv run mintmark packcheck .
uv run pytest
uv run python tools/mdlint.py .
```

All of it runs offline against the vendored core wheel. A separated,
network-labeled workflow confirms weekly that the vendored artifact still matches
the core repository at the pinned tag, because the offline check is only as good
as the artifact it runs against.

## Project status

Version 0.1.2, released. Two reference datasets are attached to
[v0.1.2](https://github.com/lokomotifai/mintmark-banking/releases/tag/v0.1.2), minted with the
safe identifier policy at the seeds declared in
[docs/reference-datasets.json](docs/reference-datasets.json). The engine is on PyPI as
[`mintmark`](https://pypi.org/project/mintmark/).

The seeds are settled deliberately. A changed seed silently invalidates a
published manifest, so it is never the fix for a coverage miss; the templates or
the document mix change instead.

Under semantic versioning, the public surface here is `pack.yaml`, the field
declarations, the recipes, the template sets, the lexicons, and the bytes a fixed
seed produces. After the first tagged release, adding an entry to a lexicon
changes the draw for every subsequent index, which makes it a major bump rather
than a minor one.

## Community contract

Contributions under the Developer Certificate of Origin 1.1, no contributor
license agreement. See [CONTRIBUTING.md](CONTRIBUTING.md), which explains why
there is no engine code here and what to do when a declaration cannot express
what the pack needs. [GOVERNANCE.md](GOVERNANCE.md) sets out what this repository
decides and what it does not. [SECURITY.md](SECURITY.md) covers the private
reporting route and what counts as a vulnerability in a repository that executes
nothing.

`README.md` is canonical and [README.tr.md](README.tr.md) is a full mirror.

## License and trademark

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE). The license grants no
right to the Mintmark name or logo; see [TRADEMARKS.md](TRADEMARKS.md).

Reference datasets are licensed **CC BY 4.0**: use them for anything, including
commercially, and credit the source. Every dataset carries its own credit line in
`MINTMARK.json` and `mintmark verify` prints it, so nothing has to be assembled by
hand. See [LICENSE-DATASETS.md](LICENSE-DATASETS.md). Pending legal confirmation;
nothing here states it as settled.

<p align="center"><sub>Part of the Mintmark family: <a href="https://github.com/lokomotifai/mintmark">the engine</a> · <a href="https://github.com/lokomotifai/mintmark-insurance">insurance</a> · <a href="https://github.com/lokomotifai/mintmark-hr">human resources</a></sub></p>
