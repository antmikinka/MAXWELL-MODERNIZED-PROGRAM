# Template: citation-linking-template

## Purpose

Standardized template for linking citations and references throughout documentation.

## Applicability

Citation management, reference linking, bibliography generation

---

## YAML Frontmatter

```yaml
documentation_type: citation_linking
version: "{{VERSION}}"
generated_date: "{{GENERATED_DATE}}"
citation_style: "{{CITATION_STYLE}}"
maxwell_articles: "{{MAXWELL_ARTICLES}}"
total_citations: {{TOTAL_CITATIONS}}
unique_sources: {{UNIQUE_SOURCES}}
```

---

## LLM Instructions

You are linking citations for the Maxwell Treatise Modernization Project. Follow these guidelines:

1. **Consistent Style**: Use Maxwell treatise citation format consistently
2. **Complete References**: Include all necessary bibliographic information
3. **Bidirectional Links**: Link citations to references and vice versa
4. **CGS Context**: Note CGS unit context where relevant
5. **Theory Classification**: Preserve classification in citations

---

## Template Structure

### Citation Index

```markdown
# Citation Index: {{INDEX_TITLE}}

## Summary

**Total Citations:** {{TOTAL_CITATIONS}}  
**Unique Sources:** {{UNIQUE_SOURCES}}  
**Maxwell Articles:** {{MAXWELL_ARTICLES}}

## Maxwell Treatise Citations

### Standard Format

```
Maxwell, J.C. (1873). A Treatise on Electricity and Magnetism.
  Part {{PART}}, Chapter {{CHAPTER}}, Art. {{ARTICLE_RANGE}}: {{TOPIC}}
```

### All Citations

| Citation ID | Article Range | Topic | First Referenced | Times Cited |
|-------------|---------------|-------|------------------|-------------|
| {{CITATION_ID}} | Art. {{XX}}-{{YY}} | {{TOPIC}} | {{DOCUMENT}} | {{COUNT}} |
```

### Document Citation Map

```markdown
## Document Citation Map

### {{DOCUMENT_NAME}}

**Citations:** {{CITATION_COUNT}}

| Citation | Maxwell Article | Context | Purpose |
|----------|----------------|---------|---------|
| {{CITATION}} | Art. {{XX}} | {{CONTEXT}} | {{PURPOSE}} |

**Reference List:**

1. Maxwell, J.C. (1873). Art. {{XX}}-{{YY}}: {{TOPIC}}
2. ...
```

### Cross-Document Citations

```markdown
## Cross-Document Citation Analysis

### Most Cited Articles

| Rank | Article | Citation Count | Documents |
|------|---------|----------------|-----------|
| 1 | Art. {{XX}}-{{YY}} | {{COUNT}} | {{DOCUMENTS}} |
| 2 | Art. {{XX}}-{{YY}} | {{COUNT}} | {{DOCUMENTS}} |
| 3 | Art. {{XX}}-{{YY}} | {{COUNT}} | {{DOCUMENTS}} |

### Citation Density by Document

| Document | Length (words) | Citations | Density (per 1000) |
|----------|----------------|-----------|-------------------|
| {{DOCUMENT}} | {{LENGTH}} | {{COUNT}} | {{DENSITY}} |
```

### Reference Bibliography

```markdown
## Reference Bibliography

### Primary Sources

1. **Maxwell, J.C. (1873)**
   - Title: A Treatise on Electricity and Magnetism
   - Publisher: Clarendon Press, Oxford
   - Articles: {{ARTICLE_RANGE}}
   - CGS Units: Throughout

### Secondary Sources

1. **{{AUTHOR}} ({{YEAR}})**
   - Title: {{TITLE}}
   - Publication: {{PUBLICATION}}
   - Related Maxwell Articles: {{ARTICLES}}
   - Context: {{CONTEXT}}
```

### Citation Links

```markdown
## Citation Links

### Forward Links (Maxwell -> Modern)

Art. {{XX}}-{{YY}} is referenced in:
- {{DOCUMENT_1}}: {{CONTEXT}}
- {{DOCUMENT_2}}: {{CONTEXT}}

### Backward Links (Modern -> Maxwell)

{{DOCUMENT}} references:
- Art. {{XX}}: {{CONTEXT}}
- Art. {{YY}}: {{CONTEXT}}
```

---

## Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `{{VERSION}}` | Template version | Yes | - |
| `{{GENERATED_DATE}}` | Generation date | Auto | - |
| `{{CITATION_STYLE}}` | Citation format style | Yes | Maxwell |
| `{{MAXWELL_ARTICLES}}` | Article range | Yes | - |
| `{{TOTAL_CITATIONS}}` | Total citation count | Yes | - |
| `{{UNIQUE_SOURCES}}` | Unique source count | Yes | - |
| `{{INDEX_TITLE}}` | Index title | Yes | - |
| `{{CITATION_ID}}` | Citation identifier | Yes | - |
| `{{ARTICLE_RANGE}}` | Article numbers | Yes | - |
| `{{TOPIC}}` | Article topic | Yes | - |
| `{{DOCUMENT}}` | Document name | Yes | - |
| `{{CONTEXT}}` | Citation context | Yes | - |
| `{{PURPOSE}}` | Citation purpose | Yes | - |
| `{{COUNT}}` | Citation count | Yes | - |
| `{{DOCUMENTS}}` | Document list | Conditional | - |
| `{{LENGTH}}` | Document length | Conditional | - |
| `{{DENSITY}}` | Citation density | Conditional | - |
| `{{AUTHOR}}` | Author name | Conditional | - |
| `{{YEAR}}` | Publication year | Conditional | - |
| `{{TITLE}}` | Work title | Conditional | - |
| `{{PUBLICATION}}` | Publication venue | Conditional | - |

---

## Conditional Logic

### Include Citation Map If:

```
IF has_multiple_documents:
  INCLUDE document_citation_map
  SHOW citations per document
ELSE:
  USE single_document_format
```

### Include Cross-Document Analysis If:

```
IF citation_count > 10:
  INCLUDE cross_document_analysis
  SHOW most_cited_articles
  SHOW citation_density
```

### Include Reference Bibliography If:

```
IF has_secondary_sources:
  INCLUDE full_bibliography
  SEPARATE primary and secondary
ELSE:
  INCLUDE maxwell_only_reference
```

---

## Citation Style Guide

### Maxwell Treatise Citation

**Full Format:**
```
Maxwell, J.C. (1873). A Treatise on Electricity and Magnetism 
(3rd ed.). Clarendon Press, Oxford. Part III, Chapter IX, 
Art. 449-474: Magnetic Measurements.
```

**Short Format (in-text):**
```
Maxwell (1873, Art. 449-474)
Maxwell, Art. 449-474
```

### CGS Unit Citation

When citing measurements:
```
All units in CGS system per Maxwell's convention (Art. 1-50).
SI equivalents provided for reference only.
```

---

## Quality Criteria

### Completeness

- [ ] All citations accounted for
- [ ] All references linked
- [ ] Bidirectional links verified
- [ ] No orphaned citations

### Accuracy

- [ ] Article numbers correct
- [ ] Document links valid
- [ ] Contexts accurately described
- [ ] Counts verified

### Consistency

- [ ] Citation style consistent
- [ ] CGS units noted where relevant
- [ ] Theory classification preserved
- [ ] Formatting consistent

---

## Output Format

Citation index should be:
- Markdown format
- Tables for indices
- Hyperlinked references
- Searchable structure
- Export-compatible (BibTeX, etc.)

---

## Related Templates

- `{{api-documentation-template.md}}` - API reference
- `{{tutorial-documentation-template.md}}` - Tutorials
- `{{cross-reference-template.md}}` - Cross-references
