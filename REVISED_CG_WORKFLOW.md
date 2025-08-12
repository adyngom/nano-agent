# Revised Claude-Gemini Production Workflow

After extensive testing, we identified critical gaps in our automated workflow for production-quality code. This revision addresses issue lifecycle management, implements Test-Driven Development (TDD), and ensures proper GitHub process integration with board automation.

## Core Principles
- **TDD-First**: All new features must have tests before implementation
- **State Integrity**: Issue states must accurately reflect actual development progress  
- **Context Preservation**: Development history and decisions must persist across sessions
- **Production Ready**: Code must pass comprehensive testing before review

## Project Context
Currently targeting projects with 50+ existing issues. The workflow must handle both new feature development and legacy code modernization. 

## Workflow Commands

### `/cg-init` - Project Initialization
Sets up and verifies project readiness for the CG workflow:

1. **Environment Verification**: 
   - Checks for required dependencies and tools
   - Validates GitHub integration and project board access
   - Detects existing testing framework (Jest for Next.js, others as applicable)

2. **Documentation Generation**:
   - Creates `CG_INIT.md` with project assessment and recommendations
   - Moves to `docs/` folder when initialization is complete
   - Generates `CG_ISSUES.md` with issues in "Sprint Planning" column

3. **Test Framework Setup**:
   - Auto-detects Jest for Next.js projects
   - Configures sensible defaults for other frameworks
   - Validates test runner configuration

### `/cg-legacy` - Legacy Code Modernization
Brings existing untested code up to TDD standards:

1. **Code Analysis**: Scans existing codebase for untested endpoints/functions
2. **Test Retrofit**: Creates comprehensive test suites for legacy code
3. **Documentation**: Generates `CG_LEGACY.md` with modernization progress
4. **Integration**: Ensures legacy tests integrate with new TDD workflow

### `/cg-issue <number>` - Start/Resume Issue Work
Enhanced issue management with intelligent state detection:

1. **State Analysis**:
   - Checks if issue is closed but has incomplete work (existing CG_TDD_* files)
   - Reopens closed issues when development is actually incomplete
   - Detects existing feature branches and resumes work appropriately

2. **Context Recovery**:
   - Reads existing `CG_TDD_*` files to understand previous work
   - Determines appropriate starting point (analysis, planning, implementation, or testing)
   - Preserves all development history and decisions

3. **Documentation Creation**:
   - Creates `CG_ISSUE_<number>.md` with issue details and CHANGELOG integration
   - Updates progress tracking throughout development lifecycle

### `/cg-resume <number>` - Explicit Resume Command
For cases where automatic resume detection needs manual override:

1. **Force Resume**: Explicitly continues work on apparently "completed" issues
2. **Context Analysis**: Deep analysis of existing work state and remaining tasks
3. **Branch Management**: Handles complex branch scenarios and merge conflicts

### `/cg-doctor` - Workflow Health Check
Comprehensive diagnostic and troubleshooting:

1. **Workflow Validation**: Checks for orphaned documentation files and inconsistent states
2. **Tool Verification**: Validates all required tools and integrations are working
3. **Issue Audit**: Reports on issue states vs. actual development progress

### `/cg-test <number>` - Independent Test Runner
Validates TDD implementation without full workflow:

1. **Test Execution**: Runs all tests for specific issue
2. **Coverage Analysis**: Reports test coverage and identifies gaps
3. **Results Documentation**: Updates `CG_TDD_TEST_RESULTS_<number>.md`

## Hybrid Claude-Gemini Architecture via MCP

### Model Strategy (UPDATED)
- **Development**: Claude Sonnet 4 (TDD implementation, code creation)
- **Heavy Analysis**: Gemini via MCP (security review, large context analysis)
- **Cost Optimization**: Targeted delegation for expensive operations only

### MCP Integration
- **Server**: @fuko2935/gemini-mcp-server via Smithery (Docker containerized)
- **Features**: 36 specialized analysis modes, 98% success rate
- **Team Distribution**: Zero Python dependencies, simple configuration
- **Authentication**: Gemini API key via environment variables

### Agent Specialization

#### 1. **tdd-issue-analyzer** (CTO-Level Analysis)
**Model**: Claude Opus 4.1  
**Role**: Senior Software Architect with deep system understanding

**Responsibilities**:
- Comprehensive issue analysis and system impact assessment
- Architecture decision documentation and technical debt consideration
- Creates `CG_TDD_<issue-number>.md` with implementation strategy
- Security and performance implications analysis
- Integration with existing codebase patterns

#### 2. **tdd-issue-planner** (Test Strategy)
**Model**: Claude Sonnet 4 (focused context, not Haiku - too limited for test planning)  
**Role**: Senior Test Engineer with comprehensive testing knowledge

**Responsibilities**:
- Develops complete test strategy based on analysis phase
- Creates `CG_TDD_TESTS_<issue-number>.md` with all required tests
- Unit, integration, and end-to-end test planning
- Test data and mock strategy definition
- Coverage requirements and success criteria

**Note**: Claude Code cannot run multiple agent instances simultaneously. Sequential execution with handoff between agents.

#### 3. **tdd-issue-implementer** (Development)
**Model**: Claude Sonnet 4 with specialized agent integration  
**Role**: Senior Developer with access to all available tools and agents

**Responsibilities**:
- Creates detailed `CG_TDD_IMPLEMENTATION_<issue-number>.md` task list
- Uses existing specialized agents (security-reviewer, architecture-reviewer, etc.)
- Implements tests first, then production code (true TDD)
- Each task completion = atomic commit with detailed message
- Integrates with existing codebase patterns and conventions

## Board Integration and State Management

### Revised Board Flow
```
Sprint Planning → Analysis → Implementation → Testing → Code Review → E2E Testing → Done
```

**Key Changes**:
- **Testing before Code Review**: Ensures reviewers see tested, working code
- **E2E Testing**: Separate phase for Playwright end-to-end validation
- **State Synchronization**: Board automatically reflects actual development progress

### Column Transitions

#### Sprint Planning → Analysis
- Triggered by `/cg-issue <number>` command
- Issue assigned to developer
- `tdd-issue-analyzer` creates implementation strategy

#### Analysis → Implementation  
- Analysis phase complete with approved `CG_TDD_<number>.md`
- `tdd-issue-planner` creates comprehensive test strategy
- Feature branch created/checked out

#### Implementation → Testing
- All planned tests implemented and passing
- Production code complete according to TDD methodology
- `CG_TDD_TEST_RESULTS_<number>.md` generated with full coverage report

#### Testing → Code Review
- Automatic transition when all tests pass
- `/cg-push` triggered automatically
- PR created with full documentation trail

#### Code Review → E2E Testing
- PR approved by human reviewers
- Security and architecture reviews complete
- Ready for comprehensive end-to-end validation

#### E2E Testing → Done
- All Playwright tests pass
- Final integration validation complete
- Issue and PR automatically closed

### Failure Recovery

#### Test Failures (Testing → Implementation)
- Automatic column move back to "Implementation"
- Issue remains assigned to original developer  
- Context preserved in TDD documentation

#### Code Review Failures (Code Review → Implementation)
- Issue reopened and moved to "Implementation"
- PR remains open with review feedback
- Security/architecture issues documented for resolution

#### E2E Test Failures (E2E Testing → Code Review)
- Move back to "Code Review" for additional fixes
- Integration issues documented and assigned

## Workflow Orchestration

### Command Sequence (UPDATED with MCP Integration)
```bash
# Initial setup (once per project)
/cg-init

# Legacy code modernization (as needed)
/cg-legacy

# Per-issue development cycle
/cg-issue <number>          # Starts TDD workflow
# → Analysis phase (Claude Sonnet 4)
# → Planning phase (Claude Sonnet 4)  
# → Implementation phase (Claude Sonnet 4 + specialized agents)
# → Testing validation
/cg-push                    # Basic handoff to Gemini CLI

# Enhanced workflow with MCP delegation (NEW)
/cg-push "message" --security-analysis    # Claude + Gemini security review
/cg-security-review <number>              # Dedicated Gemini security analysis
/cg-analyze-context <issue-list>          # Batch analysis via Gemini large context

# Manual overrides and diagnostics
/cg-resume <number>         # Force resume interrupted work
/cg-doctor                  # Health check and diagnostics
/cg-test <number>          # Independent test validation
```

### Error Handling and Recovery

#### Documentation Management
- `CG_*.md` files stored in `docs/` directory within project repository
- Files committed with implementation for full audit trail
- Cleanup handled automatically on issue completion

#### Multi-Developer Coordination
- Feature branch isolation prevents conflicts during TDD phases
- Board state provides real-time visibility into team progress
- Documentation trails enable seamless handoffs between developers

#### Cost Optimization (UPDATED)
- **Targeted Delegation**: Expensive analysis only when requested via flags
- **Docker Distribution**: No Python dependency management for teams
- **MCP Efficiency**: Gemini large context for batch processing
- **Smart Fallback**: Claude Sonnet 4 security checklist if Gemini unavailable
- **80%+ Cost Reduction**: From expensive Claude Opus security analysis

#### Expected Cost Impact
```
Previous Approach:
50 issues × 80K tokens × Claude Opus pricing = $2000-3000+

Current Approach:  
50 issues × 15K Claude tokens + targeted Gemini analysis = $300-500
Savings: 80%+ reduction while improving analysis quality
```
