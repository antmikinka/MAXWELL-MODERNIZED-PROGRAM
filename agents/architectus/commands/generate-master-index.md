# Command: generate-master-index

## Description

Generates a comprehensive cross-part master index of all articles in Maxwell's Treatise mapped to their modern Python module implementations. This command creates the definitive lookup table for navigating between Maxwell's original text and the modernized codebase.

## Usage

```bash
architectus generate-master-index [OPTIONS]

Options:
  --format <FORMAT>       Output format: markdown, csv, json, html (default: markdown)
  --sort <SORT>           Sort order: article, layer, module (default: article)
  --part <PART>           Generate index for specific part only
  --include-unmapped      Include unmapped articles in output
  --with-chapters         Include chapter information
  --output <PATH>         Write index to file (default: stdout)
```

## Input

- **Architecture COMPLETE Documents**: All 6 Part architecture maps
- **Maxwell's Treatise Reference**: Original article numbering and titles
- **Module Registry**: Current module implementations

## Index Structure

### Master Index Format (Markdown)

```markdown
# Maxwell Treatise Master Index

## Part I: Electrostatics (Articles 27-229)

| Article | Chapter | Title | Module Path | Layer | Status |
|---------|---------|-------|-------------|-------|--------|
| 27 | I | Electrification by friction | maxwell/core/charge.py | 1 | Implemented |
| 28 | I | Electrification by induction | maxwell/core/charge.py | 1 | Implemented |
| 29 | I | Conduction; conductors | maxwell/core/materials.py | 1 | Implemented |
| ... | ... | ... | ... | ... | ... |

## Part II: Electrokinematics (Articles 230-370)
...
```

### Index Format (CSV)

```csv
part,article,chapter,title,module_path,layer,status
I,27,I,Electrification by friction,maxwell/core/charge.py,1,implemented
I,28,I,Electrification by induction,maxwell/core/charge.py,1,implemented
I,29,I,Conduction; conductors,maxwell/core/materials.py,1,implemented
```

### Index Format (JSON)

```json
{
  "generated": "2026-04-11T10:30:00Z",
  "total_articles": 885,
  "parts": {
    "I": {
      "domain": "Electrostatics",
      "layers": [0, 12],
      "articles": [
        {
          "article": "27",
          "chapter": "I",
          "title": "Electrification by friction",
          "module": "maxwell/core/charge.py",
          "layer": 1,
          "status": "implemented"
        }
      ]
    }
  }
}
```

## Index Sections

### 1. Article-to-Module Index

Primary index mapping each article to its module:
- Article number (including sub-articles)
- Chapter number
- Article title (abbreviated)
- Module path
- Layer number
- Implementation status

### 2. Module-to-Article Index

Reverse index mapping each module to its articles:
- Module path
- Articles covered
- Layer number
- Part domain

### 3. Layer Index

Articles grouped by layer:
- Layer number
- Layer name/description
- Articles in layer
- Module count

### 4. Chapter Index

Articles grouped by chapter:
- Part number
- Chapter number
- Chapter title
- Article range
- Module summary

## Output

### Summary Statistics

```
Master Index Generation Complete
================================

Total Articles Indexed: 885
Total Modules: 250+
Parts Covered: 6
Layers: 0-97

By Status:
  Implemented: 520 (58.7%)
  Mapped: 365 (41.3%)
  Unmapped: 0 (0%)

Index Files Generated:
  - Maxwell_Treatise_Master_Index.md
  - Maxwell_Treatise_Master_Index.csv
  - Maxwell_Treatise_Master_Index.json
```

### Sample Index Entry

```markdown
### Article 412

**Title:** Magnetic Potential of Solenoid  
**Part:** III (Magnetism)  
**Chapter:** VIII  
**Layer:** 35  
**Module:** `maxwell/magnetics/potential.py`  
**Class/Function:** `calc_solenoid_potential()`  
**Status:** Implemented  
**Dependencies:** 
  - Part I: Article 70 (Electric potential)
  - Part II: Article 339 (Current sheet)
**Tests:** `tests/magnetics/test_solenoid_potential.py`
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Index generated successfully |
| 1 | Index generated with warnings (unmapped articles) |
| 2 | Index generation failed (missing data) |
| 3 | Configuration error (missing files) |

## Examples

```bash
# Generate all formats
architectus generate-master-index --output master_index/

# Generate CSV only
architectus generate-master-index --format csv --output articles.csv

# Sort by module
architectus generate-master-index --sort module --output by_module.md

# Include chapter info
architectus generate-master-index --with-chapters --output detailed_index.md

# Single part index
architectus generate-master-index --part I --output part_i_index.md
```

## Related Commands

- `audit-coverage` - Article coverage audit
- `validate-architecture` - Architecture validation
- `review-layer-mapping` - Layer mapping review

## Integration

### Documentation Build

```yaml
- name: Generate Master Index
  run: architectus generate-master-index --format markdown --output docs/index.md
  
- name: Deploy Index
  run: |
    cp docs/index.md docs/site/reference/article-index.md
```

### IDE Integration

JSON format supports IDE integration:

```json
// .vscode/settings.json
{
  "maxwellTreatise.indexPath": "./maxwell_treatise_index.json",
  "maxwellTreatise.enableArticleLinks": true
}
```

### Search Index

The generated index can be used for documentation search:

```bash
# Search for articles about "potential"
architectus search-index "potential"
```

## Implementation Notes

This command:
1. Parses all architecture COMPLETE documents
2. Extracts all article mappings
3. Normalizes article numbers
4. Cross-references with module registry
5. Generates multiple output formats
6. Includes cross-references and dependencies

## Sub-Article Handling

Sub-articles are indexed with their parent:

```markdown
| Article | Title | Module |
|---------|-------|--------|
| 74 | Theory of inverse square | tests/verification/verify_cavendish.py |
| 74a | Modified experiment | tests/verification/verify_cavendish.py |
| 74b | Theoretical basis | tests/verification/verify_cavendish.py |
| 74c | Numerical calculation | tests/verification/verify_cavendish.py |
| 74d | Practical application | tests/verification/verify_cavendish.py |
| 74e | Conclusion | tests/verification/verify_cavendish.py |
```

## Index Maintenance

The master index should be regenerated:
- After any architecture change
- Before each release
- When new modules are implemented
- When article mappings are updated

## Cross-Reference Format

Index entries include cross-references:

```markdown
**See Also:**
- Article 70: Electric potential (Part I, Layer 2)
- Article 339: Current sheet (Part II, Layer 21)
- Article 412: Magnetic potential (Part III, Layer 35)
```
