# CG Resume - Explicit Resume Command

For cases where automatic resume detection needs manual override or when complex context recovery is required.

## Purpose

Explicitly continue work on apparently "completed" issues or handle complex scenarios where automatic state detection needs manual intervention.

## Variables
ISSUE_NUMBER: $ARGUMENTS (IMPORTANT: first argument - the GitHub issue number to resume)
FORCE_PHASE: $ARGUMENTS (OPTIONAL: second argument - specific phase to resume from: analysis, planning, implementation, testing)

## Instructions

- If the ISSUE_NUMBER is not provided, stop and ask the user to provide it.
- This command forces resumption even when automatic detection suggests work is complete
- Useful for complex scenarios, debugging, or when context needs manual intervention

## Resume Scenarios

### Scenario 1: Force Resume "Completed" Issue
- Issue appears complete but needs additional work
- Manual override of automatic state detection
- Deep context analysis to determine actual work state

### Scenario 2: Context Recovery After Interruption
- Work was interrupted mid-stream
- Session ended unexpectedly during implementation
- Need to reconstruct work context and continue

### Scenario 3: Branch Management Complications
- Complex merge conflicts or branch issues
- Multiple developers worked on same issue
- Need to reconcile conflicting work states

### Scenario 4: Debugging Workflow Issues
- CG workflow encountered errors or inconsistencies
- Need to manually inspect and correct workflow state
- Troubleshoot agent delegation or documentation issues

## Workflow

### Phase 1: Deep Context Analysis

```
@agent-cg-analyzer "Perform deep context analysis for resuming GitHub issue #{ISSUE_NUMBER}:

1. Comprehensive State Assessment:
   - Analyze all existing CG_TDD_* files for this issue
   - Review Git branch state and commit history
   - Check GitHub issue status and board position
   - Identify any conflicting or incomplete work

2. Work Progress Evaluation:
   - Determine actual completion state vs. apparent state
   - Identify gaps in documentation or implementation
   - Assess quality of existing work and decisions
   - Document any issues or inconsistencies found

3. Resume Strategy:
   - Recommend optimal resumption point
   - Identify dependencies and prerequisites
   - Plan approach to resolve any conflicts or issues
   - Ensure continuity with existing work

Force Phase Override: ${FORCE_PHASE if provided, otherwise 'automatic detection'}
Provide detailed analysis and specific recommendations for safe resumption."
```

### Phase 2: Targeted Resumption

Based on analysis results, execute targeted resumption:

#### Resume from Analysis Phase
```
@agent-cg-analyzer "Continue analysis work for issue #{ISSUE_NUMBER} with context preservation:
- Review and enhance existing CG_TDD_{ISSUE_NUMBER}.md
- Address any gaps or inconsistencies identified
- Ensure analysis meets current standards and requirements"
```

#### Resume from Planning Phase
```
@agent-cg-planner "Continue test planning for issue #{ISSUE_NUMBER} with context preservation:
- Review and enhance existing CG_TDD_TESTS_{ISSUE_NUMBER}.md
- Address any gaps in test strategy
- Ensure compatibility with current implementation approach"
```

#### Resume from Implementation Phase
```
@agent-cg-implementer "Continue implementation for issue #{ISSUE_NUMBER} with context preservation:
- Review existing CG_TDD_IMPLEMENTATION_{ISSUE_NUMBER}.md
- Assess current code state and test completion
- Continue from last completed atomic task
- Maintain consistency with established patterns"
```

### Phase 3: State Reconciliation

1. **Documentation Updates**:
   - Update all CG_TDD_* files with current state
   - Ensure consistency across all documentation
   - Document resume process and any changes made

2. **Board State Correction**:
   - Move issue to appropriate column based on actual state
   - Update assignee and status as needed
   - Ensure board reflects reality of development progress

3. **Branch Management**:
   - Resolve any branch conflicts or issues
   - Ensure clean working state for continued development
   - Update branch with latest changes if needed

## Advanced Resume Options

### Force Phase Override
When FORCE_PHASE is specified:
- Skip automatic state detection
- Start directly from specified phase
- Useful for debugging or specific workflow scenarios
- Requires manual validation of prerequisites

### Conflict Resolution
For complex scenarios with conflicts:
- Analyze all conflicting work and documentation
- Recommend resolution strategy
- Implement changes to ensure consistency
- Document resolution process for future reference

### Multi-Developer Coordination
When multiple developers have worked on an issue:
- Identify all contributors and their changes
- Reconcile different approaches and decisions
- Ensure unified direction going forward
- Update documentation to reflect consolidated approach

## Error Handling

### Invalid Resume State
- If issue cannot be safely resumed, document why
- Recommend alternative approaches (restart from specific phase)
- Provide clear guidance on manual intervention needed

### Missing Context
- If critical context is missing, reconstruct from available information
- Document assumptions and decisions made during reconstruction
- Implement additional safeguards to prevent context loss

### Workflow Inconsistencies
- Identify and document any workflow or process issues
- Implement fixes to prevent similar issues in the future
- Update workflow documentation with lessons learned

## Success Criteria

- Issue work can be safely continued from appropriate point
- All documentation is consistent and up-to-date
- Board state accurately reflects development progress
- Any conflicts or issues are resolved
- Clear path forward is established
- Context is preserved and enhanced

## When to Use

**Use `/cg-resume` when**:
- Automatic resume detection is insufficient
- Complex context recovery is needed
- Manual intervention is required for workflow issues
- Debugging CG workflow problems
- Multiple developers need coordination

**Use `/cg-issue` instead when**:
- Simple continuation of normal workflow
- Automatic state detection is working correctly
- No complex conflicts or issues exist