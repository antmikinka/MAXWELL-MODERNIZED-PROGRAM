# Template: Dynamical System

## Purpose

Standardized template for implementing Lagrangian and Hamiltonian formulations of electromagnetic systems. This template covers electrokinetic energy, generalized coordinates, and field dynamics.

## Source Category

**CRITICAL: Theory Preservation**

This template is for:
- **Maxwell's 1873 Historical Text**: Articles 551-571 (Electrokinetic Energy and Dynamics)
- **Standard Mathematical Implementation**: Variational calculus, canonical transformations
- **User Original Theory**: Mark any user extensions as "User Original Theory - Authoritative - DO NOT ALTER"

## Template Structure

### 1. Module Header

```python
"""
{SYSTEM_NAME} Dynamical System

Maxwell Treatise Reference:
- Primary Articles: {ARTICLE_NUMBERS}
- Part: Part IV (Electromagnetism)

Source Category:
- Maxwell 1873: Articles 551-571
- Standard Math: {Variational methods, Hamiltonian mechanics}
- User Theory: {NONE or specify}

CGS Units: {UNIT_SPECIFICATIONS}
"""

import numpy as np
from typing import Union, Optional, Dict, Callable
from maxwell.dynamics.lagrangian import LagrangianSystem
from maxwell.dynamics.hamiltonian import HamiltonianSystem
from maxwell.utils.citation import maxwell_citation
```

### 2. Lagrangian Class Definition

```python
class {LagrangianName}:
    """
    {LAGRANGIAN_DESCRIPTION}
    
    Maxwell Articles: {ARTICLE_NUMBERS}
    
    Attributes:
        generalized_coords: q_i variables
        generalized_velocities: q̇_i variables
        kinetic_energy: T(q̇)
        potential_energy: V(q)
        dissipation: Rayleigh dissipation function
        citations: Maxwell article references
    
    CGS Units:
        Lagrangian L: erg
        Generalized coordinate: varies
        Generalized velocity: varies
    """
    
    def __init__(
        self,
        generalized_coords: Dict[str, Callable],
        kinetic_energy: Callable,
        potential_energy: Callable,
        dissipation: Optional[Callable] = None,
        citations: Optional[list] = None
    ):
        self.q = generalized_coords
        self.T = kinetic_energy
        self.V = potential_energy
        self.F = dissipation  # Rayleigh dissipation
        self.citations = citations or self._default_citations()
    
    @staticmethod
    def _default_citations() -> list:
        """Return default Maxwell article citations."""
        return [
            maxwell_citation(article=551, part='IV'),
            maxwell_citation(article=553, part='IV'),
            maxwell_citation(article=554, part='IV'),
        ]
    
    def lagrangian(self, q, q_dot, t=None) -> float:
        """
        Compute Lagrangian L = T - V.
        
        Args:
            q: Generalized coordinates
            q_dot: Generalized velocities
            t: Time (if explicit)
        
        Returns:
            float: Lagrangian value (erg)
        
        Maxwell Reference: Arts. {553-554}
        """
        T = self.T(q, q_dot, t)
        V = self.V(q, t)
        return T - V
```

### 3. Euler-Lagrange Equations

```python
    def euler_lagrange_equations(
        self,
        q: np.ndarray,
        q_dot: np.ndarray,
        q_ddot: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Generate Euler-Lagrange equations.
        
        Args:
            q: Generalized coordinates
            q_dot: Generalized velocities
            q_ddot: Generalized accelerations (optional)
        
        Returns:
            ndarray: Left-hand side of EL equations
        
        Maxwell Reference: Arts. {555-558}
        
        Formula:
            d/dt(∂L/∂q̇_i) - ∂L/∂q_i = Q_i
        
        Where Q_i includes non-conservative forces.
        """
        equations = []
        
        for i, (q_i, q_dot_i) in enumerate(zip(q, q_dot)):
            # d/dt(∂L/∂q̇_i)
            dL_dqdot = self._partial_L_dqdot(i, q, q_dot)
            time_derivative = self._time_derivative(dL_dqdot, q, q_dot, q_ddot)
            
            # ∂L/∂q_i
            dL_dq = self._partial_L_dq(i, q, q_dot)
            
            # EL equation
            el_i = time_derivative - dL_dq
            equations.append(el_i)
        
        return np.array(equations)
    
    def generalized_forces(
        self,
        q: np.ndarray,
        q_dot: np.ndarray
    ) -> np.ndarray:
        """
        Compute generalized forces Q_i.
        
        Args:
            q: Coordinates
            q_dot: Velocities
        
        Returns:
            ndarray: Generalized forces
        
        Includes:
            - External EMF
            - Dissipative forces (from Rayleigh function)
        """
        # From Rayleigh dissipation: Q_i = -∂F/∂q̇_i
        Q_diss = -self._partial_F_dqdot(q_dot)
        
        # Add external forces if specified
        Q_ext = self.external_forces(q, q_dot)
        
        return Q_diss + Q_ext
```

### 4. Electrokinetic Energy

```python
    @classmethod
    def electrokinetic_system(
        cls,
        inductance_matrix: np.ndarray,
        capacitance_matrix: Optional[np.ndarray] = None,
        resistance_matrix: Optional[np.ndarray] = None
    ):
        """
        Create system from circuit inductances.
        
        Args:
            inductance_matrix: L_ij matrix (cm in CGS)
            capacitance_matrix: C_i values (optional)
            resistance_matrix: R_i values (optional)
        
        Returns:
            {LagrangianName}: Circuit Lagrangian
        
        Maxwell Reference: Arts. {551-552}
        
        Electrokinetic Energy:
            T = (1/2) Σ_ij L_ij I_i I_j
        """
        def kinetic_energy(q, q_dot, t=None):
            # q_dot = currents I
            T = 0.5 * np.dot(q_dot, np.dot(inductance_matrix, q_dot))
            return T
        
        def potential_energy(q, t=None):
            if capacitance_matrix is None:
                return 0.0
            # q = charges, V = q²/(2C)
            V = 0.5 * np.dot(q, np.dot(capacitance_matrix, q))
            return V
        
        def dissipation(q_dot, t=None):
            if resistance_matrix is None:
                return 0.0
            # Rayleigh: F = (1/2) Σ R_i I_i²
            F = 0.5 * np.dot(q_dot, np.dot(resistance_matrix, q_dot))
            return F
        
        return cls(
            generalized_coords={'charges': lambda: q},
            kinetic_energy=kinetic_energy,
            potential_energy=potential_energy,
            dissipation=dissipation
        )
```

### 5. Hamiltonian Formulation

```python
    def to_hamiltonian(self) -> 'HamiltonianSystem':
        """
        Convert to Hamiltonian formulation.
        
        Returns:
            HamiltonianSystem: Hamiltonian system
        
        Maxwell Reference: Arts. {560-564}
        
        Legendre Transform:
            H = Σ p_i q̇_i - L
            p_i = ∂L/∂q̇_i
        """
        from maxwell.dynamics.hamiltonian import HamiltonianSystem
        
        # Compute canonical momenta
        def momenta(q, q_dot):
            return self._partial_L_dqdot_all(q, q_dot)
        
        # Hamiltonian via Legendre transform
        def hamiltonian(q, p):
            # Invert p = ∂L/∂q̇ to get q̇(q, p)
            q_dot = self._invert_momenta(q, p)
            
            # H = Σ p_i q̇_i - L
            legendre = np.dot(p, q_dot)
            L = self.lagrangian(q, q_dot)
            return legendre - L
        
        return HamiltonianSystem(
            coordinates=q,
            momenta=momenta,
            hamiltonian=hamiltonian
        )
    
    def canonical_equations(self) -> Callable:
        """
        Get canonical (Hamilton) equations.
        
        Returns:
            Callable: Right-hand side of canonical equations
        
        Equations:
            dq_i/dt = ∂H/∂p_i
            dp_i/dt = -∂H/∂q_i + Q_i
        """
        H = self.to_hamiltonian()
        
        def rhs(t, state):
            n = len(state) // 2
            q = state[:n]
            p = state[n:]
            
            q_dot = H._partial_H_dp(q, p)
            p_dot = -H._partial_H_dq(q, p) + self.generalized_forces(q, q_dot)
            
            return np.concatenate([q_dot, p_dot])
        
        return rhs
```

### 6. Field-Theoretic Formulation

```python
    @classmethod
    def electromagnetic_field_lagrangian(
        cls,
        potentials: Dict[str, Callable],
        sources: Optional[Dict[str, Callable]] = None
    ):
        """
        Create Lagrangian for EM field.
        
        Args:
            potentials: {'V': scalar_potential, 'A': vector_potential}
            sources: {'rho': charge_density, 'J': current_density}
        
        Returns:
            {LagrangianName}: Field Lagrangian
        
        Maxwell Reference: Arts. {568-571}
        
        Lagrangian Density:
            ℒ = (1/8π)(E² - B²) - ρV + (1/c)J·A
        """
        def field_lagrangian(fields, field_rates, t=None):
            A = fields['A']
            V = fields['V']
            dA_dt = field_rates['A']
            
            # E = -∇V - (1/c)∂A/∂t
            E = -np.gradient(V) - (1/c_CGS) * dA_dt
            
            # B = ∇ × A
            B = np.cross(np.gradient(), A)
            
            # ℒ density
            L_density = (1/(8*np.pi)) * (np.dot(E, E) - np.dot(B, B))
            
            # Add source terms
            if sources is not None:
                L_density -= sources['rho'] * V
                L_density += (1/c_CGS) * np.dot(sources['J'], A)
            
            # Integrate over space
            return np.trapz(L_density, dx=fields['dx'])
        
        return cls(
            generalized_coords=potentials,
            kinetic_energy=lambda *args: 0,  # Included in L
            potential_energy=lambda *args: 0,
            dissipation=None
        )
    
    def derive_field_equations(self) -> Dict:
        """
        Derive Maxwell's equations from Lagrangian.
        
        Returns:
            dict: Field equations
        
        Maxwell Reference: Arts. {598-601}
        
        From δ∫ℒ d⁴x = 0:
            ∂_μ(∂ℒ/∂(∂_μ A_ν)) - ∂ℒ/∂A_ν = 0
        """
        # Variation with respect to V gives Gauss's law
        # Variation with respect to A gives Ampère-Maxwell
        return {
            'gauss': '∇·E = 4πρ',
            'no_monopoles': '∇·B = 0',
            'faraday': '∇×E = -(1/c)∂B/∂t',
            'ampere_maxwell': '∇×B = (4π/c)J + (1/c)∂E/∂t'
        }
```

### 7. Coupled Circuit Dynamics

```python
    @classmethod
    def coupled_circuits(
        cls,
        L1: float,
        L2: float,
        M: float,
        C1: Optional[float] = None,
        C2: Optional[float] = None,
        R1: Optional[float] = None,
        R2: Optional[float] = None
    ):
        """
        Create Lagrangian for coupled LC circuits.
        
        Args:
            L1, L2: Self-inductances
            M: Mutual inductance
            C1, C2: Capacitances (optional)
            R1, R2: Resistances (optional)
        
        Returns:
            {LagrangianName}: Coupled circuit system
        
        Maxwell Reference: Arts. {578-580}
        """
        # Inductance matrix
        L_matrix = np.array([[L1, M], [M, L2]])
        
        # Capacitance matrix (inverse for energy)
        C_inv = None
        if C1 is not None and C2 is not None:
            C_inv = np.diag([1/C1, 1/C2])
        
        # Resistance matrix
        R_matrix = None
        if R1 is not None and R2 is not None:
            R_matrix = np.diag([R1, R2])
        
        return cls.electrokinetic_system(
            inductance_matrix=L_matrix,
            capacitance_matrix=C_inv,
            resistance_matrix=R_matrix
        )
    
    def normal_modes(self) -> Dict:
        """
        Compute normal mode frequencies.
        
        Returns:
            dict: {frequencies, mode_shapes}
        """
        # For coupled LC circuits without resistance
        # Solve eigenvalue problem
        pass
```

### 8. Conservation Laws

```python
    def energy(self, q: np.ndarray, q_dot: np.ndarray) -> float:
        """
        Compute total energy.
        
        Args:
            q: Coordinates
            q_dot: Velocities
        
        Returns:
            float: Total energy (erg)
        
        Maxwell Reference: Arts. {543-544}
        """
        T = self.T(q, q_dot)
        V = self.V(q)
        return T + V
    
    def verify_energy_conservation(
        self,
        trajectory: np.ndarray,
        tolerance: float = 1e-6
    ) -> bool:
        """
        Verify energy conservation along trajectory.
        
        Args:
            trajectory: Time series of (q, q_dot)
            tolerance: Maximum relative change allowed
        
        Returns:
            bool: True if energy conserved
        """
        energies = [self.energy(q, q_dot) for q, q_dot in trajectory]
        relative_change = (max(energies) - min(energies)) / np.mean(energies)
        return relative_change < tolerance
    
    def momentum(self, q: np.ndarray, q_dot: np.ndarray) -> np.ndarray:
        """
        Compute canonical momentum p = ∂L/∂q̇.
        
        Args:
            q: Coordinates
            q_dot: Velocities
        
        Returns:
            ndarray: Canonical momentum
        """
        return self._partial_L_dqdot_all(q, q_dot)
```

## Checklist for Implementation

- [ ] Module header with article citations
- [ ] CGS units specified
- [ ] Source category documented
- [ ] Lagrangian L = T - V defined
- [ ] Euler-Lagrange equations derived
- [ ] Hamiltonian formulation available
- [ ] Electrokinetic energy included
- [ ] Field-theoretic version (if applicable)
- [ ] Conservation laws verified
- [ ] Theory preservation decorators
- [ ] Maxwell article citations

## Related Templates

- `field-implementation.md` - Field dynamics
- `wave-propagation.md` - Wave energy
- `analytical-solution.md` - Normal modes
- `cross-part-bridge.md` - Multi-system coupling
