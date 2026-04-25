# Checklist: Code Review

## Purpose

Systematic code review for mathematical implementations.

## Review Information

| Field | Value |
|-------|-------|
| Component | {component_name} |
| Author | {author_name} |
| Reviewer | {reviewer_name} |
| Date | {date} |

## Code Structure

- [ ] **Modularity**: Code is well-modularized
- [ ] **Single Responsibility**: Each function does one thing
- [ ] **Function Length**: Functions < 50 lines (excluding docs)
- [ ] **Class Design**: Classes have clear purpose
- [ ] **Inheritance**: Inheritance hierarchy is shallow

## Naming Conventions

- [ ] **Function Names**: snake_case, descriptive
- [ ] **Class Names**: PascalCase, descriptive
- [ ] **Variables**: Clear, meaningful names
- [ ] **Constants**: UPPER_CASE
- [ ] **Private Members**: Leading underscore

## Readability

- [ ] **Whitespace**: Consistent formatting
- [ ] **Comments**: Comments explain why, not what
- [ ] **Complexity**: Cyclomatic complexity < 10
- [ ] **Nesting**: Max nesting depth < 4
- [ ] **Line Length**: Lines < 100 characters

## Error Handling

- [ ] **Exception Types**: Appropriate exception types
- [ ] **Error Messages**: Clear, actionable messages
- [ ] **Edge Cases**: Edge cases handled gracefully
- [ ] **Fail Fast**: Invalid input caught early
- [ ] **Resource Cleanup**: Resources properly released

## Testing

- [ ] **Test Coverage**: > 90% line coverage
- [ ] **Test Quality**: Tests verify behavior, not implementation
- [ ] **Edge Cases**: Edge cases tested
- [ ] **Error Tests**: Error conditions tested
- [ ] **Regression Tests**: Regression tests present

## Documentation

- [ ] **Module Docstring**: Present and accurate
- [ ] **Function Docstrings**: Complete for all public functions
- [ ] **Type Hints**: Complete type annotations
- [ ] **Examples**: Working examples provided
- [ ] **References**: Maxwell articles cited

## Performance

- [ ] **Algorithm Choice**: Appropriate algorithm selected
- [ ] **Vectorization**: NumPy vectorization used
- [ ] **Memory**: Memory usage reasonable
- [ ] **Caching**: Results cached where appropriate
- [ ] **Profiling**: Performance profiled

## Security (if applicable)

- [ ] **Input Sanitization**: Inputs validated
- [ ] **No Hardcoded Secrets**: No hardcoded credentials
- [ ] **Safe Evaluation**: No unsafe eval/exec

## Version Control

- [ ] **Commit Messages**: Clear, descriptive messages
- [ ] **Branch Name**: Descriptive branch name
- [ ] **Change Scope**: Focused change (single concern)
- [ ] **Diff Size**: Reasonable diff size (< 500 lines)

## Review Decision

- [ ] **Approved**: Ready to merge
- [ ] **Approved with Comments**: Minor issues to address
- [ ] **Changes Requested**: Significant changes needed
- [ ] **Rejected**: Fundamental issues

## Review Comments

| Line | Type | Comment |
|------|------|---------|
| {line} | {BUG|STYLE|OPTIMIZATION|QUESTION} | {comment} |

## Follow-up Actions

- [ ] {action_1}
- [ ] {action_2}
