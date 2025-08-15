# CG Workflow Implementation Plan: Agent-Centric Architecture

## Executive Summary

This document outlines the comprehensive implementation strategy for the Claude-Gemini (CG) Production Workflow system. Built on our proven nano-agent MCP server foundation, this plan delivers a production-ready TDD workflow through **agent creation and coordination**, automated GitHub integration, multi-provider LLM orchestration, and enterprise-grade development processes.

**Modus Operandi**: Agent creation and coordination - users interact via `@agent-name` in Claude Code's interactive environment, with intelligent hooks providing workflow automation and suggestions.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Implementation Phases](#implementation-phases)
3. [Agent Ecosystem Design](#agent-ecosystem-design)
4. [Agent Coordination Framework](#agent-coordination-framework)
5. [File-Based State Management](#file-based-state-management)
6. [Hook Enhancement Strategy](#hook-enhancement-strategy)
7. [GitHub Integration Plan](#github-integration-plan)
8. [Testing Strategy](#testing-strategy)
9. [Risk Assessment & Mitigation](#risk-assessment--mitigation)
10. [Success Metrics](#success-metrics)
11. [Timeline & Milestones](#timeline--milestones)

## Architecture Overview

### Foundation Layer (✅ Complete)
- **Nano-Agent MCP Server**: Multi-provider LLM orchestration
- **Provider Support**: OpenAI, Anthropic, Google Gemini, Ollama
- **Claude Code Integration**: Stable hook system and agent configurations
- **File System Tools**: Complete CRUD operations for documentation generation

### Agent Layer (🎯 Primary Implementation Target)
```
┌─────────────────────────────────────────────┐
│            Claude Code Agents              │
├─────────────────────────────────────────────┤
│ @cg-init    │ @cg-analyzer │ @cg-planner   │
│ @cg-implementer │ @cg-doctor │ @cg-legacy  │
└─────────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────┐
│         Agent Coordination Layer            │
├─────────────────────────────────────────────┤
│ File-Based State │ Context Passing │ Hooks │
│ PRD Files | Analysis Docs | Test Plans     │
└─────────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────┐
│            Nano-Agent MCP Server            │
├─────────────────────────────────────────────┤
│ OpenAI │ Anthropic │ Google │ Ollama       │
│ GPT-5  │ Claude-4  │ Gemini │ Local        │
└─────────────────────────────────────────────┘
```

### Integration Layer (🚧 Hook Enhancement)
- **Session Hooks**: Implicit agent detection and suggestion
- **Post-Tool Hooks**: Agent coordination and workflow automation
- **GitHub API Integration**: Project boards, issues, PRs
- **Documentation Generation**: Automated TDD documentation

## Implementation Phases

### Phase 1: Core Agent Creation (Week 1-2)
**Objective**: Create essential CG workflow agents in `.claude/agents/`

#### 1.1 CG-Init Agent
**Primary Role**: Smart project initialization and workflow routing

```yaml
# .claude/agents/cg-init.md
---
name: cg-init
description: Smart project initialization agent that detects existing PRD/UX files and routes workflow appropriately for new or continuing projects
model: sonnet
color: green
tools: mcp__nano-agent__prompt_nano_agent
---
```

**Agent Responsibilities**:
1. **Project State Detection**:
   - Check for existing `PRD_*.md` and `UX_STRATEGY_*.md` files
   - Assess SaaS foundation status (package.json, framework setup)
   - Determine if starting new project or continuing from pre-development

2. **Workflow Routing**:
   - **New Project**: Collect business idea and coordinate with TOP_OF_WORKFLOW agents
   - **Continuation**: Verify SaaS foundation and proceed to technical implementation
   - **Setup SaaS Foundation**: Use @saas-starter-specialist for foundation setup

3. **Agent Coordination**:
   - Delegate to @business-analyst-expert for PRD creation
   - Hand off to @ui-ux-strategy-expert for design strategy
   - Transition to @cg-analyzer for technical implementation

#### 1.2 CG-Analyzer Agent (CTO-Level Analysis)
**Primary Role**: Comprehensive technical analysis and system impact assessment

```yaml
# .claude/agents/cg-analyzer.md
---
name: cg-analyzer
description: CTO-level analysis agent for comprehensive issue analysis and system impact assessment using Claude Opus 4.1 for maximum reasoning capability
model: claude-opus-4-1-20250805
color: purple
tools: mcp__nano-agent__prompt_nano_agent
---
```

**Output Format**: `CG_TDD_<issue_number>.md`

#### 1.3 CG-Planner Agent (Test Strategy)
**Primary Role**: Comprehensive test strategy development

```yaml
# .claude/agents/cg-planner.md
---
name: cg-planner
description: Senior Test Engineer for comprehensive test strategy development using Claude Sonnet 4 for optimal cost/performance balance
model: claude-sonnet-4-20250514
color: blue
tools: mcp__nano-agent__prompt_nano_agent
---
```

**Output Format**: `CG_TDD_TESTS_<issue_number>.md`

#### 1.4 CG-Implementer Agent (TDD Development)
**Primary Role**: Senior developer with access to specialized agents

```yaml
# .claude/agents/cg-implementer.md
---
name: cg-implementer
description: Senior Developer for TDD implementation with access to all specialized agents using Claude Sonnet 4 for optimal coding capability
model: claude-sonnet-4-20250514
color: orange
tools: mcp__nano-agent__prompt_nano_agent
---
```

**Agent Access**: Can coordinate with specialized agents:
- @gemini-security-agent for security reviews
- @architecture-reviewer for code quality
- @claude-git-assistant for commit automation

### Phase 2: Agent Coordination Framework (Week 2-3)

#### 2.1 File-Based State Management
**Coordination Mechanism**: Agents coordinate through structured markdown files

```
Workflow State Files:
├── PRD_<project>.md              # Business requirements (from pre-dev)
├── UX_STRATEGY_<project>.md      # Design strategy (from pre-dev)
├── CG_TDD_<issue>.md            # Technical analysis (from @cg-analyzer)
├── CG_TDD_TESTS_<issue>.md      # Test strategy (from @cg-planner)
├── CG_TDD_IMPLEMENTATION_<issue>.md # Implementation docs (from @cg-implementer)
└── CG_WORKFLOW_STATE.md         # Overall workflow state tracking
```

#### 2.2 Agent Handoff Protocol
```markdown
## Agent Coordination Pattern

### User Intent Detection
User: "I want to build a freelancer invoice platform"
↓
Session Hook detects → Suggests @cg-init
↓
@cg-init analyzes project state

### New Project Flow
@cg-init → No existing PRD/UX files found
↓
@cg-init → Coordinates with @business-analyst-expert (PRD creation)
↓
@business-analyst-expert → Creates PRD_FreelancerInvoice.md
↓
@cg-init → Coordinates with @ui-ux-strategy-expert (Design strategy)
↓
@ui-ux-strategy-expert → Creates UX_STRATEGY_FreelancerInvoice.md
↓
@cg-init → Ready for technical implementation

### Technical Implementation Flow
User: "@cg-analyzer <issue_number>"
↓
@cg-analyzer → Reads PRD + UX files → Creates CG_TDD_<issue>.md
↓
User: "@cg-planner <issue_number>"
↓
@cg-planner → Reads analysis → Creates CG_TDD_TESTS_<issue>.md
↓
User: "@cg-implementer <issue_number>"
↓
@cg-implementer → Reads analysis + tests → Implements feature + documentation
```

#### 2.3 Context Preservation Strategy
```python
# Agent context reading pattern
class AgentContextManager:
    def load_workflow_context(self, issue_number: Optional[int] = None):
        context = {
            "prd_files": glob.glob("PRD_*.md"),
            "ux_files": glob.glob("UX_STRATEGY_*.md"),
            "project_state": self.detect_project_state(),
            "saas_foundation": self.check_saas_foundation()
        }
        
        if issue_number:
            context.update({
                "analysis": f"CG_TDD_{issue_number}.md",
                "test_plan": f"CG_TDD_TESTS_{issue_number}.md",
                "implementation": f"CG_TDD_IMPLEMENTATION_{issue_number}.md"
            })
        
        return context
```

### Phase 3: Hook Enhancement (Week 2-3)

#### 3.1 Implicit Agent Detection
```python
# .claude/hooks/session_start.py (enhanced)
async def handle_session_start(user_message: str):
    # Detect implicit cg-init triggers
    init_patterns = [
        r"i want to build",
        r"help me create a saas",
        r"let's start a new project",
        r"build me a platform for"
    ]
    
    if any(re.search(pattern, user_message, re.IGNORECASE) for pattern in init_patterns):
        return {
            "suggestion": "It looks like you want to start a new project. Try using @cg-init to begin the CG workflow.",
            "auto_invoke_agent": "cg-init",
            "context": {"user_idea": user_message}
        }
    
    # Detect issue development patterns
    issue_patterns = [
        r"implement.*issue\s+(\d+)",
        r"work on.*#(\d+)",
        r"start.*feature.*(\d+)"
    ]
    
    for pattern in issue_patterns:
        match = re.search(pattern, user_message, re.IGNORECASE)
        if match:
            issue_number = match.group(1)
            return {
                "suggestion": f"Ready to work on issue #{issue_number}? Use @cg-analyzer {issue_number} to start the technical analysis.",
                "auto_invoke_agent": "cg-analyzer",
                "context": {"issue_number": issue_number}
            }
    
    return None
```

#### 3.2 Agent Coordination Hooks
```python
# .claude/hooks/post_tool_use.py (enhanced)
async def handle_post_tool_use(tool_name: str, result: dict):
    if tool_name == "mcp__nano-agent__prompt_nano_agent":
        # Check if this was a CG agent execution
        if "CG_TDD_" in str(result.get("files_created", [])):
            # Suggest next agent in workflow
            if "CG_TDD_TESTS_" not in str(result.get("files_created", [])):
                return {
                    "suggestion": "Analysis complete! Next, use @cg-planner to create the test strategy.",
                    "next_agent": "cg-planner"
                }
            elif "CG_TDD_IMPLEMENTATION_" not in str(result.get("files_created", [])):
                return {
                    "suggestion": "Test strategy ready! Now use @cg-implementer to begin TDD implementation.",
                    "next_agent": "cg-implementer"
                }
    
    return None
```

### Phase 4: Advanced Agent Features (Week 3-4)

#### 4.1 CG-Doctor Agent (Workflow Diagnostics)
**Primary Role**: Diagnose and resolve workflow issues

```yaml
# .claude/agents/cg-doctor.md
---
name: cg-doctor
description: Workflow diagnostics and recovery specialist that analyzes CG workflow state and resolves issues
model: sonnet
color: red
tools: mcp__nano-agent__prompt_nano_agent
---
```

**Diagnostic Capabilities**:
- Detect incomplete workflows
- Identify missing documentation
- Validate agent coordination state
- Suggest recovery actions

#### 4.2 CG-Legacy Agent (Legacy Code Modernization)
**Primary Role**: Retrofit existing codebases with TDD

```yaml
# .claude/agents/cg-legacy.md
---
name: cg-legacy
description: Legacy code modernization specialist that adds TDD practices to existing codebases
model: sonnet
color: yellow
tools: mcp__nano-agent__prompt_nano_agent
---
```

**Modernization Workflow**:
1. Scan codebase for untested files
2. Prioritize by risk and complexity
3. Generate test strategies for existing code
4. Create modernization roadmap

#### 4.3 Agent Specialization Integration
**Cost-Optimized Model Selection**:
```yaml
Agent Model Strategy:
├── @cg-init: sonnet (balanced capability for routing)
├── @cg-analyzer: opus (maximum reasoning for architecture)
├── @cg-planner: sonnet (structured planning)
├── @cg-implementer: sonnet (coding with agent coordination)
├── @cg-doctor: sonnet (diagnostic analysis)
└── Security Reviews: gemini (cost-effective specialized analysis)
```

## Agent Ecosystem Design

### Core Agent Specifications

#### Agent Frontmatter Standard
```yaml
---
name: agent-name
description: Clear description with specific use cases and coordination capabilities
model: opus|sonnet|gemini
color: blue|purple|green|orange|red|yellow
tools: mcp__nano-agent__prompt_nano_agent
---
```

#### Agent System Prompt Pattern
```markdown
You are a [ROLE] specializing in [DOMAIN]. Your role in the CG workflow is to [SPECIFIC_RESPONSIBILITY].

## Context Awareness
Always start by reading relevant workflow files:
- PRD_*.md files for business context
- UX_STRATEGY_*.md files for design context  
- CG_TDD_*.md files for technical context
- Previous agent outputs for coordination

## Coordination Protocol
- Read context from existing workflow files
- Generate structured output in specified format
- Suggest next agent or workflow step
- Preserve workflow state in generated documentation

## Output Requirements
Generate documentation following the [TEMPLATE_NAME] format with:
1. Clear analysis and recommendations
2. Actionable next steps
3. References to supporting context
4. Coordination suggestions for user
```

### Agent Interaction Patterns

#### Sequential Workflow Pattern
```
@cg-init → Project routing and foundation setup
     ↓
@business-analyst-expert → PRD creation (if new project)
     ↓
@ui-ux-strategy-expert → Design strategy (if new project)  
     ↓
@cg-analyzer → Technical analysis for specific issue
     ↓
@cg-planner → Test strategy development
     ↓
@cg-implementer → TDD implementation with specialized agent coordination
```

#### Parallel Workflow Pattern
```
@cg-implementer coordinates with:
├── @gemini-security-agent (security review)
├── @architecture-reviewer (code quality review)
├── @claude-git-assistant (commit automation)
└── @error-pattern-analyzer (debugging support)
```

## File-Based State Management

### Workflow State Files

#### PRD Format (from TOP_OF_WORKFLOW)
```markdown
# Product Requirements Document: [Project Name]

## Executive Summary
- Business opportunity and market validation
- User personas and target audience
- Success metrics and KPIs

## Feature Specifications  
- Core features with acceptance criteria
- Technical requirements and constraints
- Integration requirements

## Implementation Guidance
- Recommended technology stack
- SaaS Starter integration plan
- Development timeline
```

#### CG Analysis Format
```markdown
# Technical Analysis: [Issue Title]

## System Impact Assessment
- Affected components and integration points
- Data flow changes and implications
- Performance and security considerations

## Architecture Strategy
- Recommended design patterns
- Code organization approach  
- Dependency management

## Implementation Plan
- Development phases and dependencies
- Testing requirements
- Risk assessment and mitigation
```

#### CG Test Strategy Format
```markdown
# Test Strategy: [Issue Title]

## Test Categories
- Unit test specifications
- Integration test requirements
- End-to-end test scenarios

## Implementation Plan
- TDD implementation order
- Mock and test data requirements
- Success criteria and coverage goals

## Quality Gates
- Test validation checkpoints
- Performance benchmarks
- Security test requirements
```

### State Tracking System
```markdown
# CG_WORKFLOW_STATE.md

## Current Project State
- **Project**: [Name]
- **Phase**: [Pre-Development|Technical Implementation|Testing|Deployment]
- **Active Issues**: [List with status]
- **Next Actions**: [Recommended steps]

## Workflow History
- Agent executions and outputs
- Decision points and rationale
- Context handoffs and coordination

## Agent Coordination Log
- Agent interactions and dependencies
- File generation and updates
- Workflow progression tracking
```

## Hook Enhancement Strategy

### Session Hook Enhancements
```python
# Intelligent agent suggestion system
class AgentSuggestionEngine:
    def analyze_user_intent(self, message: str) -> AgentSuggestion:
        # Business idea detection
        if self.is_business_idea(message):
            return AgentSuggestion(
                agent="cg-init", 
                reason="New project initialization needed",
                context={"user_idea": message}
            )
        
        # Technical work detection  
        if self.is_technical_request(message):
            return AgentSuggestion(
                agent="cg-analyzer",
                reason="Technical analysis required",
                context=self.extract_technical_context(message)
            )
        
        # Workflow continuation detection
        if self.is_workflow_continuation(message):
            return self.suggest_next_workflow_step()
        
        return None
```

### Post-Tool-Use Automation
```python
# Workflow progression automation
class WorkflowProgressionEngine:
    def handle_agent_completion(self, agent: str, output: dict):
        if agent == "cg-analyzer" and "CG_TDD_" in output.files:
            return WorkflowSuggestion(
                message="Technical analysis complete. Next step: @cg-planner for test strategy.",
                auto_suggest_agent="cg-planner"
            )
        
        if agent == "cg-planner" and "CG_TDD_TESTS_" in output.files:
            return WorkflowSuggestion(
                message="Test strategy ready. Next step: @cg-implementer for TDD development.",
                auto_suggest_agent="cg-implementer"
            )
        
        return None
```

## GitHub Integration Plan

### Agent-Driven GitHub Integration
Rather than command-based GitHub operations, agents coordinate GitHub interactions through the nano-agent system:

#### GitHub Integration Agents
```yaml
# Specialized agents for GitHub operations
├── @github-issue-manager: Issue lifecycle management
├── @github-board-manager: Project board automation  
├── @github-pr-manager: Pull request automation
└── @github-workflow-manager: CI/CD and action coordination
```

#### Issue Lifecycle Integration
```python
# @cg-analyzer coordinates with GitHub
async def analyze_issue(self, issue_number: int):
    # Fetch issue details via nano-agent GitHub integration
    issue_data = await self.fetch_github_issue(issue_number)
    
    # Perform technical analysis
    analysis = await self.perform_analysis(issue_data)
    
    # Update GitHub issue with analysis
    await self.update_github_issue(issue_number, {
        "labels": ["analysis-complete"],
        "comment": "Technical analysis completed. See CG_TDD_{issue_number}.md"
    })
    
    # Move on project board
    await self.move_board_card(issue_number, "Analysis", "Implementation")
```

### Project Board Automation
**Board Structure**: Sprint Planning → Analysis → Implementation → Testing → Code Review → E2E Testing → Done

**Agent-Driven Transitions**:
- @cg-analyzer completion → Move to Implementation
- @cg-planner completion → Ready for TDD development  
- @cg-implementer completion → Move to Testing
- Test validation → Move to Code Review

## Testing Strategy

### Agent Testing Framework
```python
# Agent behavior testing
class CGAgentTestSuite:
    async def test_cg_init_new_project(self):
        # Test @cg-init behavior with no existing files
        result = await self.invoke_agent("cg-init", context={
            "user_message": "I want to build a task management app"
        })
        
        assert "business-analyst-expert" in result.suggested_agents
        assert result.workflow_phase == "pre-development"
    
    async def test_cg_init_continuation(self):
        # Test @cg-init behavior with existing PRD/UX files
        self.create_mock_files(["PRD_TaskApp.md", "UX_STRATEGY_TaskApp.md"])
        
        result = await self.invoke_agent("cg-init")
        
        assert result.workflow_phase == "technical-implementation"
        assert "cg-analyzer" in result.suggested_agents
    
    async def test_agent_coordination(self):
        # Test full agent workflow coordination
        workflow_result = await self.execute_agent_sequence([
            ("cg-analyzer", {"issue_number": 1}),
            ("cg-planner", {"issue_number": 1}), 
            ("cg-implementer", {"issue_number": 1})
        ])
        
        assert all(doc in workflow_result.generated_files for doc in [
            "CG_TDD_1.md", "CG_TDD_TESTS_1.md", "CG_TDD_IMPLEMENTATION_1.md"
        ])
```

### Integration Testing Scenarios
1. **Complete New Project Flow**: Business idea → PRD → UX → Technical implementation
2. **Project Continuation Flow**: Existing PRD/UX → Technical analysis → Implementation
3. **Agent Coordination Flow**: Sequential agent execution with proper context passing
4. **Error Recovery Flow**: @cg-doctor diagnosis and workflow recovery
5. **Legacy Integration Flow**: @cg-legacy modernization of existing code

## Risk Assessment & Mitigation

### Agent Coordination Risks

#### Risk: Agent Context Loss
**Probability**: Medium  
**Impact**: High  
**Mitigation**:
- Robust file-based state management
- Context validation in each agent
- Workflow state tracking and recovery
- @cg-doctor for state diagnosis

#### Risk: User Workflow Confusion
**Probability**: Medium  
**Impact**: Medium  
**Mitigation**:
- Clear agent descriptions and use cases
- Intelligent hook suggestions
- Workflow progression guidance
- Comprehensive documentation

#### Risk: Agent Execution Performance
**Probability**: Low  
**Impact**: Medium  
**Mitigation**:
- Optimized model selection per agent
- Efficient nano-agent coordination
- Caching for repeated operations
- Performance monitoring

### Technical Implementation Risks

#### Risk: Hook Integration Complexity
**Probability**: Medium  
**Impact**: Medium  
**Mitigation**:
- Start with basic hook enhancements
- Incremental feature addition
- Fallback to manual agent invocation
- User feedback integration

#### Risk: File-Based State Management
**Probability**: Low  
**Impact**: Medium  
**Mitigation**:
- Structured markdown format validation
- State consistency checking
- Backup and recovery mechanisms
- @cg-doctor for state repair

## Success Metrics

### Agent Performance Metrics
- **Agent Response Quality**: User satisfaction >8/10
- **Workflow Completion Rate**: >90% successful end-to-end workflows
- **Context Preservation**: >95% accurate context handoffs
- **User Guidance**: <5% user workflow confusion incidents

### Development Efficiency Metrics
- **Time to Analysis**: <5 minutes for issue analysis
- **Documentation Quality**: 100% of features documented via agents
- **Workflow Adherence**: >95% TDD workflow compliance
- **Agent Coordination**: <2% coordination failures

### Cost Optimization Metrics
- **Model Selection Efficiency**: 80% cost reduction via strategic model use
- **Agent Specialization**: 60% faster task completion vs. general agents
- **Workflow Automation**: 70% reduction in manual coordination overhead

## Timeline & Milestones

### Week 1-2: Core Agent Creation
- [ ] **Day 1-3**: Create @cg-init, @cg-analyzer, @cg-planner agents
- [ ] **Day 4-7**: Create @cg-implementer, @cg-doctor agents  
- [ ] **Day 8-14**: Test basic agent functionality and coordination

**Milestone**: Core CG agents functional and tested

### Week 2-3: Agent Coordination Framework
- [ ] **Day 15-21**: Implement file-based state management
- [ ] **Day 22-28**: Enhance session and post-tool hooks

**Milestone**: Agent coordination system operational

### Week 3-4: Advanced Features
- [ ] **Day 29-35**: Create @cg-legacy and specialized agents
- [ ] **Day 36-42**: Integrate GitHub automation via agents

**Milestone**: Complete agent ecosystem with automation

### Week 4-5: Testing & Integration
- [ ] **Day 43-49**: Comprehensive agent testing
- [ ] **Day 50-56**: User workflow testing and refinement

**Milestone**: Production-ready agent system

### Week 5-6: Documentation & Training
- [ ] **Day 57-63**: User documentation and examples
- [ ] **Day 64-70**: Team training and feedback integration

**Milestone**: Ready for team adoption

## Repository Structure

```
nano-agent/
├── .claude/
│   ├── agents/                         # CG Agent Configurations
│   │   ├── cg-init.md                 # Project initialization
│   │   ├── cg-analyzer.md             # Technical analysis
│   │   ├── cg-planner.md              # Test strategy
│   │   ├── cg-implementer.md          # TDD implementation
│   │   ├── cg-doctor.md               # Workflow diagnostics
│   │   ├── cg-legacy.md               # Legacy modernization
│   │   └── specialized/               # Specialized agents
│   ├── hooks/                         # Enhanced Hooks
│   │   ├── session_start.py           # Agent suggestion
│   │   ├── post_tool_use.py           # Workflow coordination
│   │   └── agent_coordination.py      # Agent handoff logic
│   └── settings.json                  # Claude Code configuration
├── apps/nano_agent_mcp_server/        # Existing MCP server
├── docs/                              # Generated documentation
│   ├── agent_guides/                  # Agent usage guides
│   ├── workflow_examples/             # Example workflows
│   └── troubleshooting/               # Common issues
├── tests/
│   ├── agent_tests/                   # Individual agent tests
│   ├── coordination_tests/            # Agent coordination tests
│   └── integration_tests/             # End-to-end workflow tests
└── examples/
    ├── sample_projects/               # Example project flows
    ├── prd_examples/                  # Sample PRDs and outputs
    └── workflow_demos/                # Complete workflow examples
```

## Next Steps

### Immediate Actions (This Week)
1. **Agent Creation**: Start with @cg-init, @cg-analyzer, @cg-planner
2. **File-Based State**: Implement workflow state management
3. **Basic Coordination**: Test agent handoff via file context
4. **Hook Enhancement**: Add intelligent agent suggestions

### Phase 1 Deliverables (Next 2 Weeks)  
1. **Functional Agents**: @cg-init through @cg-implementer working
2. **Agent Coordination**: File-based context passing operational
3. **Hook Integration**: Session hooks suggesting appropriate agents
4. **Documentation Templates**: Standard formats for all workflow files

### Success Criteria for Phase 1
- [ ] Agents execute without errors
- [ ] Context preservation across agent handoffs
- [ ] Intelligent agent suggestions working
- [ ] File-based state management functional
- [ ] Basic workflow coordination operational

---

## Appendices

### A. Agent Usage Patterns

#### New Project Initiation
```
User: "I want to build a project management SaaS"
Hook: Suggests @cg-init
@cg-init: Detects no existing files → Coordinates with pre-dev agents
Result: PRD and UX strategy files created → Ready for @cg-analyzer
```

#### Technical Implementation
```
User: "@cg-analyzer 123"
@cg-analyzer: Reads PRD/UX context → Creates CG_TDD_123.md
Hook: Suggests @cg-planner
@cg-planner: Reads analysis → Creates CG_TDD_TESTS_123.md  
Hook: Suggests @cg-implementer
@cg-implementer: Reads analysis + tests → Implements feature
```

#### Legacy Code Modernization
```
User: "@cg-legacy"
@cg-legacy: Scans codebase → Creates modernization plan
Result: Test strategies for existing code → Integration with TDD workflow
```

### B. Agent Prompt Templates

#### Standard Agent Context Loading
```markdown
## Context Loading Protocol
Before beginning your task, read and analyze these workflow files:
1. PRD_*.md - Business requirements and user personas
2. UX_STRATEGY_*.md - Design strategy and component planning
3. CG_TDD_*.md - Previous technical analysis (if continuing workflow)
4. CG_WORKFLOW_STATE.md - Current workflow state and history

## Output Requirements
Generate structured documentation following the specified format:
- Clear analysis and recommendations
- References to supporting context files
- Actionable next steps for user
- Coordination suggestions for subsequent agents
```

### C. Workflow State Examples

#### CG_WORKFLOW_STATE.md Template
```markdown
# CG Workflow State

## Project Overview
- **Name**: TaskFlow Pro
- **Phase**: Technical Implementation
- **PRD**: PRD_TaskFlowPro.md
- **UX Strategy**: UX_STRATEGY_TaskFlowPro.md

## Active Development
- **Issue #123**: User authentication system
  - Analysis: ✅ CG_TDD_123.md
  - Test Plan: ✅ CG_TDD_TESTS_123.md
  - Implementation: 🚧 In Progress
  - Next: @cg-implementer coordination

## Agent Coordination History
- 2025-08-13 10:30: @cg-init → Project initialization
- 2025-08-13 11:00: @business-analyst-expert → PRD creation
- 2025-08-13 14:30: @ui-ux-strategy-expert → Design strategy
- 2025-08-13 15:00: @cg-analyzer → Technical analysis for issue #123
- 2025-08-13 15:30: @cg-planner → Test strategy for issue #123

## Next Actions
1. Complete @cg-implementer for issue #123
2. Begin @cg-analyzer for issue #124 (Dashboard component)
3. Schedule @cg-legacy for existing user management code
```

---

**Document Version**: 2.0 (Agent-Centric Revision)  
**Last Updated**: 2025-08-13  
**Status**: Ready for Implementation  
**Architecture**: Agent Creation and Coordination  

This revised implementation plan focuses on **agent creation and coordination** as the primary modus operandi, leveraging Claude Code's interactive environment with intelligent workflow automation through hooks and file-based state management.