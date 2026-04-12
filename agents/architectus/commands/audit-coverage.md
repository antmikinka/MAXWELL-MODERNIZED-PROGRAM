# Command: audit-coverage

## Description

Performs comprehensive audit of article coverage across all 6 Parts of Maxwell's Treatise. This command generates detailed reports showing which articles are mapped to modules, identifies gaps in coverage, and provides statistics on implementation progress.

## Usage

```bash
architectus audit-coverage [OPTIONS]

Options:
  --part <PART>           Audit specific part only (I, II, III, IV, V, VI)
  --chapter <CHAPTER>     Audit specific chapter within part
  --detailed              Show detailed article-by-article breakdown
  --gaps-only             Show only unmapped articles
  --output <FORMAT>       Output format: text, json, markdown, csv (default: text)
  --report <PATH>         Write audit report to file
```

## Input

- **Architecture COMPLETE Documents**: All 6 Part architecture maps
- **Maxwell's Treatise Reference**: Original article numbering
- **Module Registry**: Current implementation status

## Coverage Analysis

### 1. Article Count by Part

| Part | Domain | Base Articles | Sub-Articles | Total | Mapped | Coverage |
|------|--------|---------------|--------------|-------|--------|----------|
| I | Electrostatics | 203 | 45 | 248 | TBD | TBD |
| II | Electrokinematics | 141 | 12 | 153 | TBD | TBD |
| III | Magnetism | TBD | TBD | TBD | TBD | TBD |
| IV | Electromagnetism | TBD | TBD | TBD | TBD | TBD |
| V | System Core | TBD | TBD | TBD | TBD | TBD |
| VI | Scalar Physics | TBD | TBD | TBD | TBD | TBD |
| **TOTAL** | | **885+** | | | | |

### 2. Coverage Categories

Articles are categorized as:
- **MAPPED**: Article has valid module assignment
- **UNMAPPED**: Article has no module assignment (gap)
- **IMPLEMENTED**: Module exists and is functional
- **PENDING**: Module mapped but not implemented
- **SUB-ARTICLE**: Article is sub-article (e.g., 74a, 74b)

### 3. Layer Coverage

Coverage is also tracked by layer:
- Layers with 100% coverage
- Layers with partial coverage
- Layers with no coverage

## Output

### Summary Output

```
Article Coverage Audit
======================

Part I: Electrostatics (Layers 0-12)
  Base Articles: 203 (Arts. 27-229)
  Sub-Articles: 45
  Total: 248
  Mapped: 248 (100%)
  Implemented: 180 (72.6%)

Part II: Electrokinematics (Layers 13-30)
  Base Articles: 141 (Arts. 230-370)
  Sub-Articles: 12
  Total: 153
  Mapped: 153 (100%)
  Implemented: 89 (58.2%)

[... Parts III-VI ...]

OVERALL COVERAGE
================
Total Articles: 885+
Mapped: 885+ (100%)
Implemented: 520 (58.7%)
Unmapped: 0 (0%)
```

### Gaps-Only Output

```
Unmapped Articles (Gaps)
========================

Part III: Magnetism
  Article 412: No module assignment
  Article 456a-c: Sub-articles not mapped

Part IV: Electromagnetism
  Article 523: No module assignment
  Article 601-610: Layer 67 module pending

Total Gaps: 12 articles
```

### Detailed Output (CSV Format)

```csv
part,article,chapter,title,module_path,status,layer
I,27,I,Electrification by friction,core/charge.py,implemented,1
I,28,I,Electrification by induction,core/charge.py,implemented,1
I,29,I,Conduction; conductors,core/materials.py,implemented,1
...
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Audit completed, 100% coverage |
| 1 | Audit completed, gaps found |
| 2 | Audit completed, partial coverage |
| 3 | Configuration error (missing files) |

## Examples

```bash
# Full coverage audit
architectus audit-coverage

# Single part audit
architectus audit-coverage --part I

# Show only gaps
architectus audit-coverage --gaps-only

# Generate CSV report
architectus audit-coverage --output csv --report coverage.csv

# Detailed breakdown
architectus audit-coverage --detailed
```

## Related Commands

- `validate-architecture` - Overall architecture validation
- `generate-master-index` - Master article index generation
- `check-dependencies` - Cross-part dependency check

## Integration

### CI/CD Pipeline

```yaml
- name: Article Coverage Audit
  run: architectus audit-coverage --output json --report coverage.json
  continue-on-error: false
  
- name: Check Coverage Threshold
  run: |
    coverage=$(jq '.overall.coverage_percentage' coverage.json)
    if (( $(echo "$coverage < 100" | bc -l) )); then
      echo "Coverage below 100%: $coverage%"
      exit 1
    fi
```

### Dashboard Integration

JSON output format supports dashboard integration:

```json
{
  "timestamp": "2026-04-11T10:30:00Z",
  "overall": {
    "total_articles": 885,
    "mapped": 885,
    "implemented": 520,
    "coverage_percentage": 100.0,
    "implementation_percentage": 58.7
  },
  "by_part": {
    "I": {"total": 248, "mapped": 248, "implemented": 180},
    "II": {"total": 153, "mapped": 153, "implemented": 89},
    ...
  },
  "gaps": []
}
```

## Implementation Notes

This command:
1. Parses all architecture COMPLETE documents
2. Extracts article numbers from mapping tables
3. Validates article numbering sequences
4. Identifies sub-articles (a, b, c suffixes)
5. Cross-references with module registry
6. Generates comprehensive coverage reports

## Sub-Article Handling

Sub-articles are handled specially:
- Format: `{base}{letter}` (e.g., 74a, 74b, 74c)
- Counted separately from base articles
- Must be individually mapped
- Often represent expanded explanations or proofs

## Coverage Thresholds

| Threshold | Status |
|-----------|--------|
| 100% | Complete - all articles mapped |
| 90-99% | Near Complete - minor gaps |
| 75-89% | In Progress - significant work remaining |
| <75% | Early Stage - major gaps |
