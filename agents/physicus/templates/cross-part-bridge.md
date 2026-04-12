# Template: Cross-Part Bridge

## Purpose

Standardized template for implementing modules that bridge multiple Parts of Maxwell's Treatise. This template handles cross-part dependencies and ensures consistent treatment across electrostatics, magnetostatics, and electromagnetism.

## Source Category

**CRITICAL: Theory Preservation**

This template is for:
- **Maxwell's 1873 Historical Text**: Articles spanning multiple Parts
- **Standard Mathematical Implementation**: Multi-physics coupling
- **User Original Theory**: Mark any user extensions as "User Original Theory - Authoritative - DO NOT ALTER"

## Template Structure

### 1. Module Header

```python
"""
{BRIDGE_NAME} Cross-Part Bridge

Maxwell Treatise Reference:
- Part I Articles: {PART_I_ARTICLES}
- Part II Articles: {PART_II_ARTICLES}
- Part III Articles: {PART_III_ARTICLES}
- Part IV Articles: {PART_IV_ARTICLES}

Source Category:
- Maxwell 1873: Articles {X-Y} across Parts
- Standard Math: {Multi-physics coupling}
- User Theory: {NONE or specify}

CGS Units: {UNIT_SPECIFICATIONS}

Dependencies:
- Part I (Electrostatics): Layer 0-12
- Part II (Electrokinematics): Layer 13-30
- Part III (Magnetism): Layer 30b-42
- Part IV (Electromagnetism): Layer 43-86
"""

import numpy as np
from typing import Union, Optional, Dict, Tuple
from maxwell.core.vector import VectorField, ScalarField
from maxwell.utils.citation import maxwell_citation
```

### 2. Bridge Class Definition

```python
class {BridgeName}:
    """
    {BRIDGE_DESCRIPTION}
    
    Maxwell Articles: Multiple Parts (see below)
    
    Cross-Part Dependencies:
    - Part I: {PART_I_CONTRIBUTIONS}
    - Part II: {PART_II_CONTRIBUTIONS}
    - Part III: {PART_III_CONTRIBUTIONS}
    - Part IV: {PART_IV_CONTRIBUTIONS}
    
    Attributes:
        electrostatic_contribution: From Part I
        electrokinetic_contribution: From Part II
        magnetic_contribution: From Part III
        coupling_terms: Cross-part coupling
        citations: Maxwell article references
    
    CGS Units: {UNIT_SPECIFICATIONS}
    """
    
    def __init__(
        self,
        electrostatic_part: Optional[object] = None,
        electrokinetic_part: Optional[object] = None,
        magnetic_part: Optional[object] = None,
        coupling_parameters: Optional[Dict] = None,
        citations: Optional[list] = None
    ):
        self.electrostatic = electrostatic_part
        self.electrokinetic = electrokinetic_part
        self.magnetic = magnetic_part
        self.coupling = coupling_parameters or {}
        self.citations = citations or self._default_citations()
    
    @staticmethod
    def _default_citations() -> list:
        """Return Maxwell article citations from all Parts."""
        return [
            maxwell_citation(article={N}, part='I'),
            maxwell_citation(article={N}, part='II'),
            maxwell_citation(article={N}, part='III'),
            maxwell_citation(article={N}, part='IV'),
        ]
```

### 3. Electromagnetic Coupling

```python
    def full_maxwell_system(
        self,
        charge_density: Callable,
        current_density: Callable,
        boundary_conditions: Dict
    ) -> Dict:
        """
        Solve complete Maxwell equation system.
        
        Args:
            charge_density: ρ(x,y,z,t)
            current_density: J(x,y,z,t)
            boundary_conditions: For all fields
        
        Returns:
            dict: {E, B, V, A} fields
        
        Maxwell Equations (CGS):
            ∇·D = 4πρ        (Part I, Art. 608)
            ∇·B = 0          (Part III, Art. 403)
            ∇×E = -(1/c)∂B/∂t  (Part IV, Art. 590)
            ∇×H = (4π/c)J + (1/c)∂D/∂t  (Part IV, Art. 607)
        
        Cross-Part Dependencies:
            - Gauss's law from Part I
            - Solenoidal B from Part III
            - Faraday's law from Part IV
            - Ampère-Maxwell from Part IV
        """
        # This couples all four Parts
        pass
    
    def quasistatic_approximation(
        self,
        timescale: float,
        lengthscale: float
    ) -> str:
        """
        Determine appropriate quasistatic approximation.
        
        Args:
            timescale: Characteristic time τ
            lengthscale: Characteristic length L
        
        Returns:
            str: 'electrostatic', 'magnetostatic', or 'full'
        
        Criterion:
            - If L/(cτ) << 1: electroquasistatic
            - If L/(cτ) << 1 and magnetic dominant: magnetoquasistatic
            - Otherwise: full Maxwell
        """
        from maxwell.core.constants import c_CGS
        
        ratio = lengthscale / (c_CGS * timescale)
        
        if ratio < 0.01:
            # Check which effect dominates
            if self._electric_energy_dominant():
                return 'electroquasistatic'  # Part I + Part II
            else:
                return 'magnetoquasistatic'  # Part III + Part II
        else:
            return 'full_maxwell'  # All Parts
```

### 4. Electrostatic-Magnetostatic Bridge

```python
    def electromagnetic_stress_tensor(
        self,
        E_field: VectorField,
        B_field: VectorField
    ) -> np.ndarray:
        """
        Combined stress tensor from E and B fields.
        
        Args:
            E_field: From Part I electrostatics
            B_field: From Part III magnetostatics
        
        Returns:
            ndarray: 3x3 stress tensor
        
        Maxwell Reference:
            - Part I: Arts. 103-110 (electrostatic stress)
            - Part IV: Arts. 641-646 (full stress)
        
        Formula:
            T_ij = (1/4π)[E_i E_j + B_i B_j - (1/2)δ_ij(E² + B²)]
        """
        # Part I contribution
        T_electrostatic = self._electrostatic_stress(E_field)
        
        # Part III contribution  
        T_magnetic = self._magnetostatic_stress(B_field)
        
        # Combined
        T_combined = T_electrostatic + T_magnetic
        
        return T_combined
    
    def poynting_theorem_verification(
        self,
        E_field: VectorField,
        B_field: VectorField,
        J_field: VectorField
    ) -> Dict:
        """
        Verify Poynting theorem across Parts.
        
        Args:
            E_field: Electric field
            B_field: Magnetic field
            J_field: Current density
        
        Returns:
            dict: Energy balance verification
        
        Maxwell Reference:
            - Part I: Energy density (Arts. 630-638)
            - Part III: Magnetic energy
            - Part IV: Poynting theorem (Arts. 630-638)
        
        Poynting Theorem:
            ∂u/∂t + ∇·S = -J·E
        
        Where:
            u = (E² + B²)/8π (energy density)
            S = (c/4π) E × H (Poynting vector)
        """
        # Energy density (Part I + Part III)
        u_electric = E_field.magnitude**2 / (8 * np.pi)
        u_magnetic = B_field.magnitude**2 / (8 * np.pi)
        u_total = u_electric + u_magnetic
        
        # Poynting vector (Part IV)
        from maxwell.core.constants import c_CGS
        H_field = B_field  # In vacuum
        S = (c_CGS / (4 * np.pi)) * np.cross(E_field, H_field)
        
        # Work term (Part II)
        J_dot_E = np.dot(J_field.components, E_field.components)
        
        # Verify balance
        time_derivative_u = self._compute_time_derivative(u_total)
        div_S = S.divergence()
        
        residual = time_derivative_u + div_S + J_dot_E
        
        return {
            'energy_density': u_total,
            'poynting_flux': S,
            'work_rate': J_dot_E,
            'balance_residual': residual,
            'verified': np.max(np.abs(residual)) < 1e-6
        }
```

### 5. Circuit-Field Coupling

```python
    def circuit_field_interface(
        self,
        circuit currents: Dict,
        field_region: Dict
    ) -> Dict:
        """
        Couple circuit theory (Part II) with fields (Parts I, III, IV).
        
        Args:
            circuit_currents: {branch: I_value}
            field_region: Spatial region specification
        
        Returns:
            dict: Coupled solution
        
        Cross-Part Coupling:
            - Part II: Circuit currents (Arts. 273-284)
            - Part III: B field from currents (Arts. 475-479)
            - Part IV: Induction back on circuits (Arts. 528-531)
        """
        # From Part II: Get current distribution
        J = self._circuit_to_current_density(circuit_currents)
        
        # From Part III: Compute B field
        B = self._biot_savart(J)
        
        # From Part IV: Compute induced EMF
        dPhi_dt = self._compute_flux_derivative(B)
        induced_EMF = -(1/c_CGS) * dPhi_dt
        
        # Back-coupling to circuit
        circuit_response = self._update_circuit_with_EMF(induced_EMF)
        
        return {
            'current_density': J,
            'magnetic_field': B,
            'induced_EMF': induced_EMF,
            'circuit_response': circuit_response
        }
```

### 6. Material Interface

```python
    def material_boundary_conditions(
        self,
        region_1: Dict,
        region_2: Dict,
        interface: Dict
    ) -> Dict:
        """
        Apply boundary conditions at material interface.
        
        Args:
            region_1: Material properties (ε₁, μ₁, σ₁)
            region_2: Material properties (ε₂, μ₂, σ₂)
            interface: Interface geometry
        
        Returns:
            dict: Field values at boundary
        
        Maxwell Reference:
            - Part I: Dielectric boundaries (Arts. 78a-c)
            - Part III: Magnetic boundaries (Arts. 400-402)
            - Part IV: Full EM boundary conditions
        
        Boundary Conditions:
            D₁n - D₂n = 4πσ_surface  (Part I)
            B₁n = B₂n                (Part III)
            E₁t = E₂t                (Part I)
            H₁t - H₂t = (4π/c)K      (Part IV)
        """
        # Extract normal and tangential components
        E1_n, E1_t = self._decompose_field(region_1['E'], interface.normal)
        E2_n, E2_t = self._decompose_field(region_2['E'], interface.normal)
        
        # Apply boundary conditions
        # Part I: Tangential E continuous
        assert np.allclose(E1_t, E2_t), "Tangential E discontinuous"
        
        # Part I: Normal D discontinuous by surface charge
        D1_n = region_1['epsilon'] * E1_n
        D2_n = region_2['epsilon'] * E2_n
        surface_charge = (D1_n - D2_n) / (4 * np.pi)
        
        # Part III: Normal B continuous
        B1_n = region_1['B'] @ interface.normal
        B2_n = region_2['B'] @ interface.normal
        assert np.allclose(B1_n, B2_n), "Normal B discontinuous"
        
        return {
            'surface_charge': surface_charge,
            'E_tangential': E1_t,  # = E2_t
            'B_normal': B1_n,
            'boundary_verified': True
        }
```

### 7. Energy Conservation

```python
    def total_energy_accounting(
        self,
        include_parts: list = ['I', 'II', 'III', 'IV']
    ) -> Dict:
        """
        Compute total energy across all Parts.
        
        Args:
            include_parts: Which Parts to include
        
        Returns:
            dict: Energy breakdown by Part
        
        Energy Contributions:
            - Part I: Electrostatic energy (Arts. 85a-b)
            - Part II: Electrokinetic energy (Arts. 551-552)
            - Part III: Magnetostatic energy (Arts. 630-638)
            - Part IV: Field energy + interaction (Arts. 630-638)
        """
        energy = {}
        
        if 'I' in include_parts:
            # Part I: W = (1/2) ∫ ρV dτ
            energy['electrostatic'] = self._electrostatic_energy()
        
        if 'II' in include_parts:
            # Part II: Circuit energy (I²R losses, etc.)
            energy['electrokinetic'] = self._electrokinetic_energy()
        
        if 'III' in include_parts:
            # Part III: Magnetic energy
            energy['magnetostatic'] = self._magnetostatic_energy()
        
        if 'IV' in include_parts:
            # Part IV: Full EM field energy
            energy['electromagnetic'] = self._field_energy()
        
        energy['total'] = sum(energy.values())
        
        return energy
    
    def verify_conservation_across_parts(
        self,
        time_series: Dict
    ) -> bool:
        """
        Verify energy conservation across all Parts.
        
        Args:
            time_series: Time series of field configurations
        
        Returns:
            bool: True if energy conserved
        
        Maxwell Reference:
            - Part II: Art. 262 (energy in electrolysis)
            - Part IV: Arts. 543-544 (general conservation)
        """
        total_energies = []
        
        for t, fields in time_series.items():
            energy = self.total_energy_accounting()
            total_energies.append(energy['total'])
        
        # Check conservation
        relative_change = (max(total_energies) - min(total_energies)) / np.mean(total_energies)
        
        return relative_change < 1e-6
```

### 8. Dependency Graph

```python
    def get_dependency_graph(self) -> Dict:
        """
        Return cross-part dependency graph.
        
        Returns:
            dict: Dependency structure
        
        Dependencies:
            Part I (Electrostatics): Foundation
            Part II (Electrokinematics): Depends on Part I
            Part III (Magnetism): Depends on Part I
            Part IV (Electromagnetism): Depends on Parts I, II, III
        """
        return {
            'Part I': {
                'depends_on': [],
                'provides': ['charge', 'E_field', 'potential'],
                'layers': '0-12'
            },
            'Part II': {
                'depends_on': ['Part I'],
                'provides': ['current', 'resistance', 'networks'],
                'layers': '13-30'
            },
            'Part III': {
                'depends_on': ['Part I'],
                'provides': ['magnetization', 'H_field', 'B_field'],
                'layers': '30b-42'
            },
            'Part IV': {
                'depends_on': ['Part I', 'Part II', 'Part III'],
                'provides': ['full_Maxwell', 'waves', 'dynamics'],
                'layers': '43-86'
            }
        }
```

## Checklist for Implementation

- [ ] Module header with all Part citations
- [ ] CGS units specified
- [ ] Source category documented
- [ ] Cross-part dependencies identified
- [ ] Coupling terms implemented
- [ ] Boundary conditions handled
- [ ] Energy conservation verified
- [ ] Dependency graph documented
- [ ] Theory preservation decorators
- [ ] Maxwell article citations from all Parts

## Related Templates

- `field-implementation.md` - Single-part implementation
- `constitutive-relation.md` - Material handling
- `dynamical-system.md` - Full dynamics
- `validation-protocol.md` - Cross-part validation
