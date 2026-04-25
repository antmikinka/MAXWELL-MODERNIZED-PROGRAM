# Template: cross-reference-template

## Purpose

Standardized template for generating cross-references and citation links.

## Applicability

Document cross-references, Maxwell article indices, citation networks

---

## YAML Frontmatter

```yaml
documentation_type: cross_reference
version: "{{VERSION}}"
generated_date: "{{GENERATED_DATE}}"
reference_type: "{{REFERENCE_TYPE}}"
maxwell_articles: "{{MAXWELL_ARTICLES}}"
linked_documents:
  {{LINKED_DOCUMENTS}}
cgs_units_referenced: {{CGS_UNITS}}
```

---

## LLM Instructions

You are generating cross-references for the Maxwell Treatise Modernization Project. Follow these guidelines:

1. **Accurate Citations**: Verify all Maxwell article numbers against source text
2. **Bidirectional Links**: Create forward and backward references
3. **Context Preservation**: Include brief context for each reference
4. **CGS Unit Consistency**: Note CGS unit usage in referenced sections
5. **Theory Classification**: Distinguish between maxwell_original, user_original, standard_math

---

## Template Structure

### Cross-Reference Index

```markdown
# Cross-Reference: {{REFERENCE_TITLE}}

## Overview

{{REFERENCE_OVERVIEW}}

**Reference Type:** {{REFERENCE_TYPE}}  
**Maxwell Articles:** {{MAXWELL_ARTICLES}}

## Article Index

### Part I: Electrostatics (Art. 1-229)

| Article | Topic | Referenced In | Context |
|---------|-------|---------------|---------|
| Art. {{XX}} | {{TOPIC}} | {{DOCUMENT}} | {{CONTEXT}} |

### Part II: Electrokinematics (Art. 230-370)

| Article | Topic | Referenced In | Context |
|---------|-------|---------------|---------|
| Art. {{XX}} | {{TOPIC}} | {{DOCUMENT}} | {{CONTEXT}} |

### Part III: Magnetism (Art. 371-474)

| Article | Topic | Referenced In | Context |
|---------|-------|---------------|---------|
| Art. {{XX}} | {{TOPIC}} | {{DOCUMENT}} | {{CONTEXT}} |

### Part IV: Electromagnetism (Art. 475-866)

| Article | Topic | Referenced In | Context |
|---------|-------|---------------|---------|
| Art. {{XX}} | {{TOPIC}} | {{DOCUMENT}} | {{CONTEXT}} |
```

### Document Cross-References

```markdown
## Document Index

### {{DOCUMENT_NAME}}

**Location:** `{{FILE_PATH}}`

**Maxwell Articles Cited:**

| Article | Citation Context | Page/Section |
|---------|-----------------|--------------|
| Art. {{XX}} | {{CONTEXT}} | {{LOCATION}} |

**Related Documents:**

- {{RELATED_DOCUMENT_1}}
- {{RELATED_DOCUMENT_2}}
```

### Topic Cross-References

```markdown
## Topic Index

### {{TOPIC_NAME}}

**Definition:** {{TOPIC_DEFINITION}}

**Maxwell Articles:**

- Art. {{XX}}: {{DESCRIPTION}}
- Art. {{YY}}: {{DESCRIPTION}}

**Referenced In:**

| Document | Section | Context |
|----------|---------|---------|
| {{DOCUMENT}} | {{SECTION}} | {{CONTEXT}} |

**CGS Units:**

| Quantity | CGS Unit | Symbol |
|----------|----------|--------|
| {{QUANTITY}} | {{UNIT}} | {{SYMBOL}} |
```

### Citation Network

```markdown
## Citation Network

### Citing {{TARGET_DOCUMENT}}

The following documents cite {{TARGET_DOCUMENT}}:

1. {{ CITING_DOCUMENT_1 }}
   - Citation context: {{CONTEXT}}
   - Maxwell articles: {{ARTICLES}}

2. {{ CITING_DOCUMENT_2 }}
   - Citation context: {{CONTEXT}}
   - Maxwell articles: {{ARTICLES}}

### Cited by {{TARGET_DOCUMENT}}

{{TARGET_DOCUMENT}} cites the following:

1. {{ CITED_DOCUMENT_1 }}
   - Citation context: {{CONTEXT}}
   - Purpose: {{PURPOSE}}

2. {{ CITED_DOCUMENT_2 }}
   - Citation context: {{CONTEXT}}
   - Purpose: {{PURPOSE}}
```

---

## Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `{{VERSION}}` | Cross-reference version | Yes | - |
| `{{GENERATED_DATE}}` | Generation date | Auto | - |
| `{{REFERENCE_TYPE}}` | Type of cross-reference | Yes | - |
| `{{MAXWELL_ARTICLES}}` | Article range covered | Yes | - |
| `{{LINKED_DOCUMENTS}}` | Documents in network | Yes | - |
| `{{CGS_UNITS}}` | Units referenced | Yes | - |
| `{{REFERENCE_TITLE}}` | Title of cross-reference | Yes | - |
| `{{REFERENCE_OVERVIEW}}` | Overview description | Yes | - |
| `{{TOPIC}}` | Article topic | Yes | - |
| `{{DOCUMENT}}` | Document name | Yes | - |
| `{{CONTEXT}}` | Citation context | Yes | - |
| `{{FILE_PATH}}` | Document location | Yes | - |
| `{{LOCATION}}` | Page/section location | Yes | - |
| `{{RELATED_DOCUMENT}}` | Related document | Conditional | - |
| `{{TOPIC_NAME}}` | Topic name | Conditional | - |
| `{{TOPIC_DEFINITION}}` | Topic definition | Conditional | - |
| `{{QUANTITY}}` | Physical quantity | Conditional | - |
| `{{UNIT}}` | CGS unit | Conditional | - |
| `{{SYMBOL}}` | Unit symbol | Conditional | - |
| `{{TARGET_DOCUMENT}}` | Target of analysis | Conditional | - |
| `{{CITING_DOCUMENT}}` | Document that cites | Conditional | - |
| `{{CITED_DOCUMENT}}` | Document that is cited | Conditional | - |
| `{{PURPOSE}}` | Citation purpose | Conditional | - |

---

## Conditional Logic

### Include Article Index If:

```
IF reference_type == "article_index":
  INCLUDE article_index_by_part
  GROUP by Maxwell treatise parts
ELSE IF reference_type == "document_index":
  INCLUDE document_cross_references
```

### Include Citation Network If:

```
IF has_bidirectional_references:
  INCLUDE citation_network_section
  SHOW both citing and cited
ELSE IF has_unidirectional_references:
  INCLUDE references_only_section
```

### Include Topic Index If:

```
IF covers_multiple_topics:
  INCLUDE topic_index
  GROUP by subject area
ELSE:
  USE article_index_only
```

### Include CGS Units Table If:

```
IF references_involve_measurements:
  INCLUDE cgs_units_table
  PROVIDE SI equivalents as reference
```

---

## Cross-Reference Types

### Article Index

Maps Maxwell articles to documents that reference them.

### Document Index

Maps documents to Maxwell articles they cite.

### Topic Index

Maps topics to articles and documents.

### Citation Network

Shows bidirectional citation relationships.

---

## Quality Criteria

### Accuracy

- [ ] All article numbers verified
- [ ] All document links valid
- [ ] All contexts accurately described
- [ ] No broken references

### Completeness

- [ ] All relevant articles covered
- [ ] All relevant documents indexed
- [ ] All topics mapped
- [ ] Citation network complete

### Consistency

- [ ] CGS units consistently noted
- [ ] Theory classification consistent
- [ ] Formatting consistent throughout
- [ ] Cross-references bidirectional

### Usability

- [ ] Easy to navigate
- [ ] Clear organization
- [ ] Helpful context provided
- [ ] Search-friendly structure

---

## Maxwell Treatise Structure

### Part I: Electrostatics (Art. 1-229)

- Fundamental concepts (Art. 1-50)
- Electric fields (Art. 51-150)
- Potential theory (Art. 151-229)

### Part II: Electrokinematics (Art. 230-370)

- Currents (Art. 230-286)
- Networks (Art. 287-300)
- Resistance (Art. 301-370)

### Part III: Magnetism (Art. 371-474)

- Magnetic poles (Art. 371-423)
- Magnetic induction (Art. 424-440)
- Magnetic measurements (Art. 449-474)

### Part IV: Electromagnetism (Art. 475-866)

- Electromagnetic force (Art. 475-500)
- Induction (Art. 501-600)
- Galvanometers (Art. 730-750)
- Light (Art. 780-866)

---

## Output Format

Cross-reference should be:
- Markdown format
- Tables for indices
- Hyperlinked where possible
- Chronologically organized
- Searchable structure

---

## Related Templates

- `{{api-documentation-template.md}}` - API reference
- `{{tutorial-documentation-template.md}}` - Tutorials
- `{{release-notes-template.md}}` - Version changes
