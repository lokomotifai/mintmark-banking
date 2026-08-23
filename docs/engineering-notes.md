# Engineering notes

Operational know-how for this repository. Committed, unlike the plan.

## The core wheel is bound to an immutable source revision

`pack.yaml` requires Mintmark `>=0.3,<0.4`, while required CI installs the
vendored `mintmark-0.3.0-py3-none-any.whl` whose SHA-256 is recorded in
`vendor/CHECKSUMS`. The separated network workflow checks out core commit
`499216efdc8d30ccb21d4a4a03a38b014b0ca870`, rebuilds it, and byte-compares that
independently sourced wheel with the vendored artifact.

## Why there are evaluation twins of the document types

The baseline recipe wants the special-category density of ordinary banking text.
The evaluation recipe needs more than one special-category span per document, or
its coverage targets are unreachable.

A recipe selects a template set through the record type that names it, so the two
densities need two record types rather than one type with a switch. Hence
`complaint_ticket` and `complaint_ticket_eval`, and the same for the other two.
Each recipe sets the other family's counts to zero.

The alternative, one type whose template set a recipe overrides, would let a
recipe half-mix the families and produce a dataset whose density nobody declared.

## The special-category rate comes from the recipe

Templates write `[?special: ...]` rather than a literal probability, and the rate
comes from the recipe's `special_rate`. Before the core supported that, a recipe
declared the field and nothing read it: template authors fixed the density with
literal probabilities and the recipe only appeared to govern it.

If you write a literal rate in a special-category slot, you have taken that slot
out of the recipe's control. Do not.

## VKN reaches this pack only through documents

Every record type here is retail, so no field carries a tax number. The
evaluation recipe still needs 500 VKN spans, so the complaint and KYC templates
carry `{id:VKN}` in phrasings where a tax number genuinely appears in Turkish
banking text.

Do not solve this by adding a corporate customer record type. The brief settles
the record set, and the insurance pack is where corporate policyholders live.

## The anomaly kinds are labels, not structures

`anomaly_kind` is drawn per row at declared rates. A real burst is many
transactions clustered in time on one account; the pack contract cannot declare a
pattern that correlates rows, because each field comes from an independent
stream.

This is recorded in both READMEs rather than left for a user to discover. Genuine
temporal shapes are a core change. If one lands, the baseline contract changes
with it and that is a major version event. A former `anomaly-mix` recipe was
removed because it was byte-for-byte identical to the baseline and falsely
implied that a recipe could alter field-level anomaly rates.

## Regenerating the samples

    mintmark mint --pack . --recipe retail-baseline --seed 1 \
      --records customer=6 --records account=6 --records card=3 \
      --records transaction=48 --records complaint_ticket=6 \
      --records kyc_note=6 --records support_transcript=6 \
      --out ./regenerated

Then copy the JSONL files into `samples/`. The freshness test compares by bytes,
so a drift fails the build.

Do not commit a sample file that is empty. The evaluation twins produce nothing
under the baseline recipe, and an empty committed file represents nothing while
looking like coverage.

## Adding to a lexicon after the first release

It changes the draw for every subsequent index, which changes emitted bytes for a
fixed seed, which breaks the reproducibility of every published manifest. That
makes it a major version bump.

Before the first tagged release it is free. After, it is a decision.

## Why birth dates carry an age window

`birth_date` used to be a plain `datetime_window` draw, which meant every person
in a dataset describing 2026 was also born in 2026. Nothing in the suite caught
it: the field is a valid date, the label is right, the span aligns, the manifest
verifies. It is only wrong to a reader, which is the one check that had not run.

The field now declares `params: {age_years: [18, 90]}`, and the core draws from
the span that would give a person that age at the start of the recipe window. The
parameter is optional and a field that omits it behaves exactly as before, so no
other declaration in the family had to move.

Adopting it moved emitted bytes for a fixed seed, so the samples were regenerated
and the pack version went to 0.1.1. That is the rule this pack already had for
lexicon growth, applied to a declaration change.

## A version bump changes every emitted byte

The pack version is one of the six inputs the engine derives every generation
stream from, alongside the seed, the engine's major version, the pack name, the
recipe name, and the site path. So raising `version` in `pack.yaml` changes every
value in every record for a fixed seed, and the sample freshness test fails until
the samples are regenerated.

That reads like a bug the first time it happens. It is the opposite: version and
content correspond exactly, so two datasets carrying the same pack version cannot
differ, and nobody can quietly change what a version emits. The cost is that a
bump is never free for anyone holding a published manifest, which is the reason
the family treats one as a decision rather than a formality.

The pack digest is a separate thing and does not seed anything. It records which
declarations produced a dataset, so a consumer can tell whether the pack they
hold is the pack it came from. An earlier note here said the version reached the
streams by way of the digest. That was wrong, and worth correcting rather than
quietly deleting: it is the kind of plausible mechanism somebody would go on to
reason from.
