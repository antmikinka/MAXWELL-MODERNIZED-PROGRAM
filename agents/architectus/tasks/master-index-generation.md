# Task: Master Index Generation

## Description

Generate a comprehensive article-to-module index covering all 885+ articles across all 6 Parts of Maxwell's Treatise. This task produces the definitive navigation tool for the modernized treatise.

## Workflow

### Step 1: Article Extraction

For each Part:
1. Parse architecture COMPLETE document
2. Extract all article numbers from mapping tables
3. Extract article titles
4. Extract chapter assignments
5. Handle sub-articles (e.g., 74a, 74b, 74c)

### Step 2: Module Mapping

For each article:
1. Extract module path assignment
2. Extract class/function name
3. Extract layer number
4. Verify module exists (if implemented)
5. Record implementation status

### Step 3: Index Compilation

Build unified index:
1. Sort by article number (primary)
2. Sort by Part (secondary)
3. Include chapter information
4. Include layer information
5. Include status indicators

### Step 4: Cross-Reference Generation

Generate cross-references:
1. Module-to-article (reverse index)
2. Layer-to-articles (grouping)
3. Chapter-to-articles (grouping)
4. Topic-based grouping (optional)

### Step 5: Format Generation

Generate multiple formats:
1. Markdown (human-readable)
2. CSV (spreadsheet import)
3. JSON (programmatic access)
4. HTML (web viewing)

### Step 6: Quality Validation

Validate index:
1. Check all articles indexed
2. Verify no duplicates
3. Verify module paths valid
4. Test cross-references
5. Validate format correctness

## Input

- All 6 Architecture COMPLETE documents
- Module registry
- Implementation status database

## Output

### Primary Deliverable

`Maxwell_Treatise_Master_Index.md` containing:
- Complete article index (all 885+ articles)
- Part sections with article ranges
- Module lookup tables
- Status indicators

### Secondary Deliverables

- `Maxwell_Treatise_Master_Index.csv` - Spreadsheet format
- `Maxwell_Treatise_Master_Index.json` - Programmatic format
- `Maxwell_Treatise_Master_Index.html` - Web format
- `reverse_index.md` - Module-to-article index

## Success Criteria

- [ ] All 885+ articles indexed
- [ ] All sub-articles included
- [ ] Module mappings accurate
- [ ] Cross-references valid
- [ ] All formats generated
- [ ] Index is searchable

## Estimated Duration

- Initial generation: 2-4 hours
- Format conversion: 1-2 hours
- Quality validation: 1-2 hours

## Related Commands

- `generate-master-index` - Index generation command
- `audit-coverage` - Coverage verification

## Related Templates

- `master-index.md` - Index template

## Index Structure Example

```markdown
# Maxwell Treatise Master Index

## Part I: Electrostatics (Articles 27-229)

| Article | Chapter | Title | Module | Layer | Status |
|---------|---------|-------|--------|-------|--------|
| 27 | I | Electrification by friction | core/charge.py | 1 | Implemented |
| 28 | I | Electrification by induction | core/charge.py | 1 | Implemented |
| 29 | I | Conduction; conductors | core/materials.py | 1 | Implemented |
| 74a | II | Cavendish modified experiment | tests/verify_cavendish.py | 13 | Implemented |
| 74b | II | Theoretical basis | tests/verify_cavendish.py | 13 | Implemented |
...

## Part II: Electrokinematics (Articles 230-370)
...

## Part III: Magnetism (Articles 371-521)
...

## Part IV: Electromagnetism (Articles 522-710)
...

## Part V: System Core (Articles 711-780)
...

## Part VI: Scalar Physics (Articles 781-866)
...

## Appendices
...
```

## Search Example

```bash
# Find article by number
architectus search-index --article 412

# Find module by article
architectus search-index --article 74a --field module

# Find all articles in layer
architectus search-index --layer 8

# Find all articles about topic
architectus search-index --topic "potential"
```
