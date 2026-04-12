# Checklist: Cross-Reference Linking

## Purpose

Validate that cross-references and links are accurate, functional, and complete throughout documentation.

---

## Level 1: Internal Links (Required)

### Section Links
- [ ] All internal section links functional
- [ ] Section references accurate
- [ ] Heading text matches link text
- [ ] No broken internal links

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Figure/Table Links
- [ ] All figure references functional
- [ ] All table references functional
- [ ] Figure/table numbers accurate
- [ ] Captions match references

**Status:** [ ] Pass [ ] Pass [ ] N/A  
**Score:** ___ / 4

### Index Links
- [ ] Table of contents links functional
- [ ] Index entries linked correctly
- [ ] Page/section numbers accurate
- [ ] Navigation intuitive

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

**Level 1 Total:** ___ / 12 points

---

## Level 2: External Links (Required)

### URL Validity
- [ ] All external URLs valid
- [ ] No 404 errors
- [ ] Links point to correct resources
- [ ] HTTPS used where available

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Link Relevance
- [ ] External links relevant to content
- [ ] Link destination described
- [ ] Link purpose clear
- [ ] No misleading links

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Link Persistence
- [ ] Stable URLs used (DOI, permalink)
- [ ] Archive links provided (if applicable)
- [ ] Link expiration noted (if applicable)
- [ ] Backup references provided

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

**Level 2 Total:** ___ / 12 points

---

## Level 3: Maxwell Article Links (Required)

### Article Reference Links
- [ ] Maxwell article references linked
- [ ] Links point to correct articles
- [ ] Article text accessible (if digital)
- [ ] Article context provided

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Cross-Article Links
- [ ] Related articles cross-referenced
- [ ] Article network mapped
- [ ] Primary/secondary distinctions made
- [ ] Topic connections clear

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Treatise Structure Links
- [ ] Part references linked
- [ ] Chapter references linked
- [ ] Treatise navigation supported
- [ ] Structure documented

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

**Level 3 Total:** ___ / 12 points

---

## Level 4: Document Network (Expert)

### Inter-Document Links
- [ ] Related documents linked
- [ ] Document hierarchy clear
- [ ] Parent/child relationships marked
- [ ] Sibling documents connected

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Bidirectional Links
- [ ] Links work both directions
- [ ] Backlinks provided
- [ ] Reference symmetry maintained
- [ ] No orphaned documents

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Link Context
- [ ] Link purpose described
- [ ] Expected content previewed
- [ ] Link type indicated (API, tutorial, reference)
- [ ] Navigation path clear

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

**Level 4 Total:** ___ / 12 points

---

## Level 5: CGS and Classification Links (Expert)

### CGS Unit Links
- [ ] CGS unit definitions linked
- [ ] Unit conversion references linked
- [ ] Physical constant references linked
- [ ] Unit system documentation linked

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Classification Links
- [ ] Theory classification references linked
- [ ] maxwell_original sources linked
- [ ] user_original context linked
- [ ] standard_math references linked

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Semantic Links
- [ ] Concept definitions linked
- [ ] Term glossary linked
- [ ] Topic indices linked
- [ ] Semantic relationships marked

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

**Level 5 Total:** ___ / 12 points

---

## Summary

| Level | Category | Score | Max | Percentage |
|-------|----------|-------|-----|------------|
| 1 | Internal Links | ___ | 12 | ___% |
| 2 | External Links | ___ | 12 | ___% |
| 3 | Maxwell Article Links | ___ | 12 | ___% |
| 4 | Document Network | ___ | 12 | ___% |
| 5 | CGS and Classification Links | ___ | 12 | ___% |
| **TOTAL** | | **___** | **60** | **___%** |

### Approval Status

**Status:** [ ] Approved [ ] Conditional [ ] Rejected

**Approver:** ______________________

**Date:** ______________________

**Next Review:** ______________________

---

## Link Types Reference

### Internal Links

| Type | Format | Example |
|------|--------|---------|
| Section | `#section-name` | `#cgs-units` |
| Figure | `#figure-N` | `#figure-3` |
| Table | `#table-N` | `#table-2` |
| Equation | `#eq-N` | `#eq-5` |

### External Links

| Type | Format | Example |
|------|--------|---------|
| Maxwell Treatise | URL | `https://archive.org/maxwell-treatise` |
| Academic Paper | DOI | `https://doi.org/10.xxxx/xxxx` |
| Documentation | URL | `https://docs.example.com` |

### Cross-Document Links

| Type | Format | Example |
|------|--------|---------|
| Agent | `../agent-name/file.md` | `../materia/agent.md` |
| Template | `../templates/name.md` | `../templates/api-docs.md` |
| Checklist | `../checklists/name.md` | `../checklists/validation.md` |

---

## Quality Criteria

- [ ] All internal links functional
- [ ] All external URLs valid
- [ ] Maxwell article references linked
- [ ] Document network connected
- [ ] CGS and classification links present
