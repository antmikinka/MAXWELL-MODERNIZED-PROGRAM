# Template: citation-template

## Description

Template for Maxwell article citation decorators.

## Structure

```python
@cite_article(
    [{article_numbers}],
    part='{part}',
    theory_type='{type}',
    note='{note}'
)
def {function_name}(...):
    """
    {docstring}
    
    Maxwell Articles: {article_citation}
    """
```

## LLM Instructions

1. Always include article numbers
2. Specify part (I, II, III, IV)
3. Classify theory type
4. Add note for user theories

## Theory Types

- `maxwell_original` - From Maxwell's text
- `user_original` - User's theory (authoritative)
- `standard_math` - Standard implementation
