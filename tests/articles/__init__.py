"""Central reference-value store for Treatise goldens (Stage-4 D-05 / C3).

``reference_values.json`` holds harvested golden values keyed by article
number (as a string).  Schema per entry::

    "<article>": {
      "values": {
        "<key>": {
          "value": <number>,
          "units": "<string>",
          "tolerance": {"rel": <n>} | {"abs": <n>},   # exactly one
          "provenance": "<mandatory non-empty string>"
        }
      }
    }

Loader API (import as ``from articles import ref_value, tolerance_of``):

* :func:`reference_values` -- the whole store (cached).
* :func:`entry`            -- one article's ``{"values": {...}}`` mapping.
* :func:`ref_entry`        -- one value entry dict.
* :func:`ref_value`        -- the bare numeric value.
* :func:`tolerance_of`     -- ``{"rel": x}`` / ``{"abs": x}`` unpackable
  straight into ``pytest.approx(value, **tolerance_of(art, key))``.
* :func:`provenance` / :func:`units` -- metadata accessors.
* :func:`validate_store`   -- schema integrity check (used by
  ``tests/articles/test_reference_store.py``).

Note on importability: ``tests/`` has no ``__init__.py``, so pytest's
prepend import mode puts ``tests/`` itself on ``sys.path``; this package is
therefore importable as ``articles`` from every test module.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

_STORE_PATH = Path(__file__).resolve().parent / "reference_values.json"

__all__ = [
    "reference_values",
    "entry",
    "ref_entry",
    "ref_value",
    "tolerance_of",
    "provenance",
    "units",
    "validate_store",
]


@lru_cache(maxsize=1)
def reference_values() -> Dict[str, Any]:
    """Return the full reference-value store (cached)."""
    with open(_STORE_PATH, encoding="utf-8") as handle:
        return json.load(handle)


def _article_key(article: int | str) -> str:
    return str(article)


def entry(article: int | str) -> Dict[str, Any]:
    """Return the ``{"values": {...}}`` entry for one article."""
    store = reference_values()
    key = _article_key(article)
    if key not in store:
        raise KeyError(f"reference_values.json has no entry for article {key}")
    return store[key]


def ref_entry(article: int | str, key: str) -> Dict[str, Any]:
    """Return the full value-entry dict for ``article``/``key``."""
    values = entry(article).get("values", {})
    if key not in values:
        raise KeyError(
            f"article {article}: no reference value named {key!r}; "
            f"available: {sorted(values)}"
        )
    return values[key]


def ref_value(article: int | str, key: str) -> float:
    """Return the bare golden number for ``article``/``key``."""
    return ref_entry(article, key)["value"]


def tolerance_of(article: int | str, key: str) -> Dict[str, float]:
    """Return the tolerance dict, unpackable into ``pytest.approx``.

    Example::

        assert x == pytest.approx(ref_value(712, "on_axis_uniformity"),
                                  **tolerance_of(712, "on_axis_uniformity"))
    """
    tol = ref_entry(article, key)["tolerance"]
    # Return a fresh copy so callers cannot mutate the cached store.
    return dict(tol)


def provenance(article: int | str, key: str) -> str:
    """Return the provenance string for ``article``/``key``."""
    return ref_entry(article, key)["provenance"]


def units(article: int | str, key: str) -> str:
    """Return the units string for ``article``/``key``."""
    return ref_entry(article, key)["units"]


def validate_store() -> list[str]:
    """Schema-validate the store; return a list of problems (empty == OK).

    Checks: top level is an object keyed by parseable article numbers in
    1..866; each entry has a ``values`` object; each value entry has a
    numeric non-bool ``value``, a string ``units``, a ``tolerance`` with
    exactly one of ``rel``/``abs`` (numeric, >= 0), and a non-empty string
    ``provenance``.
    """
    problems: list[str] = []
    try:
        store = reference_values()
    except Exception as exc:  # noqa: BLE001 - report, don't raise
        return [f"store does not parse: {exc!r}"]

    if not isinstance(store, dict):
        return [f"top level is {type(store).__name__}, expected object"]

    for art, art_entry in store.items():
        where = f"article {art}"
        try:
            number = int(art)
        except (TypeError, ValueError):
            problems.append(f"{where}: key is not an integer article number")
            continue
        if not 1 <= number <= 866:
            problems.append(f"{where}: article number outside 1..866")
        if not isinstance(art_entry, dict) or "values" not in art_entry:
            problems.append(f"{where}: missing 'values' object")
            continue
        values = art_entry["values"]
        if not isinstance(values, dict) or not values:
            problems.append(f"{where}: 'values' must be a non-empty object")
            continue
        for key, val in values.items():
            loc = f"{where}.{key}"
            if not isinstance(val, dict):
                problems.append(f"{loc}: entry is not an object")
                continue
            value = val.get("value")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                problems.append(f"{loc}: 'value' must be a number (non-bool)")
            units_field = val.get("units")
            if not isinstance(units_field, str) or not units_field.strip():
                problems.append(f"{loc}: 'units' must be a non-empty string")
            tol = val.get("tolerance")
            if not isinstance(tol, dict) or set(tol) not in ({"rel"}, {"abs"}):
                problems.append(
                    f"{loc}: 'tolerance' must be exactly one of rel/abs"
                )
            else:
                (bound,) = tol.values()
                if isinstance(bound, bool) or not isinstance(bound, (int, float)):
                    problems.append(f"{loc}: tolerance bound must be numeric")
                elif bound < 0:
                    problems.append(f"{loc}: tolerance bound must be >= 0")
            prov = val.get("provenance")
            if not isinstance(prov, str) or not prov.strip():
                problems.append(
                    f"{loc}: 'provenance' must be a non-empty string"
                )
    return problems
