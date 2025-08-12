# CG Test - Independent Test Runner

Validates TDD implementation without full workflow execution, providing focused testing and coverage analysis.

## Purpose

Run comprehensive tests for specific issues, analyze coverage, validate TDD implementation, and generate detailed test reports independent of the main CG workflow.

## Variables
ISSUE_NUMBER: $ARGUMENTS (IMPORTANT: first argument - the GitHub issue number to test)
TEST_TYPE: $ARGUMENTS (OPTIONAL: second argument - 'unit', 'integration', 'e2e', 'all' - defaults to 'all')

## Instructions

- If the ISSUE_NUMBER is not provided, stop and ask the user to provide it.
- This command focuses exclusively on testing validation
- Independent of workflow state - can be run at any time
- Provides detailed testing analysis and recommendations

## Test Execution Workflow

### Phase 1: Test Discovery and Validation

1. **Test File Discovery**:
   - Locate all tests related to the specified issue
   - Identify unit tests, integration tests, and end-to-end tests
   - Validate test file naming and organization
   - Check for missing or incomplete test coverage

2. **Test Environment Validation**:
   - Verify testing framework is properly configured
   - Check test dependencies and setup requirements
   - Validate mock configurations and test data
   - Ensure test environment is clean and isolated

3. **TDD Compliance Check**:
   - Verify tests were written before implementation code
   - Check for proper test structure and organization
   - Validate that tests follow TDD best practices
   - Ensure tests are meaningful and comprehensive

### Phase 2: Test Execution

```
@agent-cg-implementer "Execute comprehensive test validation for GitHub issue #{ISSUE_NUMBER}:

1. Test Discovery:
   - Locate all tests related to issue #{ISSUE_NUMBER}
   - Identify unit, integration, and end-to-end tests
   - Validate test file organization and naming
   - Check for comprehensive test coverage

2. Test Environment Setup:
   - Verify testing framework configuration
   - Validate dependencies and test data setup
   - Ensure clean, isolated test environment
   - Check mock configurations and external service setup

3. Test Execution:
   - Run unit tests and validate all pass
   - Execute integration tests and check results
   - Run end-to-end tests if applicable
   - Generate detailed test execution report

4. Coverage Analysis:
   - Measure code coverage for issue-related code
   - Identify gaps in test coverage
   - Analyze quality of test assertions
   - Evaluate edge case and error scenario coverage

5. TDD Validation:
   - Verify tests follow TDD methodology
   - Check that tests were written before implementation
   - Validate test quality and meaningfulness
   - Ensure proper test isolation and independence

Test Type Focus: ${TEST_TYPE if provided, otherwise 'all test types'}
Generate CG_TDD_TEST_RESULTS_{ISSUE_NUMBER}.md with comprehensive analysis."
```

## Test Type Specifications

### Unit Tests (`/cg-test 123 unit`)
Focus on isolated function/method testing:
- Individual function behavior validation
- Edge case and boundary condition testing
- Error handling and exception scenarios
- Mock-based isolation of dependencies

### Integration Tests (`/cg-test 123 integration`)
Focus on component interaction testing:
- API endpoint testing
- Database interaction validation
- Service integration verification
- Cross-module communication testing

### End-to-End Tests (`/cg-test 123 e2e`)
Focus on complete user workflow testing:
- Full user journey validation
- Browser-based testing (if applicable)
- Real environment integration
- Performance and reliability testing

### All Tests (`/cg-test 123` or `/cg-test 123 all`)
Comprehensive testing across all types:
- Complete test suite execution
- Cross-type coverage analysis
- Integration between test levels
- Comprehensive quality assessment

## Expected Output

### CG_TDD_TEST_RESULTS_{ISSUE_NUMBER}.md
Comprehensive test results documentation:

#### Test Execution Summary
- Total tests run by type
- Pass/fail status for each test category
- Execution time and performance metrics
- Overall test health score

#### Coverage Analysis
- Code coverage percentage by file/function
- Coverage gaps and missing tests
- Quality assessment of test assertions
- Edge case and error scenario coverage

#### TDD Compliance Report
- Verification that tests were written first
- Assessment of test quality and structure
- TDD methodology adherence score
- Recommendations for improvement

#### Detailed Test Results
- Individual test results with pass/fail status
- Error messages and failure analysis
- Performance metrics for slow tests
- Recommendations for test optimization

#### Coverage Gaps and Recommendations
- Specific functions/methods lacking coverage
- Missing edge cases and error scenarios
- Integration points needing additional testing
- Recommended additional tests to implement

## Advanced Testing Features

### Performance Testing
When applicable, include performance validation:
- Response time measurement for API endpoints
- Memory usage analysis for complex operations
- Concurrent request handling validation
- Resource utilization monitoring

### Security Testing
Integrate security validation when relevant:
- Input validation and sanitization testing
- Authentication and authorization testing
- SQL injection and XSS vulnerability testing
- Data privacy and security compliance

### Regression Testing
Validate against previous implementations:
- Compare current results with baseline
- Identify performance regressions
- Validate bug fixes remain effective
- Ensure new features don't break existing functionality

## Error Handling and Troubleshooting

### Test Failure Analysis
When tests fail:
- Provide detailed failure analysis
- Identify root cause of failures
- Recommend specific fixes
- Prioritize failures by severity and impact

### Environment Issues
When test environment problems occur:
- Diagnose configuration issues
- Identify missing dependencies
- Validate test data and setup
- Recommend environment fixes

### Coverage Issues
When coverage is insufficient:
- Identify specific coverage gaps
- Recommend additional tests to implement
- Suggest refactoring for better testability
- Provide guidance on improving test quality

## Integration with Main Workflow

### During Development
- Use `/cg-test` to validate implementation progress
- Run focused tests during iterative development
- Verify TDD compliance throughout implementation
- Validate coverage before moving to next phase

### Before Code Review
- Comprehensive test validation before PR creation
- Coverage verification meets project standards
- Performance and security validation
- Documentation of test results for reviewers

### Quality Assurance
- Independent validation of test quality
- Verification of TDD methodology compliance
- Coverage gap identification and resolution
- Continuous test health monitoring

## Success Criteria

- All tests for the issue pass successfully
- Test coverage meets or exceeds project standards
- Tests follow TDD methodology and best practices
- Test execution is efficient and reliable
- Coverage gaps are identified and documented
- Test quality is high with meaningful assertions
- Integration between test types is validated

## When to Use

**Use `/cg-test` when**:
- Validating test implementation during development
- Checking coverage before code review
- Debugging test failures or issues
- Verifying TDD compliance
- Independent quality assurance
- Performance or regression testing

**Integrate with other commands**:
- Use with `/cg-issue` during implementation phase
- Combine with `/cg-doctor` for comprehensive health checks
- Use before `/cg-push` to ensure test quality
- Integrate with CI/CD pipeline for automated validation