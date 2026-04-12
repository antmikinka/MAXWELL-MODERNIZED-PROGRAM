# **Maxwell's Treatise: Modernized Architecture Map**

## **Part V: System Core & Infrastructure — COMPLETE EDITION**

> **Status:** COMPLETE | **Date:** 2026-04-11 | **Version:** 1.0
> **Source:** Maxwell, J.C. *A Treatise on Electricity and Magnetism*, Part V (System Core)
> **Coverage:** Meta-layer | 5 Layers (90–94) | 10+ Modules

---

## **Executive Summary**

| Metric | Value |
|--------|-------|
| **Articles** | N/A (Meta-layer, cross-cutting concerns) |
| **Chapters** | N/A (Infrastructure layer) |
| **Layers** | 5 (Layers 90–94) |
| **Modules** | 10+ |
| **Packages** | 6 (core/space, math/coords, sim, config, meta) |
| **Cross-part Dependencies** | Parts I–IV (all domain layers) |

### Part V Scope

Part V provides the **infrastructure layer** that unifies Parts I–IV into a single executable simulation framework. Unlike the physics-specific layers, Part V handles:

- **Space discretization** — Mesh/voxel grid for field storage
- **Coordinate transformations** — Cartesian, spherical, ellipsoidal switching
- **Time integration** — Numerical stepping for dynamic problems
- **Universal constants** — Single source of truth for $\epsilon_0$, $\mu_0$, $c$
- **Citation tracking** — Linking every function back to Maxwell's article numbers

This layer is essential for transforming the theoretical mappings of Parts I–IV into an executable, testable software library.

### Layer Numbering

| Layer Range | Part | Domain |
|-------------|------|--------|
| 0–12 | Part I | Electrostatics |
| 13–30 | Part II | Electrokinematics |
| 30b–42 | Part III | Magnetism |
| 43–86 | Part IV | Electromagnetism |
| **90–94** | **Part V** | **System Core** |
| 95–97 | Part VI | Scalar Physics |

---

## **Package Directory Structure**

```
maxwell/
├── core/
│   ├── __init__.py
│   └── space/                       # [Part V, Layer 90] Simulation medium
│       ├── __init__.py
│       ├── mesh.py                  # EtherGrid — 3D voxel field storage
│       ├── medium.py                # MediumProperties — μ, ε, σ maps
│       └── boundary.py              # BoundaryManager — Dirichlet/Neumann
│
├── math/
│   └── coords/                      # [Part V, Layer 91] Coordinate engine
│       ├── __init__.py
│       ├── transform.py             # CoordinateSystem — Jacobians, metrics
│       └── operators.py             # VectorOperators — ∇ in all coords
│
├── sim/                             # [Part V, Layer 92] Time integration
│   ├── __init__.py
│   ├── time_stepper.py              # RungeKutta4 — State advancement
│   └── events.py                    # EventQueue — Discrete events
│
├── config/                          # [Part V, Layer 93] Constants & precision
│   ├── __init__.py
│   ├── constants.py                 # UniversalConstants — c, ε₀, μ₀
│   └── precision.py                 # SimulationConfig — Tolerances
│
└── meta/                            # [Part V, Layer 94] Citation tracking
    ├── __init__.py
    ├── citation.py                  # @maxwell_cite decorator
    └── explorer.py                  # get_theory_text() — In-app docs
```

---

## **Layer 90: The Simulation Kernel (The "Ether")**

**Source:** Cross-cutting (Ether medium concept from Parts I, III, IV)
**Goal:** Defining the "Medium" in which all fields exist. Manages discretization of space.

| Module Path | Class/Function | Responsibility | Cross-Reference |
|-------------|----------------|----------------|-----------------|
| `maxwell/core/space/mesh.py` | `EtherGrid` | 3D voxel grid storing $\mathfrak{E}, \mathfrak{B}, \mathfrak{A}$ at every coordinate | All Parts: Container for all fields |
| `maxwell/core/space/medium.py` | `MediumProperties` | Spatial map of constitutive properties ($\mu, \epsilon, \sigma$) defining matter vs vacuum | Part II (Ch. IX): Heterogeneous media |
| `maxwell/core/space/boundary.py` | `BoundaryManager` | Enforces edge conditions (Dirichlet/Neumann) at simulation limits | Part I (Ch. IV): Green's theorem |

### Implementation Details

```python
# maxwell/core/space/mesh.py

class EtherGrid:
    """
    3D voxel grid for electromagnetic field storage.
    
    Stores field vectors (E, B, A) and scalar potentials (V, Ω) 
    at discrete spatial coordinates.
    
    Attributes:
        shape: Tuple[int, int, int] — (nx, ny, nz) grid dimensions
        extent: Tuple[float, float, float] — Physical size (Lx, Ly, Lz)
        dtype: Data type for field values (float64 recommended)
    """
    
    def __init__(self, shape: Tuple[int], extent: Tuple[float]):
        self.shape = shape
        self.extent = extent
        self.dx = extent[0] / shape[0]  # Grid spacing
        
    def store_field(self, field_name: str, data: np.ndarray):
        """Store a field component in the grid."""
        ...
        
    def interpolate(self, field_name: str, position: np.ndarray) -> float:
        """Interpolate field value at arbitrary position."""
        ...
```

---

## **Layer 91: The Coordinate Engine (The "Transformer")**

**Source:** Cross-cutting (Coordinate switching from Parts I, III)
**Goal:** Maxwell fluently switches between Cartesian, Spherical, and Ellipsoidal coordinates.

| Module Path | Class/Function | Responsibility | Cross-Reference |
|-------------|----------------|----------------|-----------------|
| `maxwell/math/coords/transform.py` | `CoordinateSystem` | Base class for coordinate transforms (Jacobians, metrics) | Part III (Ch. X): Confocal surfaces |
| `maxwell/math/coords/operators.py` | `VectorOperators` | Implementation of $\nabla$ (Grad, Div, Curl, Laplacian) for active coordinate system | Part IV (Ch. IX): General equations |

### Implementation Details

```python
# maxwell/math/coords/transform.py

from enum import Enum
from dataclasses import dataclass
import numpy as np

class CoordinateType(Enum):
    CARTESIAN = "cartesian"
    SPHERICAL = "spherical"
    ELLIPSOIDAL = "ellipsoidal"
    CYLINDRICAL = "cylindrical"

@dataclass
class CoordinateTransform:
    """Base class for coordinate transformations."""
    
    source: CoordinateType
    target: CoordinateType
    
    def jacobian(self, coords: np.ndarray) -> np.ndarray:
        """Compute Jacobian matrix of the transformation."""
        raise NotImplementedError
        
    def metric_factors(self, coords: np.ndarray) -> np.ndarray:
        """Compute scale factors (h1, h2, h3) for curvilinear coords."""
        raise NotImplementedError


class SphericalTransform(CoordinateTransform):
    """Cartesian ↔ Spherical coordinate transformation."""
    
    def __init__(self):
        super().__init__(CoordinateType.CARTESIAN, CoordinateType.SPHERICAL)
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """(x, y, z) → (r, θ, φ)"""
        x, y, z = x
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arccos(z / r)
        phi = np.arctan2(y, x)
        return np.array([r, theta, phi])
    
    def metric_factors(self, coords: np.ndarray) -> np.ndarray:
        """Scale factors: h_r=1, h_θ=r, h_φ=r sin θ"""
        r, theta, phi = coords
        return np.array([1, r, r * np.sin(theta)])
```

```python
# maxwell/math/coords/operators.py

class VectorOperators:
    """
    Vector calculus operators in arbitrary coordinate systems.
    
    Uses metric factors from CoordinateTransform for curvilinear coords.
    """
    
    def __init__(self, coord_system: CoordinateTransform):
        self.coord_system = coord_system
    
    def grad(self, scalar_field: np.ndarray, coords: np.ndarray) -> np.ndarray:
        """Compute gradient of scalar field in active coordinates."""
        h = self.coord_system.metric_factors(coords)
        # ∇f = (1/h₁)∂f/∂q₁ ê₁ + (1/h₂)∂f/∂q₂ ê₂ + (1/h₃)∂f/∂q₃ ê₃
        ...
    
    def div(self, vector_field: np.ndarray, coords: np.ndarray) -> np.ndarray:
        """Compute divergence of vector field."""
        # ∇·F = (1/h₁h₂h₃)[∂(h₂h₃F₁)/∂q₁ + ∂(h₁h₃F₂)/∂q₂ + ∂(h₁h₂F₃)/∂q₃]
        ...
    
    def curl(self, vector_field: np.ndarray, coords: np.ndarray) -> np.ndarray:
        """Compute curl of vector field."""
        # ∇×F = determinant form with scale factors
        ...
    
    def laplacian(self, scalar_field: np.ndarray, coords: np.ndarray) -> np.ndarray:
        """Compute Laplacian of scalar field."""
        # ∇²f = ∇·(∇f)
        ...
```

---

## **Layer 92: The Time Integrator (The "Clock")**

**Source:** Part II (Current dynamics), Part IV (Field evolution)
**Goal:** Central clock and integration strategy to advance the simulation.

| Module Path | Class/Function | Responsibility | Cross-Reference |
|-------------|----------------|----------------|-----------------|
| `maxwell/sim/time_stepper.py` | `RungeKutta4` | Numerical integrator to advance state ($t \rightarrow t + dt$) | Part IV (Ch. VI): Dynamical theory |
| `maxwell/sim/events.py` | `EventQueue` | Handles discrete events (switch closing, spark discharge) within continuous time | Part II (Ch. IV): Self-induction sparks |

### Implementation Details

```python
# maxwell/sim/time_stepper.py

from typing import Callable, Tuple
import numpy as np

class RungeKutta4:
    """
    4th-order Runge-Kutta time integrator.
    
    Advances system state using:
    y_{n+1} = y_n + (h/6)(k1 + 2k2 + 2k3 + k4)
    
    Suitable for Maxwell's dynamical equations (Part IV, Ch. VI).
    """
    
    def __init__(self, dt: float):
        self.dt = dt  # Time step
    
    def step(self, 
             state: np.ndarray, 
             t: float, 
             derivative_fn: Callable[[np.ndarray, float], np.ndarray]
             ) -> Tuple[np.ndarray, float]:
        """
        Advance state by one time step.
        
        Args:
            state: Current system state vector
            t: Current time
            derivative_fn: Function computing dy/dt = f(y, t)
        
        Returns:
            (new_state, new_time)
        """
        h = self.dt
        k1 = derivative_fn(state, t)
        k2 = derivative_fn(state + h*k1/2, t + h/2)
        k3 = derivative_fn(state + h*k2/2, t + h/2)
        k4 = derivative_fn(state + h*k3, t + h)
        
        new_state = state + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
        new_time = t + h
        
        return new_state, new_time


class AdaptiveTimeStepper:
    """Time stepper with adaptive step size control."""
    
    def __init__(self, initial_dt: float, tolerance: float = 1e-6):
        self.initial_dt = initial_dt
        self.tolerance = tolerance
    
    def step_with_error_control(self, state, t, derivative_fn):
        """Adjust dt to maintain error bounds."""
        ...
```

```python
# maxwell/sim/events.py

import heapq
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
import numpy as np

@dataclass(order=True)
class ScheduledEvent:
    """An event scheduled for a specific simulation time."""
    time: float
    priority: int = field(compare=False, default=0)
    callback: Callable = field(compare=False, default=None)
    args: tuple = field(compare=False, default=None)
    kwargs: dict = field(compare=False, default=None)


class EventQueue:
    """
    Priority queue for discrete events in continuous-time simulation.
    
    Handles events like:
    - Switch closing/opening
    - Spark discharge
    - Battery connection/disconnection
    - Measurement sampling
    """
    
    def __init__(self):
        self._queue = []
        self._current_time = 0.0
    
    def schedule(self, 
                 time: float, 
                 callback: Callable, 
                 args: tuple = None, 
                 priority: int = 0):
        """Schedule an event for future execution."""
        event = ScheduledEvent(
            time=time,
            priority=priority,
            callback=callback,
            args=args or (),
            kwargs={}
        )
        heapq.heappush(self._queue, event)
    
    def process_due_events(self, current_time: float):
        """Execute all events scheduled for current_time or earlier."""
        self._current_time = current_time
        while self._queue and self._queue[0].time <= current_time:
            event = heapq.heappop(self._queue)
            event.callback(*event.args, **event.kwargs)
    
    def next_event_time(self) -> Optional[float]:
        """Return time of next scheduled event, or None if queue empty."""
        return self._queue[0].time if self._queue else None
```

---

## **Layer 93: Global Constants & Units Registry (The "Standard")**

**Source:** Parts I, II, IV (Unit systems and constants)
**Goal:** Preventing "Magic Numbers." Ensuring $\epsilon_0, \mu_0, c$ are consistent across all parts.

| Module Path | Class/Function | Responsibility | Cross-Reference |
|-------------|----------------|----------------|-----------------|
| `maxwell/config/constants.py` | `UniversalConstants` | Single source of truth for $c$ (speed of light) and conversion factors | Part IV (Ch. XIX): Ratio of units |
| `maxwell/config/precision.py` | `SimulationConfig` | Controls floating-point precision (float64 vs float32) and error tolerances | Global |

### Implementation Details

```python
# maxwell/config/constants.py

from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class UniversalConstants:
    """
    Universal physical constants used throughout Maxwell's Treatise.
    
    All values in CGS Gaussian units (as used by Maxwell).
    """
    
    # Speed of light in vacuum (cm/s)
    C: float = 2.99792458e10
    
    # Note: In Gaussian units, ε₀ and μ₀ are dimensionless and equal to 1
    # They appear explicitly only in SI units
    
    # Electron charge (esu)
    E_CHARGE: float = 4.8032047e-10
    
    # Electron mass (g)
    E_MASS: float = 9.1093837e-28
    
    # Conversion factors
    ESU_TO_EMU_FACTOR: float = C  # Ratio of electrostatic to electromagnetic units
    
    @classmethod
    def si_constants(cls) -> Dict[str, float]:
        """Return SI unit constants for comparison."""
        return {
            'epsilon_0': 8.854187817e-12,  # F/m
            'mu_0': 4 * np.pi * 1e-7,  # H/m
            'c': 299792458.0,  # m/s
        }


# Convenience imports
CONST = UniversalConstants()
```

```python
# maxwell/config/precision.py

from dataclasses import dataclass
from typing import Literal

@dataclass
class SimulationConfig:
    """
    Global configuration for simulation precision and tolerances.
    
    Attributes:
        dtype: Default floating-point type (float64 for accuracy, float32 for speed)
        convergence_tolerance: Tolerance for iterative solvers
        max_iterations: Maximum iterations for iterative methods
        zero_threshold: Values below this are treated as zero
    """
    
    dtype: Literal['float32', 'float64'] = 'float64'
    convergence_tolerance: float = 1e-10
    max_iterations: int = 1000
    zero_threshold: float = 1e-15
    
    def get_dtype(self) -> type:
        """Return numpy dtype object."""
        import numpy as np
        return np.float64 if self.dtype == 'float64' else np.float32
    
    def is_zero(self, value: float) -> bool:
        """Check if value should be treated as zero."""
        return abs(value) < self.zero_threshold


# Global configuration instance
CONFIG = SimulationConfig()
```

---

## **Layer 94: The Treatise Meta-Link (The "Citation")**

**Source:** Global (Documentation linkage)
**Goal:** Linking every executed function back to the specific Article in Maxwell's text.

| Module Path | Class/Function | Responsibility | Cross-Reference |
|-------------|----------------|----------------|-----------------|
| `maxwell/meta/citation.py` | `@maxwell_cite(art_id)` | Decorator that tags Python functions with their source Article ID | Global |
| `maxwell/meta/explorer.py` | `get_theory_text(art_id)` | Returns original Maxwell text for a given simulation module (in-app documentation) | Global |

### Implementation Details

```python
# maxwell/meta/citation.py

from functools import wraps
from typing import Optional, List
import inspect

class MaxwellCitation:
    """Metadata container for a Maxwell article citation."""
    
    def __init__(self, 
                 article_id: int,
                 part: str,
                 chapter: Optional[str] = None,
                 notes: Optional[str] = None):
        self.article_id = article_id
        self.part = part
        self.chapter = chapter
        self.notes = notes
    
    def __repr__(self):
        return f"Art. {self.article_id} (Part {self.part})"


def maxwell_cite(article_id: int, 
                 part: str = None, 
                 chapter: str = None,
                 notes: str = None):
    """
    Decorator to tag functions with their Maxwell article source.
    
    Usage:
        @maxwell_cite(art_id=77, part="I", chapter="II", notes="Poisson's equation")
        def solve_poisson(rho, V):
            ...
    
    The citation is stored in function metadata for documentation generation.
    """
    def decorator(func):
        citation = MaxwellCitation(
            article_id=article_id,
            part=part,
            chapter=chapter,
            notes=notes
        )
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Attach citation to function metadata
        wrapper._maxwell_citation = citation
        
        return wrapper
    return decorator


def get_citation(func) -> Optional[MaxwellCitation]:
    """Retrieve Maxwell citation from a decorated function."""
    return getattr(func, '_maxwell_citation', None)
```

```python
# maxwell/meta/explorer.py

"""
Maxwell Treatise Explorer — In-app documentation system.

Provides programmatic access to Maxwell's original text,
linked to the corresponding Python implementations.
"""

import json
from pathlib import Path
from typing import Optional, Dict, List

class MaxwellTreatiseExplorer:
    """
    Search and retrieval interface for Maxwell's Treatise text.
    
    Loads article text from JSON index and provides lookup by:
    - Article number
    - Part/Chapter
    - Keyword search
    """
    
    def __init__(self, treatise_path: str = None):
        self.treatise_path = treatise_path or self._default_path()
        self._index: Dict[int, dict] = None
    
    def _default_path(self) -> str:
        """Default location of treatise JSON index."""
        return Path(__file__).parent.parent / "docs" / "treatise_index.json"
    
    def _load_index(self):
        """Load article index from JSON file."""
        if self._index is None:
            with open(self.treatise_path, 'r') as f:
                self._index = json.load(f)
    
    def get_article_text(self, article_id: int) -> Optional[str]:
        """
        Retrieve original Maxwell text for a specific article.
        
        Args:
            article_id: Article number (e.g., 77 for Poisson's equation)
        
        Returns:
            Full article text including equations (as LaTeX)
        """
        self._load_index()
        article = self._index.get(str(article_id))
        if article:
            return article.get('text', '')
        return None
    
    def get_article_metadata(self, article_id: int) -> Optional[dict]:
        """Get article metadata (part, chapter, page, title)."""
        self._load_index()
        return self._index.get(str(article_id))
    
    def search_by_keyword(self, keyword: str) -> List[dict]:
        """Search all articles for a keyword."""
        self._load_index()
        results = []
        for art_id, article in self._index.items():
            if keyword.lower() in article.get('text', '').lower():
                results.append({
                    'article_id': int(art_id),
                    'title': article.get('title'),
                    'snippet': article.get('text', '')[:200] + '...'
                })
        return results
    
    def get_module_documentation(self, func) -> str:
        """
        Generate documentation string for a function, including Maxwell citation.
        
        Combines Python docstring with original Maxwell text.
        """
        from .citation import get_citation
        
        citation = get_citation(func)
        doc = []
        
        # Python docstring
        if func.__doc__:
            doc.append(f"Implementation:\n{func.__doc__}\n")
        
        # Maxwell citation
        if citation:
            article_text = self.get_article_text(citation.article_id)
            if article_text:
                doc.append(f"\n---\n")
                doc.append(f"**Source: Maxwell, Part {citation.part}, Article {citation.article_id}**\n")
                doc.append(f"{article_text}")
        
        return '\n'.join(doc)


# Global explorer instance
EXPLORER = MaxwellTreatiseExplorer()

def get_theory_text(article_id: int) -> Optional[str]:
    """Convenience function to get Maxwell text for an article."""
    return EXPLORER.get_article_text(article_id)
```

---

## **Article Coverage Index**

### Part V: Infrastructure Modules

Since Part V is a meta-layer providing cross-cutting infrastructure, it does not map to specific Maxwell articles. Instead, it provides foundational support for all physics modules in Parts I–IV.

| Module | Purpose | Supports |
|--------|---------|----------|
| `maxwell/core/space/mesh.py` | Field storage grid | All field simulations |
| `maxwell/core/space/medium.py` | Material property maps | Heterogeneous media (Part II, Ch. IX) |
| `maxwell/core/space/boundary.py` | Boundary condition enforcement | Green's theorem (Part I, Ch. IV) |
| `maxwell/math/coords/transform.py` | Coordinate transformations | Spherical harmonics (Part I, Ch. IX), Ellipsoids (Part III, Ch. V) |
| `maxwell/math/coords/operators.py` | Vector calculus operators | All differential equations |
| `maxwell/sim/time_stepper.py` | Time integration | Dynamical theory (Part IV, Ch. VI) |
| `maxwell/sim/events.py` | Discrete event handling | Circuit switching, sparks (Part II, Ch. IV) |
| `maxwell/config/constants.py` | Universal constants | Unit conversions (Part II, Ch. XI), EM wave speed (Part IV, Ch. XIX) |
| `maxwell/config/precision.py` | Numerical tolerances | All numerical solvers |
| `maxwell/meta/citation.py` | Article citation decorator | Documentation linkage |
| `maxwell/meta/explorer.py` | In-app documentation | User reference |

---

## **Implementation Priority Matrix**

### Phase 1: Foundation (P0 — Critical)

| Layer | Priority | Modules | Rationale |
|-------|----------|---------|-----------|
| 90 | P0 | `mesh.py`, `medium.py` | Space discretization is prerequisite for all simulation |
| 93 | P0 | `constants.py` | Unit consistency is critical for cross-part validation |

### Phase 2: Core Infrastructure (P1 — High)

| Layer | Priority | Modules | Rationale |
|-------|----------|---------|-----------|
| 91 | P1 | `transform.py`, `operators.py` | Coordinate switching needed for spherical/ellipsoidal problems |
| 92 | P1 | `time_stepper.py` | Time dynamics required for Part IV electromagnetic waves |

### Phase 3: Developer Tools (P2 — Medium)

| Layer | Priority | Modules | Rationale |
|-------|----------|---------|-----------|
| 94 | P2 | `citation.py`, `explorer.py` | Documentation linkage — valuable but not blocking |

---

## **Validation Checklist**

- [ ] All 5 layers (90–94) have module definitions
- [ ] Space mesh supports field storage for E, B, A vectors
- [ ] Coordinate system supports Cartesian, spherical, ellipsoidal
- [ ] Vector operators (grad, div, curl, laplacian) work in all coordinate systems
- [ ] Time stepper supports RK4 integration
- [ ] Universal constants are defined once and imported everywhere
- [ ] Citation decorator can tag any function with article ID
- [ ] Explorer can retrieve original Maxwell text for any module
- [ ] Boundary manager supports Dirichlet and Neumann conditions
- [ ] Medium properties support anisotropic materials (tensor μ, ε)
- [ ] Event queue handles concurrent events with priority ordering

---

## **Version History**

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-11 | Initial COMPLETE architecture map. 5 layers (90–94), 10+ modules, cross-cutting infrastructure for Parts I–IV integration. |

---

**END OF PART V DOCUMENT**
