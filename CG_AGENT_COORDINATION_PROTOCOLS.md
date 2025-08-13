# CG Agent Coordination Protocols

## Overview

This document defines the coordination protocols for CG workflow agents, ensuring seamless handoffs and consistent state management across the agent ecosystem.

## File-Based State Management

### Core Principle
Agents coordinate through structured markdown files rather than direct communication. Each agent reads context from existing files and generates new files for subsequent agents.

### Workflow State Files

#### Pre-Development Phase (Agent 1-4 Outputs)
```
PRD_<ProjectName>.md              # Business requirements (from @business-analyst-expert - Agent 1)
UX_STRATEGY_<ProjectName>.md      # Design strategy (from @ui-ux-strategy-expert - Agent 2)
```

#### Project Setup Phase (Agent 3-4 Outputs)
```
GitHub Issues                     # Structured issues with epics (from @project-orchestrator-expert - Agent 3)
GitHub Project Board              # Configured board with automation (from @project-board-manager-expert - Agent 4)
```

#### Technical Implementation Phase (CG Agents)
```
CG_TDD_<issue>.md                 # Technical analysis (from @cg-analyzer)
CG_TDD_TESTS_<issue>.md           # Test strategy (from @cg-planner)
CG_TDD_IMPLEMENTATION_<issue>.md  # Implementation docs (from @cg-implementer)
```

#### State Tracking
```
CG_WORKFLOW_STATE.md              # Overall workflow state and coordination log
```

## Agent Coordination Patterns

### Complete TOP_OF_WORKFLOW Sequence
**Reference**: `business_idea → Agent 1 → PRD → Agent 2 → UI/UX Brief → Agent 3 → GitHub Issues → Agent 4 → Project Board → Development`

### 1. Project Initialization Flow

#### @cg-init (Project Router) - **Agent 0: Workflow Orchestrator**
**Input**: User request or project directory
**Context Reading**:
- Check for existing PRD_*.md files
- Check for existing UX_STRATEGY_*.md files
- Check for GitHub Issues and Project Board setup
- Assess SaaS foundation (package.json, framework files)

**Decision Logic**:
```markdown
IF no PRD/UX files exist:
  → Route to complete pre-development workflow
  → Step 1: Coordinate with @business-analyst-expert (Agent 1)
  → Step 2: Coordinate with @ui-ux-strategy-expert (Agent 2)  
  → Step 3: Coordinate with @project-orchestrator-expert (Agent 3)
  → Step 4: Coordinate with @project-board-manager-expert (Agent 4)
  → Step 5: Setup SaaS foundation via @saas-starter-specialist
  → Result: Ready for development

ELSE IF PRD/UX exist but no GitHub setup:
  → Route to project setup workflow
  → Step 3: @project-orchestrator-expert for GitHub Issues
  → Step 4: @project-board-manager-expert for Project Board
  → Result: Ready for technical implementation

ELSE IF complete pre-development exists:
  → Route to technical implementation
  → Suggest @cg-analyzer for issue analysis
```

**Output**: Project state assessment and complete workflow routing

### 2. Complete Pre-Development Workflow (Agent 1-4 Sequence)

#### Agent 1: @business-analyst-expert (PRD Creation)
**Input**: Business idea from user
**Processing**: Market research, user personas, feature specifications
**Output**: PRD_[ProjectName].md with comprehensive business requirements
**Next Agent**: @ui-ux-strategy-expert (Agent 2)

#### Agent 2: @ui-ux-strategy-expert (UI/UX Brief Creation)  
**Input**: PRD_[ProjectName].md
**Context Reading**: Business requirements and user personas
**Processing**: Design strategy, component planning, user experience architecture
**Output**: UX_STRATEGY_[ProjectName].md with complete design brief
**Next Agent**: @project-orchestrator-expert (Agent 3)

#### Agent 3: @project-orchestrator-expert (GitHub Issues Creation)
**Input**: PRD + UX Strategy documents
**Context Reading**: 
- PRD_[ProjectName].md for feature requirements
- UX_STRATEGY_[ProjectName].md for design specifications
**Processing**: Break down features into structured GitHub issues with dependencies
**Output**: 
- Complete GitHub issues with acceptance criteria
- Epic organization and milestone planning
- Dependency mapping between issues
**Next Agent**: @project-board-manager-expert (Agent 4)

#### Agent 4: @project-board-manager-expert (Project Board Creation)
**Input**: GitHub issues and epic structure
**Context Reading**: Created GitHub issues and project requirements
**Processing**: 
- Configure GitHub project board with workflow columns
- Set up automation rules and transitions
- Create multi-view dashboards for different stakeholders
**Output**: 
- Fully configured GitHub project board
- Automated workflow rules
- Team access and notification setup
**Result**: **Ready for Development Phase**

### 3. Technical Implementation Flow (Post-Setup)

#### @cg-analyzer (Technical Analysis)
**Input**: GitHub issue number or feature request
**Context Reading**:
- PRD_*.md files for business context
- UX_STRATEGY_*.md files for design context
- Existing CG_TDD_*.md files for previous analysis

**Processing**: CTO-level technical analysis and system impact assessment
**Output**: CG_TDD_<issue>.md with comprehensive technical analysis
**Next Agent Suggestion**: @cg-planner for test strategy development

#### @cg-planner (Test Strategy)
**Input**: Issue number and reference to analysis
**Context Reading**:
- CG_TDD_<issue>.md for technical analysis
- PRD/UX files for business and design context

**Processing**: Comprehensive test strategy development
**Output**: CG_TDD_TESTS_<issue>.md with complete test plan
**Next Agent Suggestion**: @cg-implementer for TDD implementation

#### @cg-implementer (TDD Implementation)
**Input**: Issue number and reference to analysis + test plan
**Context Reading**:
- CG_TDD_<issue>.md for technical analysis
- CG_TDD_TESTS_<issue>.md for test strategy
- PRD/UX files for full context

**Processing**: TDD implementation with specialized agent coordination
**Output**: CG_TDD_IMPLEMENTATION_<issue>.md with implementation details
**Specialized Agent Coordination**:
- @gemini-security-agent for security reviews
- @architecture-reviewer for code quality
- @claude-git-assistant for commit automation

## Context Loading Protocol

### Standard Context Reading Pattern
Every agent should follow this context loading pattern:

```markdown
## Context Loading Checklist
Before beginning your task, read and analyze these workflow files:

1. **Business Context**: PRD_*.md files
   - User personas and requirements
   - Business objectives and constraints
   - Success metrics and KPIs

2. **Design Context**: UX_STRATEGY_*.md files  
   - Design strategy and visual direction
   - Component library requirements
   - User experience architecture

3. **Technical Context**: CG_TDD_*.md files
   - Previous technical analysis (if continuing workflow)
   - Architecture decisions and patterns
   - System impact assessments

4. **Workflow State**: CG_WORKFLOW_STATE.md
   - Current project phase and status
   - Agent coordination history
   - Next recommended actions

## Context Validation
- Confirm all relevant context files are present
- Validate file content is complete and recent
- Identify any missing context that needs clarification
```

### Context Preservation Requirements
```markdown
## Output Requirements for Context Preservation
Each agent must generate output that preserves context for subsequent agents:

1. **Reference Source Context**: Clearly reference which files were read for context
2. **Decision Rationale**: Explain decisions made based on context
3. **Coordination Suggestions**: Recommend next agents and workflow steps
4. **State Updates**: Update CG_WORKFLOW_STATE.md with progress
```

## Agent Handoff Specifications

### Handoff Validation Checklist
Before completing execution, each agent should:

- [ ] Generated required output file in correct format
- [ ] Referenced all relevant context files in output
- [ ] Provided clear next steps and agent recommendations
- [ ] Updated CG_WORKFLOW_STATE.md with progress
- [ ] Validated output completeness and accuracy

### Next Agent Suggestions Format
```markdown
## Next Steps and Agent Coordination
Based on this [analysis/planning/implementation], the recommended next steps are:

1. **Immediate Next Agent**: @[agent-name] [specific-task]
   - **Context**: This agent should read [specific files]
   - **Focus**: [specific areas of focus]
   - **Expected Output**: [what should be generated]

2. **Alternative Approaches**: 
   - @[alternative-agent] for [specific scenario]
   - @[specialized-agent] if [specific conditions]

3. **Quality Assurance**:
   - Consider @[review-agent] for [specific review type]
   - Validate with @[testing-agent] for [specific validation]
```

## Error Recovery and Diagnostics

### @cg-doctor (Workflow Diagnostics)
**Triggers for Use**:
- Workflow appears stuck or incomplete
- Missing expected output files
- Agent coordination failures
- Context inconsistencies

**Diagnostic Capabilities**:
- Analyze workflow state and identify issues
- Validate file completeness and consistency
- Suggest recovery actions and next steps
- Repair workflow state if possible

## State Consistency Rules

### File Naming Conventions
- **PRD files**: PRD_[ProjectName].md (PascalCase, no spaces)
- **UX files**: UX_STRATEGY_[ProjectName].md (consistent with PRD naming)
- **Analysis files**: CG_TDD_[IssueNumber].md (numbers only)
- **Test files**: CG_TDD_TESTS_[IssueNumber].md (consistent with analysis)
- **Implementation files**: CG_TDD_IMPLEMENTATION_[IssueNumber].md

### State Update Requirements
Every agent execution should:
1. Update CG_WORKFLOW_STATE.md with progress
2. Log agent execution with timestamp
3. Update next actions based on completion
4. Maintain coordination history

### Consistency Validation
Agents should validate:
- File naming consistency
- Cross-references between files
- Workflow progression logic
- Context completeness

## Hook Integration Points

### Session Start Hook
```python
# Detect user intent and suggest appropriate agent
patterns = {
    "new_project": r"i want to build|help me create|let's start",
    "issue_work": r"implement.*issue\s+(\d+)|work on.*#(\d+)",
    "legacy_work": r"modernize|add tests to|legacy code"
}

suggestions = {
    "new_project": "@cg-init",
    "issue_work": "@cg-analyzer",
    "legacy_work": "@cg-legacy"
}
```

### Post-Tool-Use Hook
```python
# Suggest next agent based on completed work
if "CG_TDD_" in files_created and "CG_TDD_TESTS_" not in files_created:
    suggest_agent = "@cg-planner"
elif "CG_TDD_TESTS_" in files_created and "CG_TDD_IMPLEMENTATION_" not in files_created:
    suggest_agent = "@cg-implementer"
```

## Best Practices

### Agent Design Principles
1. **Single Responsibility**: Each agent has a clear, focused role
2. **Context Awareness**: Always read relevant context before processing
3. **State Preservation**: Generate complete output for subsequent agents
4. **Clear Handoffs**: Provide specific next steps and recommendations
5. **Error Transparency**: Clear error reporting and recovery suggestions

### Coordination Efficiency
1. **Batch Context Reading**: Read all relevant files at once
2. **Complete Output**: Generate all required files in single execution
3. **Clear Dependencies**: Explicitly state what context is required
4. **Validation**: Verify output completeness before finishing

### Cost Optimization
1. **Model Selection**: Use appropriate model for task complexity
2. **Context Efficiency**: Read only necessary context files
3. **Batch Operations**: Combine related tasks when possible
4. **Alternative Agents**: Suggest cost-effective alternatives when appropriate

---

This coordination protocol ensures consistent, efficient, and reliable agent coordination throughout the CG workflow, maintaining context and state across all phases of development.