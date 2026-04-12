# Template: coordinate-transformation

## Description

Template for implementing coordinate transformations between Cartesian, cylindrical, and spherical systems. This template ensures consistent handling of vector and tensor transformations.

## Structure

```python
"""
Coordinate Transformation: {from_coords} to {to_coords}

Maxwell Articles: {article_citations}
"""

## Transformation Definition

### Source Coordinates
{source_coordinate_definition}

### Target Coordinates
{target_coordinate_definition}

### Transformation Equations
{coordinate_mapping_equations}

### Jacobian Matrix
{jacobian_matrix}

### Scale Factors
{metric_scale_factors}

## Vector Transformation

### Component Transformation
{how_vector_components_transform}

### Basis Vector Transformation
{how_basis_vectors_transform}

## Differential Operator Transformation

### Gradient
{gradient_in_new_coordinates}

### Divergence
{divergence_in_new_coordinates}

### Curl
{curl_in_new_coordinates}

### Laplacian
{laplacian_in_new_coordinates}

## Implementation

```python
@cite_article([{articles}])
def transform_{from}_to_{to}(
    field: {field_type},
    coordinates: np.ndarray
) -> {return_type}:
    """
    Transform field from {from_coords} to {to_coords}.
    
    Parameters
    ----------
    field : {field_type}
        Field in {from_coords} coordinates
    coordinates : np.ndarray
        Coordinate values in {to_coords}
    
    Returns
    -------
    {return_type}
        Transformed field in {to_coords}
    """
    {implementation}
```

## Verification

- [ ] Jacobian determinant computed correctly
- [ ] Inverse transformation verified
- [ ] Vector magnitude preserved
- [ ] Differential operators give consistent results

## Maxwell Article References
{relevant_articles}
```

## LLM Instructions

When using this template:

1. **Define Both Systems**: Clearly specify source and target
2. **Jacobian**: Always compute and verify Jacobian
3. **Scale Factors**: Include metric scale factors
4. **Operator Forms**: Show all differential operators
5. **Verify**: Test inverse transformation

## Variables

- `{from_coords}`: Source coordinate system
- `{to_coords}`: Target coordinate system
- `{article_citations}`: Maxwell article citations
- `{source_coordinate_definition}`: Source system definition
- `{target_coordinate_definition}`: Target system definition
- `{coordinate_mapping_equations}`: Transformation equations
- `{jacobian_matrix}`: Jacobian matrix
- `{metric_scale_factors}`: Scale factors (h_r, h_θ, h_φ)
- `{how_vector_components_transform}`: Vector transformation rules
- `{how_basis_vectors_transform}`: Basis transformation
- All differential operator expressions
- `{implementation}`: Python code
- `{relevant_articles}`: Article references

## Conditional Logic

IF transformation involves spherical coordinates:
  INCLUDE singularity handling at poles
  DOCUMENT branch cut for φ

IF transformation is for tensor fields:
  INCLUDE rank-2 transformation rules
  SHOW index notation form

## Example Usage

```markdown
## Transformation Equations
Cartesian to Spherical:
x = r sin θ cos φ
y = r sin θ sin φ
z = r cos θ

## Scale Factors
h_r = 1, h_θ = r, h_φ = r sin θ

## Gradient in Spherical
∇φ = (∂φ/∂r) r̂ + (1/r)(∂φ/∂θ) θ̂ + (1/(r sin θ))(∂φ/∂φ) φ̂
```
