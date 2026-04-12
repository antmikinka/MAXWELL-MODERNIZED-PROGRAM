# Conservation Law Reference

## Purpose

Reference documentation for conservation laws used in validation.

## Energy Conservation

### Electrostatic
```
U = (1/8π) ∫ E² dV = (1/2) ∫ ρV dV
```

### Magnetostatic
```
U = (1/8π) ∫ B·H dV = (1/2) LI²
```

### Time-Varying (Poynting)
```
∂u/∂t + ∇·S = -J·E
u = (1/8π)(E² + B²)
S = (c/4π) E × B
```

## Charge Conservation

### Continuity Equation
```
∂ρ/∂t + ∇·J = 0
```

### Integral Form
```
dQ/dt = -∮ J·dA
```

## Flux Conservation

### Gauss's Law
```
∮ D·dA = 4πQ
```

### No Magnetic Monopoles
```
∮ B·dA = 0
```

## Maxwell Article References

| Law | Articles |
|-----|----------|
| Energy | 85-86, 551, 630-640 |
| Charge | 230-240 |
| Flux | 75-76, 403-404 |
