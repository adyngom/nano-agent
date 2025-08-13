# CG Workflow State Template

## Project Overview
- **Name**: [Project Name]
- **Phase**: [Pre-Development|Technical Implementation|Testing|Deployment]
- **PRD**: [PRD_ProjectName.md or N/A]
- **UX Strategy**: [UX_STRATEGY_ProjectName.md or N/A]
- **SaaS Foundation**: [Ready|Setup Required|In Progress]

## Active Development
### Current Issues
- **Issue #[NUMBER]**: [Issue Title]
  - Analysis: [✅ CG_TDD_[NUMBER].md | 🚧 In Progress | ❌ Not Started]
  - Test Plan: [✅ CG_TDD_TESTS_[NUMBER].md | 🚧 In Progress | ❌ Not Started]
  - Implementation: [✅ CG_TDD_IMPLEMENTATION_[NUMBER].md | 🚧 In Progress | ❌ Not Started]
  - Next: [Recommended next agent or action]

## Agent Coordination History
- **Date Time**: @[agent-name] → [Action completed]
- **Date Time**: @[agent-name] → [Action completed]

## Workflow Files

### Pre-Development Phase (Agent 1-4 Sequence)
- [ ] PRD_[ProjectName].md - Business requirements and user personas (Agent 1: @business-analyst-expert)
- [ ] UX_STRATEGY_[ProjectName].md - Design strategy and component planning (Agent 2: @ui-ux-strategy-expert)

### Project Setup Phase  
- [ ] GitHub Issues - Structured issues with epics and dependencies (Agent 3: @project-orchestrator-expert)
- [ ] GitHub Project Board - Configured board with automation rules (Agent 4: @project-board-manager-expert)

### Technical Implementation Phase (CG Agents)
- [ ] CG_TDD_[issue].md - Technical analysis documents (@cg-analyzer)
- [ ] CG_TDD_TESTS_[issue].md - Test strategy documents (@cg-planner)
- [ ] CG_TDD_IMPLEMENTATION_[issue].md - Implementation documentation (@cg-implementer)

### Project State
- [ ] CG_WORKFLOW_STATE.md - This tracking document

## Next Actions
1. [Specific next step with agent recommendation]
2. [Additional steps if applicable]
3. [Future considerations]

## Agent Routing Guide

### Complete TOP_OF_WORKFLOW Sequence
**Reference**: `business_idea → Agent 1 → PRD → Agent 2 → UI/UX Brief → Agent 3 → GitHub Issues → Agent 4 → Project Board → Development`

### New Project Detection (Complete Agent 1-4 Sequence)
If no PRD/UX files exist:
1. Use @cg-init to start project initialization
2. Agent 1: @business-analyst-expert → Creates PRD from business idea
3. Agent 2: @ui-ux-strategy-expert → Creates UX strategy from PRD  
4. Agent 3: @project-orchestrator-expert → Creates GitHub Issues from PRD + UX
5. Agent 4: @project-board-manager-expert → Sets up Project Board from Issues
6. @saas-starter-specialist → Sets up technical foundation
7. **Result**: Ready for development

### Partial Project Continuation
If PRD/UX exist but no GitHub setup:
1. Use @cg-init to assess project state
2. Agent 3: @project-orchestrator-expert → Creates GitHub Issues
3. Agent 4: @project-board-manager-expert → Sets up Project Board
4. **Result**: Ready for technical implementation

### Technical Implementation Flow
If complete pre-development exists:
1. Use @cg-analyzer [issue_number] for technical analysis
2. Use @cg-planner [issue_number] for test strategy
3. Use @cg-implementer [issue_number] for TDD implementation

### Specialized Support
- @cg-doctor - Workflow diagnostics and recovery
- @cg-legacy - Legacy code modernization
- @cg-gemini - Cost-optimized alternative using Google models

## Cost Optimization Notes
- @cg-analyzer uses Claude Opus 4.1 (expensive) - use for deep analysis only
- @cg-planner uses Claude Sonnet 4 (balanced) - optimal for structured planning
- @cg-implementer uses Claude Sonnet 4 (balanced) - good for coding tasks
- @cg-gemini uses Google Gemini models (cost-effective) - budget-friendly alternative

## Integration Points
- GitHub Issues: Link to specific issue numbers
- Project Board: [Board URL if applicable]
- Repository: [Repository URL]
- Documentation: Links to relevant docs

---
**Last Updated**: [Date]
**Updated By**: [Agent that last modified this file]
**Current Phase**: [Current workflow phase]