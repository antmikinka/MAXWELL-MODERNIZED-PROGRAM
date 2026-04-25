# Task: Cross-Part Dependency Verification

## Description

Comprehensive verification of all inter-part dependencies across the 6 Parts of Maxwell's Treatise. This task ensures that the layered architecture maintains proper separation of concerns and that all cross-part references are valid.

## Workflow

### Step 1: Dependency Declaration Extraction

For each Part:
1. Parse architecture COMPLETE document
2. Extract declared dependencies on other Parts
3. Extract module-level dependencies
4. Extract import statements from code
5. Build dependency declaration map

### Step 2: Dependency Graph Construction

Build directed graph:
- Nodes: Parts and modules
- Edges: Dependencies (directed)
- Weights: Dependency strength (critical, functional, optional)

### Step 3: Cycle Detection

Apply Tarjan's algorithm:
1. Find all strongly connected components
2. Identify circular dependencies
3. Report cycles with full path
4. Recommend cycle-breaking strategies

### Step 4: Dependency Validation

For each dependency:
1. Verify target module exists
2. Verify interface compatibility
3. Check version compatibility
4. Validate import paths
5. Test dependency loading

### Step 5: Impact Analysis

For each Part:
1. Identify all dependents (what depends on this)
2. Identify all dependencies (what this depends on)
3. Calculate change propagation paths
4. Estimate impact of modifications
5. Document breaking change scenarios

### Step 6: Bridge Module Verification

Identify and verify bridge modules:
- Part II → Part III bridge (Electrokinematics to Magnetism)
- Part III → Part IV bridge (Magnetism to Electromagnetism)
- Part IV → Part V bridge (Electromagnetism to System Core)

## Input

- All 6 Architecture COMPLETE documents
- Python source files (for import analysis)
- Module registry
- Dependency declaration files

## Output

### Primary Deliverable

`Cross_Part_Dependency_Report.md` containing:
- Dependency matrix
- Dependency graph visualization
- Cycle analysis results
- Validation status
- Impact analysis
- Bridge module documentation

### Secondary Deliverables

- `dependency_matrix.csv` - Part-to-part dependency table
- `dependency_graph.dot` - GraphViz format graph
- `cycle_report.json` - Cycle detection results
- `impact_analysis.json` - Change propagation data

## Success Criteria

- [ ] All dependencies extracted and documented
- [ ] Dependency graph is acyclic (DAG)
- [ ] All dependencies validated
- [ ] Impact analysis complete
- [ ] Bridge modules verified
- [ ] No undeclared dependencies found

## Estimated Duration

- Initial analysis: 2-4 hours
- Full verification: 4-8 hours
- Impact analysis: 2-4 hours

## Related Commands

- `check-dependencies` - Dependency verification command
- `validate-architecture` - Architecture validation

## Related Templates

- `dependency-map.md` - Dependency documentation template

## Dependency Matrix Format

```
| From Part | To Part I | To Part II | To Part III | To Part IV | To Part V |
|-----------|-----------|------------|-------------|------------|-----------|
| Part I    | -         | No         | No          | No         | No        |
| Part II   | Yes       | -          | No          | No         | No        |
| Part III  | Yes       | Yes        | -           | No         | No        |
| Part IV   | Yes       | Yes        | Yes         | -          | No        |
| Part V    | Yes       | Yes        | Yes         | Yes        | -         |
| Part VI   | Yes       | Yes        | Yes         | Yes        | Yes       |
```

## Example Output

```
Cross-Part Dependency Verification Report
==========================================

DEPENDENCY MATRIX
-----------------
[Matrix shown above]

DEPENDENCY GRAPH
----------------
Part VI → Parts I, II, III, IV, V
Part V → Parts I, II, III, IV
Part IV → Parts I, II, III
Part III → Parts I, II
Part II → Part I
Part I → (none, foundation)

CYCLE ANALYSIS
--------------
Circular Dependencies: NONE
Graph Type: DAG (Directed Acyclic Graph)

DEPENDENCY VALIDATION
---------------------
Total Dependencies: 35
Valid: 35 (100%)
Invalid: 0
Warnings: 2

BRIDGE MODULES
--------------
Part II → Part III:
  - maxwell/magnetics/coupling.py [VALID]
  
Part III → Part IV:
  - maxwell/em/induction.py [VALID]
  
Part IV → Part V:
  - maxwell/core/system.py [VALID]

IMPACT ANALYSIS
---------------
If Part I changes:
  Direct impact: Parts II, III, IV, V, VI
  Modules affected: 313 (100%)
  
If Part IV changes:
  Direct impact: Parts V, VI
  Modules affected: 53 (17%)
```
