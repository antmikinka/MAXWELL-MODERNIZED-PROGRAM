"""Integrity tests for the central reference-value store (Stage-4 C3/D-05).

The store is the single home for harvested Treatise goldens; these tests
guarantee the schema holds so migrated test files can rely on
``ref_value``/``tolerance_of`` without per-call defensiveness.

Run: PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/articles/test_reference_store.py
"""
from __future__ import annotations

import pytest

from articles import (
    entry,
    provenance,
    ref_entry,
    ref_value,
    reference_values,
    tolerance_of,
    units,
    validate_store,
)


def test_store_schema_is_valid() -> None:
    problems = validate_store()
    assert problems == [], "; ".join(problems)


def test_store_is_nontrivial_and_covers_last200_scope() -> None:
    """The migration seed must cover at least 10 distinct articles and must
    include goldens from the last-200 program scope (Arts. 667-866)."""
    store = reference_values()
    assert len(store) >= 10
    articles = {int(a) for a in store}
    assert all(1 <= a <= 866 for a in articles)
    assert any(667 <= a <= 866 for a in articles)


def test_every_entry_has_provenance_with_substance() -> None:
    """Provenance must say WHERE the number comes from, not just exist."""
    for art, art_entry in reference_values().items():
        for key, val in art_entry["values"].items():
            text = val["provenance"]
            assert len(text) >= 20, (
                f"article {art}.{key}: provenance too thin: {text!r}"
            )


def test_accessors_agree_and_raise_on_missing() -> None:
    art = sorted(reference_values(), key=int)[0]
    key = next(iter(entry(art)["values"]))
    assert ref_value(art, key) == entry(art)["values"][key]["value"]
    assert ref_entry(art, key)["units"] == units(art, key)
    assert ref_entry(art, key)["provenance"] == provenance(art, key)
    tol = tolerance_of(art, key)
    assert set(tol) in ({"rel"}, {"abs"})
    # mutating the returned tolerance must not corrupt the cached store
    (first_key,) = tol
    tol[first_key] = -1.0
    assert tolerance_of(art, key)[first_key] >= 0.0

    with pytest.raises(KeyError):
        entry(99999)
    with pytest.raises(KeyError):
        ref_entry(art, "no_such_key")
