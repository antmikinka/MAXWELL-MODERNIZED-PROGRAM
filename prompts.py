"""
Prompt Templates for Maxwell Treatise Processing

This module contains the system and user prompt templates used
for processing each chapter through the AI pipeline.
"""

from typing import List, Dict
from state import ProcessingState


# System prompt - constant across all chapters
SYSTEM_PROMPT = """You are a physics software architect modernizing James Clerk Maxwell's "A Treatise on Electricity and Magnetism" into a Python scientific computing library.

Your task for each chapter is to:

1. **IDENTIFY ARTICLES**: Find all article markers (pattern: XX.] or XX a.]) in the text
2. **MAP TO ARCHITECTURE**: Assign each article to the appropriate Python module/class/function based on the provided architecture specification
3. **EXTRACT EQUATIONS**: Capture important LaTeX equations from each article
4. **TRACK REFERENCES**: Note when articles reference other articles (e.g., "Art. 70", "see Art. 84")
5. **GENERATE STUBS**: Create Python implementation stubs with docstrings citing Maxwell's article

OUTPUT FORMAT:
You MUST respond with valid JSON in this exact structure:

```json
{
  "chapter": "CHAPTER_NAME",
  "chapter_title": "Human readable title",
  "article_range": {"start": "XX", "end": "YY"},
  "articles": [
    {
      "number": "27",
      "sub": null,
      "title": "Electrification by Friction",
      "page": 67,
      "module_path": "maxwell/core/charge.py",
      "implementation_type": "class",
      "implementation_name": "ElectrifiedBody",
      "equations": ["$F = k\\frac{q_1 q_2}{r^2}$"],
      "references": ["100c"],
      "key_concepts": ["vitreous electricity", "resinous electricity"],
      "stub_code": "class ElectrifiedBody:\\n    \\"\\"\\"Art. 27: Electrification by Friction\\n    \\n    Represents a body that exhibits electrical properties.\\n    \\"\\"\\"\\n    \\n    def __init__(self, polarity: str = 'positive'):\\n        self.polarity = polarity"
    }
  ],
  "state_updates": {
    "new_modules": {
      "maxwell/core/charge.py": ["27", "28", "29"]
    },
    "new_classes": {
      "ElectrifiedBody": "maxwell/core/charge.py"
    },
    "new_functions": {
      "induction_charge": "maxwell/core/charge.py"
    },
    "forward_refs": {
      "27": ["100c"]
    },
    "articles_count": 10
  }
}
```

CRITICAL RULES:
- Output ONLY valid JSON, no explanatory text before or after
- Every article must have a module_path from the architecture spec
- Use exact article numbers as they appear (including sub-letters like "85a")
- Extract LaTeX equations exactly as they appear in mathpix_markdown
- Reference article numbers without "Art." prefix in the references array
- Keep stub_code concise (< 20 lines) but include proper docstrings
- If an article is primarily descriptive (no code needed), set implementation_type to "documentation"
"""


def build_system_prompt() -> str:
    """
    Get the system prompt for chapter processing.
    """
    return SYSTEM_PROMPT


def build_chapter_prompt(
    arch_spec: str,
    state: ProcessingState,
    chapter_name: str,
    chapter_text: str,
    article_hints: List[Dict]
) -> str:
    """
    Build the user prompt for processing a specific chapter.
    
    Args:
        arch_spec: The architecture specification (may be compressed)
        state: Current processing state
        chapter_name: Name of the chapter being processed
        chapter_text: Full text of the chapter (mathpix_markdown format)
        article_hints: Pre-extracted article markers from regex
    
    Returns:
        Complete user prompt string
    """
    # Format article hints
    hints_text = format_article_hints(article_hints)
    
    # Get state summary
    state_summary = state.to_summary_string()
    
    # Build the prompt
    prompt = f"""
=== CHAPTER PROCESSING REQUEST ===

CHAPTER: {chapter_name}

{state_summary}

=== ARCHITECTURE SPECIFICATION ===
{arch_spec[:30000] if len(arch_spec) > 30000 else arch_spec}

=== PRE-EXTRACTED ARTICLE HINTS ===
These article markers were found by regex. Use them as a guide:

{hints_text}

=== CHAPTER TEXT (Mathpix Markdown) ===

{chapter_text}

=== END OF CHAPTER TEXT ===

INSTRUCTIONS:
1. Process ALL articles listed in the hints above
2. Map each to the appropriate module from the architecture spec
3. Extract key equations (LaTeX format)
4. Note references to other articles
5. Generate Python stub code for each article's contribution
6. Return results as valid JSON (no markdown code blocks around it)

Remember: Output ONLY the JSON response, nothing else.
"""
    
    return prompt


def format_article_hints(hints: List[Dict]) -> str:
    """
    Format article hints for inclusion in prompt.
    """
    if not hints:
        return "(No article markers detected - please identify articles manually)"
    
    lines = []
    for h in hints:
        art_key = h['article'] + (h['sub'] or '')
        title = h.get('title', '') or '(no title detected)'
        lines.append(f"  Art. {art_key} (page {h['page']}): {title}")
    
    return "\n".join(lines)


def build_compressed_arch_spec(full_spec: str, chapter_num: int) -> str:
    """
    Compress architecture spec to include only relevant layers.
    
    This is useful when the full spec is very large and we need
    to fit within context limits.
    """
    # For now, just truncate if too long
    # TODO: Implement smarter compression that extracts relevant layers
    
    if len(full_spec) <= 50000:
        return full_spec
    
    # Extract key sections
    sections = []
    
    # Always include directory structure
    if "Package Directory Structure" in full_spec:
        start = full_spec.find("Package Directory Structure")
        end = full_spec.find("## **Layer 0", start)
        if end == -1:
            end = start + 5000
        sections.append(full_spec[start:end])
    
    # Include layers 0-4 (core layers) always
    for i in range(5):
        layer_start = full_spec.find(f"## **Layer {i}:")
        if layer_start != -1:
            layer_end = full_spec.find(f"## **Layer {i+1}:", layer_start)
            if layer_end == -1:
                layer_end = layer_start + 3000
            sections.append(full_spec[layer_start:layer_end])
    
    # Include article coverage index if present
    if "Article Coverage Index" in full_spec:
        idx_start = full_spec.find("Article Coverage Index")
        sections.append(full_spec[idx_start:idx_start + 10000])
    
    compressed = "\n\n---\n\n".join(sections)
    
    if len(compressed) > 40000:
        compressed = compressed[:40000] + "\n\n[TRUNCATED - see full spec for details]"
    
    return compressed


# Specialized prompts for different processing modes

def build_equation_extraction_prompt(article_text: str, article_num: str) -> str:
    """
    Build a focused prompt for equation extraction only.
    """
    return f"""
Extract all mathematical equations from Article {article_num} below.

Return a JSON array of equations in LaTeX format:
{{"equations": ["equation1", "equation2", ...]}}

Article text:
{article_text}

Extract equations that are:
- Display equations ($$...$$)
- Inline equations ($...$) that define important relationships
- Numbered equations with \\tag{{}}

Return ONLY the JSON array.
"""


def build_code_generation_prompt(
    article: Dict,
    dependencies: List[str],
    existing_code: str = None
) -> str:
    """
    Build a focused prompt for generating implementation code.
    """
    deps_text = ", ".join(dependencies) if dependencies else "None"
    
    existing_text = ""
    if existing_code:
        existing_text = f"""
EXISTING CODE IN MODULE:
```python
{existing_code}
```
"""
    
    return f"""
Generate Python implementation for Maxwell's Treatise Article {article['number']}.

Article Title: {article.get('title', 'Unknown')}
Module Path: {article['module_path']}
Implementation Type: {article['implementation_type']}
Name: {article['implementation_name']}

Key Equations:
{chr(10).join(article.get('equations', []))}

Dependencies (already defined): {deps_text}
{existing_text}

Generate complete, working Python code that:
1. Implements the physics described in the article
2. Uses NumPy for numerical operations
3. Includes comprehensive docstrings with article citations
4. Follows modern Python conventions (type hints, etc.)
5. Integrates with existing code if provided

Return ONLY the Python code, no explanations.
"""


# Validation prompts

def build_validation_prompt(
    chapter_result: Dict,
    arch_spec: str
) -> str:
    """
    Build a prompt to validate processing results.
    """
    return f"""
Validate the following chapter processing result against the architecture specification.

RESULT:
{json.dumps(chapter_result, indent=2)[:10000]}

ARCHITECTURE SPEC (excerpt):
{arch_spec[:10000]}

Check for:
1. Missing articles (compare article_range with articles list)
2. Incorrect module mappings
3. Missing equations that should have been extracted
4. Invalid Python code in stubs

Return validation results as JSON:
{{
  "valid": true/false,
  "issues": ["issue1", "issue2", ...],
  "suggestions": ["suggestion1", ...]
}}
"""


import json  # Needed for build_validation_prompt
