# CG Legacy - Legacy Code Modernization

Brings existing untested code up to TDD standards with comprehensive test retrofitting and modernization.

## Purpose

Modernize legacy codebase by adding comprehensive tests, improving code quality, and integrating with the CG TDD workflow.

## Variables
MODULE_PATH: $ARGUMENTS (OPTIONAL: specific module/directory to modernize, defaults to full codebase analysis)

## Workflow

### Phase 1: Legacy Code Analysis

1. **Codebase Scanning**:
   - Scan existing codebase for untested endpoints/functions
   - Identify code without proper test coverage
   - Analyze code quality and technical debt
   - Document legacy patterns and anti-patterns

2. **Risk Assessment**:
   - Evaluate business-critical functions needing immediate testing
   - Identify high-risk areas with complex logic
   - Assess integration points and external dependencies
   - Prioritize modernization efforts based on impact

3. **Modernization Strategy**:
   - Plan incremental approach to avoid breaking changes
   - Design test strategy for legacy code characteristics
   - Identify refactoring opportunities and constraints

### Phase 2: Test Retrofitting

1. **Test Suite Creation**:
   - Create comprehensive test suites for legacy functions
   - Implement characterization tests to capture current behavior
   - Add unit tests for isolated function logic
   - Create integration tests for system interactions

2. **Coverage Improvement**:
   - Achieve meaningful test coverage for legacy modules
   - Focus on critical paths and edge cases
   - Implement mocking for external dependencies
   - Add regression tests for known issues

3. **Quality Enhancement**:
   - Refactor code to improve testability
   - Extract dependencies for better isolation
   - Improve error handling and logging
   - Update documentation and comments

### Phase 3: Integration with CG Workflow

1. **Framework Integration**:
   - Ensure legacy tests integrate with existing test framework
   - Align with TDD workflow and conventions
   - Configure automated test execution
   - Set up continuous integration for legacy modules

2. **Documentation**:
   - Generate `CG_LEGACY.md` with modernization progress
   - Document patterns and conventions established
   - Create guidelines for future legacy code handling
   - Update project documentation with new standards

## Implementation

```
@agent-cg-analyzer "Perform comprehensive legacy code modernization analysis:

1. Legacy Code Assessment:
   - Scan codebase for untested functions and endpoints
   - Analyze code quality and technical debt
   - Identify business-critical areas needing immediate attention
   - Evaluate integration points and dependencies

2. Test Retrofitting Strategy:
   - Design test approach for legacy code characteristics
   - Plan incremental modernization to avoid breaking changes
   - Prioritize high-impact, high-risk areas first
   - Create comprehensive test coverage plan

3. Modernization Planning:
   - Document refactoring opportunities and constraints
   - Plan integration with existing CG TDD workflow
   - Estimate effort and resource requirements
   - Create timeline for legacy modernization

4. Documentation Generation:
   - Create CG_LEGACY.md with analysis and plan
   - Document established patterns and conventions
   - Provide guidelines for ongoing legacy code handling

Focus on: ${MODULE_PATH if provided, otherwise 'complete codebase assessment'}"
```

### Follow-up Implementation

After analysis, execute the modernization plan:

```
@agent-cg-implementer "Execute legacy code modernization plan:

1. Test Creation:
   - Implement characterization tests for existing behavior
   - Add comprehensive unit tests for legacy functions
   - Create integration tests for system interactions
   - Focus on critical paths and edge cases

2. Code Quality Improvement:
   - Refactor for better testability and maintainability
   - Extract dependencies for improved isolation
   - Enhance error handling and logging
   - Update documentation and comments

3. Integration Validation:
   - Ensure tests integrate with existing framework
   - Validate automated test execution
   - Verify coverage targets are met
   - Test integration with CI/CD pipeline

Follow the modernization plan in CG_LEGACY.md and update progress as work is completed."
```

## Expected Outputs

### CG_LEGACY.md
Comprehensive legacy modernization documentation:
- Legacy code analysis and risk assessment
- Test retrofitting strategy and implementation plan
- Modernization progress tracking
- Established patterns and conventions
- Guidelines for future legacy code handling

### Test Coverage Improvements
- Comprehensive test suites for previously untested code
- Meaningful coverage for business-critical functions
- Integration with existing test framework
- Automated execution and CI/CD integration

## Incremental Approach

### Phase-by-Phase Execution
1. **High-Risk Areas First**: Focus on business-critical, complex logic
2. **Integration Points**: Ensure external dependencies are properly tested
3. **Complete Coverage**: Systematically address remaining untested code
4. **Quality Refinement**: Continuous improvement of test quality and coverage

### Progress Tracking
- Regular updates to `CG_LEGACY.md` with completion status
- Coverage metrics and quality improvements
- Integration with project board for visibility
- Team communication on modernization progress

## Success Criteria

- Legacy code has meaningful test coverage
- Tests integrate seamlessly with CG TDD workflow
- Code quality and maintainability are improved
- Technical debt is reduced
- Team can confidently modify legacy code
- Documentation provides clear guidelines for ongoing work

## Integration with Main Workflow

After legacy modernization:
- Use `/cg-issue <number>` for new feature development on modernized code
- Continue using `/cg-legacy` for additional modules as needed
- Use `/cg-doctor` to validate ongoing modernization health
- Apply established patterns to all new development