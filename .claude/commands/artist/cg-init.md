# CG Init - Project Initialization

Sets up and verifies project readiness for the CG workflow with comprehensive environment checks and documentation generation.

## Purpose

Prepare any project for the CG TDD workflow by validating dependencies, setting up testing frameworks, and generating initial documentation.

## Variables
No arguments required - analyzes current project automatically.

## Workflow

### Phase 1: Environment Verification

1. **Dependency Checks**:
   - Verify Git repository is properly initialized
   - Check for GitHub integration and API access
   - Validate project board access and permissions
   - Ensure required development tools are available

2. **Project Analysis**:
   - Detect project type (Next.js, React, Node.js, Python, etc.)
   - Identify existing testing framework or recommend setup
   - Analyze codebase structure and patterns
   - Assess current test coverage and quality

3. **Tool Configuration**:
   - Validate nano-agent MCP server connectivity
   - Test specialized agent availability (security-reviewer, architecture-reviewer)
   - Verify cost optimization settings and API keys

### Phase 2: Testing Framework Setup

1. **Framework Detection**:
   - Auto-detect Jest for Next.js projects
   - Identify existing test runners (pytest, mocha, etc.)
   - Recommend optimal testing framework for project type

2. **Configuration Validation**:
   - Verify test runner configuration is correct
   - Check for code coverage tools and settings
   - Ensure test scripts are properly defined

3. **TDD Readiness**:
   - Validate that tests can be run independently
   - Check for mocking capabilities and test data setup
   - Ensure integration test environment is available

### Phase 3: Documentation Generation

1. **Project Assessment**:
   - Create `CG_INIT.md` with comprehensive project analysis
   - Document current state, capabilities, and recommendations
   - Identify potential technical debt and modernization opportunities

2. **Issue Analysis**:
   - Generate `CG_ISSUES.md` with issues in "Sprint Planning" column
   - Prioritize issues based on complexity and dependencies
   - Estimate effort and resource requirements

3. **Workflow Setup**:
   - Document CG workflow configuration for this project
   - Set up directory structure for CG documentation
   - Create templates for consistent documentation

## Implementation

```
@agent-cg-analyzer "Perform comprehensive project initialization analysis:

1. Environment Analysis:
   - Check Git repository status and GitHub integration
   - Verify project board access and configuration
   - Validate development tool dependencies

2. Project Assessment:
   - Detect project type and framework
   - Analyze existing testing setup and coverage
   - Identify codebase patterns and conventions

3. TDD Readiness Evaluation:
   - Assess current testing framework capabilities
   - Recommend testing strategy for project type
   - Identify gaps in test infrastructure

4. Documentation Generation:
   - Create CG_INIT.md with project assessment
   - Generate CG_ISSUES.md with Sprint Planning items
   - Document workflow configuration and setup

Provide detailed analysis and actionable recommendations for CG workflow implementation."
```

## Expected Outputs

### CG_INIT.md
Comprehensive project assessment including:
- Project type and framework analysis
- Current testing setup evaluation
- Development environment validation
- Recommended improvements and setup steps
- CG workflow configuration for this project

### CG_ISSUES.md
Issue management documentation including:
- Issues currently in "Sprint Planning" column
- Priority and complexity analysis
- Estimated effort and dependencies
- Recommended implementation order

## Success Criteria

- All required dependencies and tools are validated
- Testing framework is properly configured for TDD
- Project is ready for CG workflow implementation
- Documentation provides clear guidance for team members
- Issues are properly prioritized and ready for development

## Post-Initialization

After successful initialization:
- Move `CG_INIT.md` to `docs/` folder for permanent reference
- Use `/cg-issue <number>` to start development on prioritized issues
- Use `/cg-legacy` if legacy code modernization is needed
- Use `/cg-doctor` periodically to validate workflow health