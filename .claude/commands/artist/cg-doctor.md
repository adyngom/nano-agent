# CG Doctor - Workflow Health Check

Comprehensive diagnostic and troubleshooting for the CG TDD workflow with detailed health reporting.

## Purpose

Validate CG workflow health, identify orphaned files, diagnose inconsistencies, and ensure all tools and integrations are functioning properly.

## Variables
SCOPE: $ARGUMENTS (OPTIONAL: specific scope for health check - 'issues', 'tools', 'files', 'board', 'all' - defaults to 'all')

## Diagnostic Categories

### 1. Workflow Validation
- Check for orphaned CG_TDD_* documentation files
- Identify inconsistent states between documentation and actual work
- Validate issue progression through workflow phases
- Detect incomplete or abandoned work

### 2. Tool Verification
- Test nano-agent MCP server connectivity
- Validate specialized agent availability (@security-reviewer, @architecture-reviewer, etc.)
- Check GitHub API access and permissions
- Verify project board access and configuration

### 3. Issue Audit
- Compare issue states vs. actual development progress
- Identify issues stuck in incorrect columns
- Detect closed issues with incomplete work
- Report on issue assignment and progress accuracy

### 4. File System Health
- Scan for orphaned or misnamed CG documentation files
- Validate documentation consistency and completeness
- Check for missing required files for active issues
- Identify outdated or conflicting documentation

## Implementation

```
@agent-cg-analyzer "Perform comprehensive CG workflow health check:

1. Workflow Validation:
   - Scan for all CG_TDD_* files in the project
   - Cross-reference with active GitHub issues
   - Identify orphaned, incomplete, or inconsistent documentation
   - Validate workflow state progression

2. Tool and Integration Testing:
   - Test nano-agent MCP server connectivity
   - Verify access to specialized agents
   - Check GitHub API and project board access
   - Validate testing framework and CI/CD integration

3. Issue State Audit:
   - Compare GitHub issue states with actual development progress
   - Identify issues in incorrect board columns
   - Detect closed issues with incomplete CG documentation
   - Report on assignment and progress accuracy

4. File System Analysis:
   - Validate documentation file naming and organization
   - Check for required files missing for active issues
   - Identify conflicting or outdated documentation
   - Ensure proper integration with project structure

5. Health Report Generation:
   - Create CG_DOCTOR_REPORT.md with comprehensive findings
   - Prioritize issues by severity and impact
   - Provide specific remediation recommendations
   - Include preventive measures for future health

Scope Focus: ${SCOPE if provided, otherwise 'comprehensive analysis'}
Provide detailed diagnostics and actionable recommendations."
```

## Diagnostic Scopes

### Issues Scope (`/cg-doctor issues`)
Focus specifically on issue-related health:
- Issue state consistency
- Board column accuracy  
- Assignment and progress tracking
- Documentation completeness for active issues

### Tools Scope (`/cg-doctor tools`)
Focus on tool and integration health:
- MCP server connectivity
- Agent availability and functionality
- API access and permissions
- Testing framework integration

### Files Scope (`/cg-doctor files`)
Focus on file system and documentation health:
- Documentation file organization
- Orphaned or misnamed files
- Content consistency and completeness
- Integration with project structure

### Board Scope (`/cg-doctor board`)
Focus on project board health:
- Column organization and rules
- Issue progression accuracy
- Board automation functionality
- State synchronization with development

## Expected Output

### CG_DOCTOR_REPORT.md
Comprehensive health report including:

#### Executive Summary
- Overall workflow health score
- Critical issues requiring immediate attention
- Summary of findings by category
- Recommended priority actions

#### Detailed Findings

**Workflow Issues**:
- Orphaned documentation files
- Inconsistent workflow states
- Incomplete or abandoned work
- Process violations or deviations

**Tool and Integration Issues**:
- Connectivity problems
- Permission or access issues
- Configuration problems
- Performance concerns

**Issue Management Issues**:
- State inconsistencies
- Incorrect board positions
- Assignment problems
- Progress tracking issues

**File System Issues**:
- Organization problems
- Missing required files
- Outdated or conflicting content
- Integration issues

#### Remediation Plan
- Prioritized action items
- Specific commands to fix identified issues
- Prevention strategies
- Recommended workflow improvements

## Automated Fixes

For common issues, the doctor can provide automated fixes:

### Orphaned File Cleanup
```
@agent-cg-implementer "Clean up orphaned CG documentation files:
- Move completed issue documentation to archive
- Remove outdated or conflicting files
- Ensure proper file naming and organization
- Update references and links as needed"
```

### Board State Correction
```
@agent-cg-implementer "Correct GitHub board state inconsistencies:
- Move issues to appropriate columns based on actual progress
- Update assignments and labels as needed
- Ensure board automation rules are functioning
- Synchronize board state with development reality"
```

### Documentation Consistency
```
@agent-cg-implementer "Fix CG documentation consistency issues:
- Update outdated documentation to match current state
- Resolve conflicting information across files
- Ensure documentation follows current standards
- Add missing required documentation for active issues"
```

## Preventive Measures

### Regular Health Checks
- Run `/cg-doctor` weekly on active projects
- Integrate health checks into CI/CD pipeline
- Monitor workflow metrics and trends
- Address issues proactively before they impact development

### Workflow Improvements
- Update CG workflow based on common issues found
- Implement additional validation and safeguards
- Enhance documentation standards and templates
- Improve tool integration and error handling

### Team Training
- Share health report findings with team
- Provide training on common issues and prevention
- Establish best practices based on diagnostic results
- Create workflows for ongoing health maintenance

## Success Criteria

- All critical workflow issues are identified and addressed
- Tool and integration health is validated
- Issue states accurately reflect development progress
- Documentation is consistent, complete, and well-organized
- Preventive measures are in place to maintain workflow health
- Team has clear guidance on maintaining CG workflow quality

## Integration with Other Commands

- Use before starting major development cycles
- Run after significant workflow changes or updates
- Integrate with `/cg-init` for new project setup validation
- Combine with `/cg-resume` for complex context recovery scenarios
- Regular maintenance alongside ongoing `/cg-issue` development