# CG Issue - Enhanced Issue Management with TDD Workflow

Start or resume issue work with intelligent state detection and sequential agent delegation.

## Variables
ISSUE_NUMBER: $ARGUMENTS (IMPORTANT: first argument - the GitHub issue number)

## Instructions

- If the ISSUE_NUMBER is not provided, stop and ask the user to provide it.
- IMPORTANT: This command orchestrates the complete TDD workflow using sequential agent delegation
- The workflow follows: Analysis (cg-analyzer) → Planning (cg-planner) → Implementation (cg-implementer)
- Handle intelligent state detection and context recovery for resumed work

## Workflow Orchestration

### Phase 1: State Analysis and Context Recovery

1. **Issue State Detection**:
   - Check if issue is closed but has incomplete work (existing CG_TDD_* files)
   - Reopen closed issues when development is actually incomplete
   - Detect existing feature branches and determine resume point

2. **Context Recovery**:
   - Read existing `CG_TDD_*` files to understand previous work
   - Determine appropriate starting point (analysis, planning, implementation, or testing)
   - Preserve all development history and decisions

3. **Documentation Setup**:
   - Create `CG_ISSUE_{ISSUE_NUMBER}.md` with issue details and CHANGELOG integration
   - Set up progress tracking throughout development lifecycle

### Phase 2: Sequential Agent Delegation

IMPORTANT: Execute each phase sequentially. Do not proceed to the next phase until the current phase is complete.

#### Step 1: Analysis Phase (Expensive - Claude Opus 4.1)
```
@agent-cg-analyzer "Analyze GitHub issue #{ISSUE_NUMBER} for comprehensive system impact assessment and implementation strategy"
```

**Expected Output**: `CG_TDD_{ISSUE_NUMBER}.md` with:
- Issue summary and analysis
- System impact assessment  
- Architecture decisions and rationale
- Security considerations
- Performance implications
- Recommended implementation approach

#### Step 2: Planning Phase (Balanced - Claude Sonnet 4)
```
@agent-cg-planner "Create comprehensive test strategy for GitHub issue #{ISSUE_NUMBER} based on the analysis phase"
```

**Expected Output**: `CG_TDD_TESTS_{ISSUE_NUMBER}.md` with:
- Test strategy overview
- Unit, integration, and end-to-end test specifications
- Mock and test data strategy
- Coverage requirements and success criteria
- TDD implementation order

#### Step 3: Implementation Phase (Efficient - Claude Sonnet 4)
```
@agent-cg-implementer "Implement TDD solution for GitHub issue #{ISSUE_NUMBER} following the approved analysis and test strategy"
```

**Expected Output**: `CG_TDD_IMPLEMENTATION_{ISSUE_NUMBER}.md` with:
- Implementation task breakdown (atomic, committable tasks)
- TDD implementation order (tests first, then code)
- Integration points with existing codebase
- Quality assurance and validation steps

### Phase 3: Board State Management

1. **Column Transitions**:
   - Move issue through: Sprint Planning → Analysis → Implementation → Testing
   - Update issue status and assignee as appropriate
   - Ensure proper state synchronization

2. **Progress Tracking**:
   - Update `CG_ISSUE_{ISSUE_NUMBER}.md` with progress at each phase
   - Maintain documentation trail for audit and handoffs
   - Track time and cost metrics for optimization

## Intelligent Resume Logic

### Scenario 1: Fresh Start
- Issue in "Sprint Planning" or no existing CG files
- Execute full workflow: Analysis → Planning → Implementation

### Scenario 2: Resume from Analysis
- `CG_TDD_{ISSUE_NUMBER}.md` exists but no test strategy file
- Skip analysis, proceed with Planning → Implementation

### Scenario 3: Resume from Planning  
- Both analysis and test files exist, but no implementation file
- Skip to Implementation phase only

### Scenario 4: Resume from Implementation
- All planning files exist, but implementation is incomplete
- Continue with implementation tasks from where left off

## Error Handling and Recovery

### Analysis Phase Failures
- Retry with clarified context or simplified scope
- Escalate to manual review if complexity exceeds agent capabilities
- Document failure modes for future optimization

### Planning Phase Failures
- Review analysis output for clarity and completeness
- Adjust test strategy scope based on implementation constraints
- Ensure test framework compatibility

### Implementation Phase Failures
- Roll back to implementation planning if architectural issues arise
- Use specialized agents (@security-reviewer, @architecture-reviewer) for specific concerns
- Maintain atomic commits for easy rollback

## Cost Optimization Strategy

### Model Selection Rationale
- **Analysis Phase**: Claude Opus 4.1 for deep architectural understanding (expensive but necessary)
- **Planning Phase**: Claude Sonnet 4 for focused test strategy (balanced cost/performance)  
- **Implementation Phase**: Claude Sonnet 4 for efficient development (cost-effective for iterative work)

### Cost Monitoring
- Track token usage and cost per phase
- Report cost metrics for workflow optimization
- Implement smart fallbacks for budget-constrained scenarios

## Success Criteria

- Issue successfully moves through all workflow phases
- All CG_TDD_* documentation files are created and complete
- Implementation follows TDD methodology (tests first, then code)
- Board state accurately reflects development progress
- Cost remains within optimization targets
- Code integrates properly with existing patterns

## Validation

After workflow completion, verify:
- All tests pass (unit, integration, end-to-end)
- Code follows existing patterns and conventions
- Security and architecture reviews are complete
- Documentation is comprehensive and accurate
- Issue is ready for code review phase