"""
Test citation decorator compliance.

Ensures all public functions have @maxwell_cite decorators with correct metadata.
This is critical for traceability back to Maxwell's original Treatise.

Tests verify:
- Every public function has a citation decorator
- Citations contain valid article numbers
- Part numbers match expected values
- Theory classes are correctly assigned
"""

from __future__ import annotations
import pytest
import inspect
from typing import Any

from maxwell.meta.citation import get_citation, get_all_citations, MaxwellCitation


class TestCitationDecorator:
    """Test suite for citation decorator validation."""

    def test_decorated_function_has_citation(self, require_citation) -> None:
        """Verify that decorated functions have citations attached."""
        # Import a known decorated function
        from maxwell.physics.coulomb import coulomb_law

        citation = require_citation(coulomb_law)
        assert isinstance(citation, MaxwellCitation)
        assert len(citation.articles) > 0
        assert citation.part >= 1
        assert citation.part <= 6

    def test_citation_articles_are_positive(self) -> None:
        """Verify all citation article numbers are positive integers."""
        all_citations = get_all_citations()

        for qualname, citation in all_citations.items():
            for article in citation.articles:
                assert article > 0, (
                    f"Article number must be positive in {qualname}: {article}"
                )

    def test_citation_part_in_valid_range(self) -> None:
        """Verify all citation part numbers are in range 1-6."""
        all_citations = get_all_citations()

        for qualname, citation in all_citations.items():
            assert 1 <= citation.part <= 6, (
                f"Part number must be 1-6 in {qualname}: {citation.part}"
            )

    def test_citation_theory_class_valid(self) -> None:
        """Verify all theory classes are valid."""
        valid_classes = {"maxwell_original", "user_original", "standard_math"}
        all_citations = get_all_citations()

        for qualname, citation in all_citations.items():
            assert citation.theory_class in valid_classes, (
                f"Invalid theory_class in {qualname}: {citation.theory_class}"
            )


class TestOerstedModuleCitations:
    """Test citation compliance for Oersted module (Arts. 475-479)."""

    @pytest.fixture(autouse=True)
    def setup_oersted_module(self) -> None:
        """Import the Oersted module before each test."""
        # Import to register citations
        from maxwell.electromagnetism.sources import oersted
        self.module = oersted

    def test_calc_oersted_field_has_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify calc_oersted_field has correct citation."""
        func = self.module.calc_oersted_field
        citation = require_citation(func)
        validate_citation_articles(func, part=4, articles=[475, 476])

    def test_calc_field_from_element_has_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify calc_field_from_element has correct citation."""
        func = self.module.calc_field_from_element
        citation = require_citation(func)
        validate_citation_articles(func, part=4, articles=[477, 478])

    def test_calc_force_on_pole_has_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify calc_force_on_pole has correct citation."""
        func = self.module.calc_force_on_pole
        citation = require_citation(func)
        validate_citation_articles(func, part=4, articles=[479])

    def test_calc_circular_field_direction_has_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify calc_circular_field_direction has correct citation."""
        func = self.module.calc_circular_field_direction
        citation = require_citation(func)
        validate_citation_articles(func, part=4, articles=[475, 476])

    def test_verify_inverse_distance_law_has_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify verify_inverse_distance_law has correct citation."""
        func = self.module.verify_inverse_distance_law
        citation = require_citation(func)
        validate_citation_articles(func, part=4, articles=[475, 476, 477, 478])

    def test_oersted_field_class_has_citation(
        self,
        require_citation
    ) -> None:
        """Verify OerstedField class methods have citations."""
        from maxwell.electromagnetism.sources.oersted import OerstedField

        # Check class methods
        for method_name in ["field_at", "direction_at", "magnitude_at"]:
            if hasattr(OerstedField, method_name):
                method = getattr(OerstedField, method_name)
                if callable(method):
                    citation = get_citation(method)
                    # Class methods should have citations
                    assert citation is not None, (
                        f"OerstedField.{method_name} must have @maxwell_cite decorator"
                    )

    def test_calc_field_from_finite_wire_has_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify calc_field_from_finite_wire has correct citation."""
        func = self.module.calc_field_from_finite_wire
        citation = require_citation(func)
        validate_citation_articles(func, part=4, articles=[477, 478])

    def test_calc_dipole_interaction_has_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify calc_dipole_interaction has correct citation."""
        func = self.module.calc_dipole_interaction
        citation = require_citation(func)
        validate_citation_articles(func, part=4, articles=[479])


class TestTraceabilityCoverage:
    """Test overall traceability coverage."""

    def test_module_public_functions_coverage(self) -> None:
        """Verify all public functions in a module have citations."""
        # Test electromagnetism module
        from maxwell.electromagnetism.sources import oersted

        uncited = []
        for name, obj in inspect.getmembers(oersted, inspect.isfunction):
            if name.startswith("_"):
                continue
            # Skip imported decorators/constructors that aren't actual functions
            if obj.__module__ != "maxwell.electromagnetism.sources.oersted":
                continue
            if get_citation(obj) is None:
                uncited.append(f"oersted.{name}")

        assert len(uncited) == 0, (
            f"Uncited public functions: {uncited}"
        )

    def test_verify_traceability_function(self) -> None:
        """Test the verify_traceability utility function."""
        from maxwell.meta.citation import verify_traceability
        from maxwell.electromagnetism.sources import oersted

        result = verify_traceability([oersted])

        assert "total" in result
        assert "cited" in result
        assert "uncited" in result
        assert "coverage_pct" in result

        # The verify_traceability function counts all functions including imports
        # The important thing is that all oersted module functions are cited
        # We verify this separately in test_module_public_functions_coverage
        assert result["cited"] > 0, "Should have some cited functions"
        assert result["total"] > 0, "Should have some total functions"
