# CG Workflow Implementation Plan

## Executive Summary

This document outlines the comprehensive implementation strategy for the Claude-Gemini (CG) Production Workflow system. Built on our proven nano-agent MCP server foundation, this plan delivers a production-ready TDD workflow with automated GitHub integration, multi-provider LLM orchestration, and enterprise-grade development processes.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Implementation Phases](#implementation-phases)
3. [Technical Requirements](#technical-requirements)
4. [Command Implementation Strategy](#command-implementation-strategy)
5. [Testing Strategy](#testing-strategy)
6. [GitHub Integration Plan](#github-integration-plan)
7. [Agent Specialization Framework](#agent-specialization-framework)
8. [Risk Assessment & Mitigation](#risk-assessment--mitigation)
9. [Success Metrics](#success-metrics)
10. [Timeline & Milestones](#timeline--milestones)

## Architecture Overview

### Foundation Layer (✅ Complete)
- **Nano-Agent MCP Server**: Multi-provider LLM orchestration
- **Provider Support**: OpenAI, Anthropic, Google Gemini, Ollama
- **Claude Code Integration**: Stable hook system and agent configurations
- **File System Tools**: Complete CRUD operations for documentation generation

### Command Layer (🚧 Implementation Target)
```
┌─────────────────────────────────────────────┐
│               CG Commands                   │
├─────────────────────────────────────────────┤
│ /cg-init     │ /cg-issue    │ /cg-legacy   │
│ /cg-resume   │ /cg-doctor   │ /cg-test     │
│ /cg-push     │ /cg-security │ /cg-analyze  │
└─────────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────┐
│            Agent Orchestration              │
├─────────────────────────────────────────────┤
│ cg-analyzer  │ cg-planner   │ cg-implementer│
│ (Opus 4.1)   │ (Sonnet 4)   │ (Sonnet 4)   │
└─────────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────────┐
│            Nano-Agent MCP Server            │
├─────────────────────────────────────────────┤
│ OpenAI │ Anthropic │ Google │ Ollama       │
│ GPT-5  │ Claude-4  │ Gemini │ Local        │
└─────────────────────────────────────────────┘
```

### Integration Layer (🎯 New Implementation)
- **GitHub API Integration**: Project boards, issues, PRs
- **Test Framework Detection**: Jest, PyTest, Go Test, etc.
- **Documentation Generation**: Automated TDD documentation
- **State Management**: Workflow state persistence and recovery

## Implementation Phases

### Phase 1: Command Framework Foundation (Week 1-2)
**Objective**: Establish the `/cg-*` command parsing and execution framework

#### 1.1 Claude Code Command Integration
- **Challenge**: Claude Code doesn't natively support custom slash commands
- **Solution**: Implement command detection via Claude Code agents and hooks
- **Approach**: 
  ```javascript
  // Session start hook pattern matching
  if (userMessage.startsWith('/cg-')) {
    const command = parseCommand(userMessage);
    await executeWorkflowCommand(command);
  }
  ```

#### 1.2 Command Parser Implementation
```python
# apps/cg_workflow/src/command_parser.py
class CGCommandParser:
    def parse(self, command_string: str) -> CGCommand:
        # Parse /cg-issue 123 --security-analysis
        # Return structured command object
    
    def validate(self, command: CGCommand) -> ValidationResult:
        # Validate command syntax and parameters
    
    def execute(self, command: CGCommand) -> ExecutionResult:
        # Route to appropriate workflow handler
```

#### 1.3 Base Command Infrastructure
- **Command Registry**: Dynamic command registration and discovery
- **Parameter Validation**: Type safety and required parameter checking  
- **Error Handling**: Graceful failure with helpful error messages
- **Logging**: Comprehensive audit trail for all workflow operations

**Deliverables**:
- [ ] `apps/cg_workflow/` directory structure
- [ ] Base command parsing framework
- [ ] Integration with Claude Code via enhanced hooks
- [ ] Unit tests for command parsing

### Phase 2: Core Workflow Commands (Week 2-4)

#### 2.1 `/cg-init` - Project Initialization
**Priority**: Critical - Required for all other workflows

**Implementation Steps**:
1. **Environment Detection**:
   ```python
   def detect_project_type():
       # Next.js: package.json + next.config.js
       # Python: pyproject.toml + requirements.txt
       # Go: go.mod
       # Return ProjectType enum
   ```

2. **Test Framework Discovery**:
   ```python
   def detect_test_framework(project_type):
       # Jest for Next.js
       # PyTest for Python
       # Go test for Go
       # Return TestFramework configuration
   ```

3. **Documentation Generation**:
   ```python
   async def generate_init_docs(project_assessment):
       # Create CG_INIT.md with:
       # - Project analysis
       # - Recommended configurations
       # - Tool verification results
       # - Next steps checklist
   ```

**Expected Output**:
```markdown
# CG_INIT.md
## Project Assessment
- **Type**: Next.js 14 Application
- **Test Framework**: Jest + React Testing Library
- **GitHub Integration**: ✅ Connected
- **Dependencies**: ✅ All required tools available

## Recommendations
- Enable GitHub Actions for automated testing
- Configure ESLint + Prettier for code quality
- Setup Playwright for E2E testing

## Next Steps
1. Run `/cg-legacy` to modernize existing untested code
2. Use `/cg-issue <number>` to start TDD development
3. Configure team GitHub project board
```

#### 2.2 `/cg-issue <number>` - Issue Development Workflow
**Priority**: Critical - Core TDD workflow

**Implementation Strategy**:
```python
class CGIssueWorkflow:
    async def start_issue(self, issue_number: int):
        # 1. Fetch issue from GitHub
        issue = await github_client.get_issue(issue_number)
        
        # 2. Check for existing work
        existing_docs = self.find_existing_documentation(issue_number)
        
        # 3. Route to appropriate phase
        if existing_docs:
            return await self.resume_workflow(issue_number, existing_docs)
        else:
            return await self.start_analysis_phase(issue)
    
    async def start_analysis_phase(self, issue):
        # Delegate to cg-analyzer agent
        analysis = await self.execute_agent(
            agent="cg-analyzer",
            prompt=f"Analyze issue: {issue.title}\n{issue.body}",
            model="claude-opus-4-1-20250805"
        )
        
        # Generate CG_TDD_<number>.md
        await self.create_analysis_document(issue.number, analysis)
        
        # Update GitHub issue status
        await self.update_issue_status(issue.number, "Analysis")
```

**Sequential Agent Execution**:
```python
async def execute_tdd_workflow(self, issue_number):
    # Phase 1: Analysis (CTO-level)
    analysis = await self.run_cg_analyzer(issue_number)
    
    # Phase 2: Test Planning (Test Engineer)
    test_plan = await self.run_cg_planner(issue_number, analysis)
    
    # Phase 3: Implementation (Senior Developer)
    implementation = await self.run_cg_implementer(issue_number, analysis, test_plan)
    
    return {
        "analysis_doc": f"CG_TDD_{issue_number}.md",
        "test_plan_doc": f"CG_TDD_TESTS_{issue_number}.md", 
        "implementation_doc": f"CG_TDD_IMPLEMENTATION_{issue_number}.md",
        "status": "Ready for Code Review"
    }
```

#### 2.3 `/cg-legacy` - Legacy Code Modernization
**Priority**: High - Enables TDD adoption for existing codebases

**Implementation Approach**:
```python
class LegacyModernizer:
    async def analyze_codebase(self):
        # Scan for untested files
        untested_files = await self.find_untested_code()
        
        # Prioritize by risk/complexity
        prioritized = self.prioritize_files(untested_files)
        
        # Generate modernization plan
        return await self.create_modernization_plan(prioritized)
    
    async def retrofit_tests(self, file_path):
        # Use cg-planner to create test strategy
        test_strategy = await self.plan_tests_for_legacy(file_path)
        
        # Generate test files
        await self.generate_test_files(file_path, test_strategy)
        
        # Validate test coverage
        coverage = await self.run_coverage_analysis(file_path)
        return coverage
```

### Phase 3: GitHub Integration (Week 3-5)

#### 3.1 GitHub API Integration
**Components**:
```python
# apps/cg_workflow/src/github_integration/
├── client.py          # GitHub API client wrapper
├── project_boards.py  # Project board management
├── issue_manager.py   # Issue lifecycle management
├── pr_automation.py   # Pull request automation
└── webhooks.py        # GitHub webhook handlers
```

**Key Features**:
- **Automatic Board Updates**: Move issues between columns based on workflow state
- **PR Creation**: Automated pull request generation with full documentation
- **Status Synchronization**: Bi-directional sync between workflow and GitHub
- **Branch Management**: Feature branch creation and cleanup

#### 3.2 Project Board Automation
**Board Structure**:
```
Sprint Planning → Analysis → Implementation → Testing → Code Review → E2E Testing → Done
```

**Transition Logic**:
```python
class BoardManager:
    async def transition_issue(self, issue_number, from_column, to_column):
        # Validate transition is allowed
        if not self.is_valid_transition(from_column, to_column):
            raise InvalidTransitionError()
        
        # Update GitHub project board
        await self.github.move_issue(issue_number, to_column)
        
        # Log transition
        await self.log_transition(issue_number, from_column, to_column)
        
        # Trigger any post-transition hooks
        await self.execute_transition_hooks(issue_number, to_column)
```

### Phase 4: Agent Specialization (Week 4-6)

#### 4.1 CG-Analyzer Agent (CTO-Level Analysis)
**Configuration**:
```yaml
# .claude/agents/cg-analyzer.md
---
name: cg-analyzer
description: CTO-level analysis agent for comprehensive issue analysis and system impact assessment
model: claude-opus-4-1-20250805
provider: anthropic
tools: mcp__nano-agent__prompt_nano_agent
---
```

**Responsibilities**:
- **System Impact Analysis**: How does this change affect the broader system?
- **Architecture Decisions**: What patterns and approaches should be used?
- **Technical Debt Assessment**: What existing debt does this address/create?
- **Security Implications**: What security considerations are relevant?
- **Performance Impact**: What are the performance implications?

**Output Format** (`CG_TDD_<number>.md`):
```markdown
# Issue Analysis: [Issue Title]

## System Impact Assessment
- **Affected Components**: List of system components impacted
- **Integration Points**: External systems/APIs affected
- **Data Flow Changes**: How data flow changes with this feature

## Architecture Strategy
- **Design Patterns**: Recommended patterns for implementation
- **Code Organization**: How to structure the new code
- **Dependency Management**: New dependencies and their justification

## Technical Implementation Plan
- **Database Changes**: Schema modifications if any
- **API Changes**: New endpoints or modifications to existing ones
- **Frontend Changes**: UI/UX components affected
- **Testing Strategy**: Types of tests needed

## Risk Assessment
- **Technical Risks**: Implementation challenges
- **Integration Risks**: Potential conflicts with existing code
- **Performance Risks**: Scalability considerations
- **Security Risks**: Security implications and mitigations
```

#### 4.2 CG-Planner Agent (Test Strategy)
**Specialization**: Comprehensive test strategy development

**Output Format** (`CG_TDD_TESTS_<number>.md`):
```markdown
# Test Strategy: [Issue Title]

## Test Categories

### Unit Tests
- **Component Tests**: Individual function/class testing
- **Mock Strategy**: External dependencies to mock
- **Edge Cases**: Boundary conditions to test

### Integration Tests
- **API Integration**: External service integration testing
- **Database Integration**: Data persistence testing
- **Component Integration**: How components work together

### End-to-End Tests
- **User Journeys**: Complete user workflows to test
- **Browser Testing**: Cross-browser compatibility
- **Performance Testing**: Load and stress testing

## Test Implementation Plan
1. **Test Setup**: Test environment and data setup
2. **Implementation Order**: Which tests to write first
3. **Success Criteria**: What constitutes passing tests
4. **Coverage Goals**: Target coverage percentages
```

#### 4.3 CG-Implementer Agent (Development)
**Role**: Senior developer with access to specialized agents

**Workflow**:
```python
async def implement_feature(self, issue_number, analysis, test_plan):
    # Create detailed implementation task list
    tasks = await self.break_down_implementation(analysis, test_plan)
    
    # Implement tests first (TDD)
    for test_task in tasks.test_tasks:
        await self.implement_test(test_task)
        await self.commit_atomic_change(test_task)
    
    # Implement production code
    for impl_task in tasks.implementation_tasks:
        await self.implement_feature_code(impl_task)
        await self.run_tests()  # Ensure tests pass
        await self.commit_atomic_change(impl_task)
    
    # Use specialized agents for reviews
    await self.run_security_review()
    await self.run_architecture_review()
    
    # Generate final documentation
    await self.create_implementation_summary(issue_number)
```

### Phase 5: Testing & Validation (Week 5-7)

#### 5.1 Internal Testing Repository
**Setup Test Environment**:
```bash
# Create test repository structure
mkdir cg-workflow-test-repo
cd cg-workflow-test-repo

# Initialize with realistic project structure
npm init -y
npm install next react react-dom jest @testing-library/react

# Create sample issues for testing
gh issue create --title "Add user authentication" --body "Implement JWT-based auth"
gh issue create --title "Create dashboard component" --body "Build responsive dashboard"
gh issue create --title "API rate limiting" --body "Add rate limiting middleware"
```

#### 5.2 Test Scenarios
**Scenario 1: New Feature Development**
- [ ] `/cg-init` on fresh Next.js project
- [ ] `/cg-issue 1` for authentication feature
- [ ] Complete TDD workflow from analysis → implementation
- [ ] Verify GitHub board updates
- [ ] Validate generated documentation

**Scenario 2: Legacy Code Modernization**
- [ ] `/cg-legacy` on existing untested codebase  
- [ ] Verify test generation for existing functions
- [ ] Validate test coverage improvements
- [ ] Check integration with new TDD workflow

**Scenario 3: Multi-Issue Coordination**
- [ ] Multiple concurrent issues in different phases
- [ ] Verify board state accuracy
- [ ] Test branch management and conflicts
- [ ] Validate documentation organization

#### 5.3 Integration Testing
```python
# tests/integration/test_cg_workflow.py
class TestCGWorkflowIntegration:
    async def test_complete_issue_workflow(self):
        # Test full workflow from /cg-issue to Done
        
    async def test_github_integration(self):
        # Test GitHub API interactions
        
    async def test_agent_coordination(self):
        # Test multi-agent workflow execution
        
    async def test_error_recovery(self):
        # Test workflow recovery from failures
```

## Technical Requirements

### System Dependencies
- **Python 3.12+**: Core workflow engine
- **Node.js 18+**: For Next.js test projects
- **GitHub CLI**: For GitHub API interactions
- **Docker**: Optional containerization
- **UV**: Python dependency management

### API Requirements
- **GitHub Personal Access Token**: Repository and project board access
- **LLM Provider API Keys**: OpenAI, Anthropic, Google
- **Webhook Endpoints**: For GitHub integration (optional)

### Performance Requirements
- **Command Response Time**: < 5 seconds for simple commands
- **Agent Execution**: < 2 minutes for analysis/planning phases
- **Documentation Generation**: < 30 seconds per document
- **GitHub API Calls**: Rate limit compliant (5000/hour)

## Command Implementation Strategy

### Command Registration Framework
```python
# apps/cg_workflow/src/commands/base.py
class CGCommand:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    async def execute(self, args: Dict[str, Any]) -> CommandResult:
        raise NotImplementedError
    
    def validate_args(self, args: Dict[str, Any]) -> ValidationResult:
        return ValidationResult(valid=True)

# Command registration
@register_command
class CGInitCommand(CGCommand):
    def __init__(self):
        super().__init__("init", "Initialize project for CG workflow")
    
    async def execute(self, args):
        # Implementation
        pass
```

### Claude Code Integration Strategy
```python
# .claude/hooks/session_start.py enhancement
async def handle_session_start(user_message: str):
    if user_message.startswith('/cg-'):
        # Parse and execute CG command
        command = CGCommandParser.parse(user_message)
        result = await command.execute()
        
        # Return structured response
        return {
            "message": result.summary,
            "files_created": result.files,
            "next_steps": result.next_steps
        }
    
    # Default Claude Code behavior
    return None
```

## Testing Strategy

### Unit Testing
- **Command Parsing**: Validate all command variations
- **Agent Integration**: Mock agent responses for testing  
- **GitHub API**: Mock GitHub API for reliable testing
- **Documentation Generation**: Validate markdown output

### Integration Testing  
- **End-to-End Workflow**: Complete issue lifecycle testing
- **Multi-Agent Coordination**: Sequential agent execution
- **Error Recovery**: Graceful failure handling
- **Performance**: Response time and resource usage

### User Acceptance Testing
- **Developer Experience**: Ease of use and learning curve
- **Documentation Quality**: Clarity and completeness
- **Workflow Efficiency**: Time savings vs. manual process
- **Error Messages**: Helpfulness and clarity

## GitHub Integration Plan

### API Integration Architecture
```python
# apps/cg_workflow/src/github/
├── __init__.py
├── client.py           # GraphQL and REST API wrapper
├── models.py           # Data models for Issues, PRs, Projects
├── project_boards.py   # Project board management
├── issue_lifecycle.py  # Issue state management
├── pr_automation.py    # Pull request automation
└── webhooks.py         # Webhook handling (future)
```

### Project Board Configuration
**Required Columns**:
- Sprint Planning
- Analysis  
- Implementation
- Testing
- Code Review
- E2E Testing
- Done

**Automation Rules**:
```python
BOARD_TRANSITIONS = {
    "Sprint Planning": ["Analysis"],
    "Analysis": ["Implementation", "Sprint Planning"],  # Can go back
    "Implementation": ["Testing", "Analysis"],          # Can go back
    "Testing": ["Code Review", "Implementation"],       # Can go back
    "Code Review": ["E2E Testing", "Implementation"],   # Can go back
    "E2E Testing": ["Done", "Code Review"],            # Can go back
    "Done": []  # Terminal state
}
```

### Issue Lifecycle Management
```python
class IssueLifecycleManager:
    async def start_issue_workflow(self, issue_number: int):
        # Move to Analysis column
        # Assign to developer
        # Create feature branch
        # Generate initial documentation
        
    async def complete_analysis(self, issue_number: int):
        # Validate analysis documentation exists
        # Move to Implementation column
        # Notify relevant parties
        
    async def handle_test_failure(self, issue_number: int):
        # Move back to Implementation
        # Add failure details to issue
        # Preserve existing work
```

## Agent Specialization Framework

### Agent Configuration Management
```python
# apps/cg_workflow/src/agents/
├── __init__.py
├── base_agent.py      # Base agent interface
├── analyzer.py        # CTO-level analysis agent
├── planner.py         # Test strategy agent  
├── implementer.py     # Development agent
├── coordinator.py     # Multi-agent coordination
└── models.py          # Agent configuration models
```

### Agent Execution Framework
```python
class AgentCoordinator:
    async def execute_sequential_workflow(self, workflow: WorkflowDefinition):
        results = {}
        
        for step in workflow.steps:
            # Execute agent with context from previous steps
            result = await self.execute_agent(
                agent=step.agent,
                prompt=step.prompt_template.format(**results),
                context=results
            )
            
            results[step.name] = result
            
            # Validate step completion
            if not step.validate(result):
                raise WorkflowStepError(f"Step {step.name} failed validation")
        
        return results
```

### Model Selection Strategy
```python
MODEL_STRATEGY = {
    "analysis": {
        "model": "claude-opus-4-1-20250805",
        "provider": "anthropic",
        "reasoning": "Complex system analysis requires highest reasoning capability"
    },
    "planning": {
        "model": "claude-sonnet-4-20250514", 
        "provider": "anthropic",
        "reasoning": "Structured planning with good cost/performance balance"
    },
    "implementation": {
        "model": "claude-sonnet-4-20250514",
        "provider": "anthropic", 
        "reasoning": "Code generation with specialized agent access"
    },
    "security_review": {
        "model": "gemini-2.5-flash",
        "provider": "google",
        "reasoning": "Cost-effective security analysis with large context"
    }
}
```

## Risk Assessment & Mitigation

### Technical Risks

#### Risk: Claude Code Command Integration Complexity
**Probability**: Medium  
**Impact**: High  
**Mitigation**: 
- Start with proof-of-concept using session hooks
- Fallback to direct agent invocation if needed
- Collaborate with Claude Code team on native command support

#### Risk: GitHub API Rate Limiting
**Probability**: Medium  
**Impact**: Medium  
**Mitigation**:
- Implement intelligent caching
- Use GraphQL for efficient data retrieval  
- Add retry logic with exponential backoff
- Monitor usage and implement usage optimization

#### Risk: Multi-Agent Coordination Complexity
**Probability**: High  
**Impact**: Medium  
**Mitigation**:
- Start with simple sequential execution
- Add comprehensive error handling
- Implement agent execution monitoring
- Create agent execution replay capability

### Process Risks

#### Risk: Documentation Overhead
**Probability**: Medium  
**Impact**: Medium  
**Mitigation**:
- Automate documentation generation where possible
- Use templates to reduce manual work
- Implement documentation validation
- Regular cleanup of obsolete documentation

#### Risk: User Adoption Resistance  
**Probability**: Medium  
**Impact**: High  
**Mitigation**:
- Comprehensive onboarding documentation
- Video tutorials and examples
- Gradual rollout with early adopters
- Regular feedback collection and iteration

## Success Metrics

### Quantitative Metrics
- **Development Velocity**: 40% faster feature delivery
- **Test Coverage**: >90% for new features  
- **Bug Reduction**: 60% fewer production bugs
- **Documentation Coverage**: 100% of features documented
- **Code Review Time**: 50% reduction in review cycles

### Qualitative Metrics  
- **Developer Satisfaction**: Survey scores >8/10
- **Code Quality**: Improved maintainability scores
- **Knowledge Transfer**: Reduced onboarding time for new team members
- **Process Compliance**: >95% adherence to TDD workflow

### Cost Optimization Metrics
- **LLM Usage Cost**: 80% reduction vs. previous approach
- **Development Time**: ROI positive within 30 days
- **Maintenance Overhead**: <5% of development time spent on workflow maintenance

## Timeline & Milestones

### Week 1-2: Foundation
- [ ] **Day 1-3**: Command framework implementation
- [ ] **Day 4-7**: Basic `/cg-init` command
- [ ] **Day 8-14**: `/cg-issue` core workflow

**Milestone**: Basic workflow commands functional

### Week 3-4: Core Features
- [ ] **Day 15-21**: GitHub integration foundation
- [ ] **Day 22-28**: Agent specialization implementation

**Milestone**: Complete TDD workflow operational

### Week 5-6: Advanced Features
- [ ] **Day 29-35**: `/cg-legacy` and advanced commands  
- [ ] **Day 36-42**: Error handling and recovery

**Milestone**: Production-ready feature set

### Week 7-8: Testing & Polish
- [ ] **Day 43-49**: Comprehensive testing and bug fixes
- [ ] **Day 50-56**: Documentation and user onboarding

**Milestone**: Ready for team adoption

### Week 9-10: Deployment & Training
- [ ] **Day 57-63**: Team rollout and training
- [ ] **Day 64-70**: Feedback collection and iteration

**Milestone**: Successful team adoption

## Repository Structure

```
cg-workflows/
├── README.md                           # Project overview
├── CG_WORKFLOW_IMPLEMENTATION_PLAN.md  # This document
├── REVISED_CG_WORKFLOW.md              # Original workflow specification
├── apps/
│   ├── cg_workflow/                    # Core workflow engine
│   │   ├── src/
│   │   │   ├── commands/               # Command implementations
│   │   │   ├── agents/                 # Agent coordination
│   │   │   ├── github/                 # GitHub integration
│   │   │   ├── documentation/          # Doc generation
│   │   │   └── utils/                  # Shared utilities
│   │   ├── tests/                      # Test suite
│   │   └── pyproject.toml             # Dependencies
│   └── nano_agent_mcp_server/          # Existing MCP server
├── .claude/
│   ├── agents/                         # CG agent configurations
│   ├── commands/                       # Workflow commands
│   ├── hooks/                          # Enhanced hooks
│   └── settings.json                   # Claude Code configuration
├── docs/                               # Generated documentation
├── examples/                           # Usage examples
└── tests/
    ├── integration/                    # Integration tests
    ├── fixtures/                       # Test data
    └── test_repos/                     # Sample repositories
```

## Next Steps

### Immediate Actions (This Week)
1. **Review and Approve Plan**: Stakeholder sign-off on implementation approach
2. **Environment Setup**: Prepare development environment and test repositories
3. **Command Framework**: Begin implementation of basic command parsing
4. **GitHub Setup**: Create test GitHub project and configure API access

### Phase 1 Deliverables (Next 2 Weeks)
1. **Working `/cg-init`**: Basic project initialization command
2. **Basic `/cg-issue`**: Simple issue workflow without full agent coordination
3. **Documentation Template**: Standard format for CG documentation
4. **Test Suite Foundation**: Unit tests for core components

### Success Criteria for Phase 1
- [ ] Commands execute without errors
- [ ] Basic documentation generation works  
- [ ] GitHub API integration functional
- [ ] Test suite passes with >80% coverage

---

## Appendices

### A. Command Reference

#### `/cg-init`
**Syntax**: `/cg-init [--force] [--project-type=<type>]`
**Description**: Initialize project for CG workflow
**Options**:
- `--force`: Overwrite existing configuration
- `--project-type`: Specify project type (nextjs, python, go)

#### `/cg-issue <number>`  
**Syntax**: `/cg-issue <number> [--resume] [--security-analysis]`
**Description**: Start or resume issue development workflow
**Options**:
- `--resume`: Force resume even if issue appears complete
- `--security-analysis`: Include Gemini security review

#### `/cg-legacy`
**Syntax**: `/cg-legacy [--scan-only] [--priority=<level>]`  
**Description**: Modernize legacy code with TDD
**Options**:
- `--scan-only`: Only scan and report, don't generate tests
- `--priority`: Focus on high/medium/low priority files

#### `/cg-doctor`
**Syntax**: `/cg-doctor [--fix] [--verbose]`
**Description**: Diagnose and fix workflow issues
**Options**:
- `--fix`: Automatically fix detected issues
- `--verbose`: Detailed diagnostic output

### B. Agent Prompt Templates

#### CG-Analyzer System Prompt
```
You are a Senior Software Architect and CTO with deep expertise in system design, 
architecture patterns, and technical decision making. Your role is to analyze 
feature requests and provide comprehensive technical guidance.

For each issue analysis, provide:

1. **System Impact Assessment**
   - What components will be affected?
   - How does this change the overall system architecture?
   - What are the integration points?

2. **Technical Strategy**
   - What design patterns should be used?
   - How should the code be organized?
   - What are the key technical decisions?

3. **Risk Analysis**  
   - What could go wrong?
   - What are the performance implications?
   - What security considerations apply?

4. **Implementation Guidance**
   - What's the recommended approach?
   - What should be implemented first?
   - What are the dependencies?

Generate detailed documentation in markdown format following the CG_TDD_<number>.md template.
```

#### CG-Planner System Prompt  
```
You are a Senior Test Engineer with expertise in Test-Driven Development, 
test strategy design, and comprehensive quality assurance practices.

Based on the architectural analysis provided, create a complete test strategy that includes:

1. **Test Categories**
   - Unit tests for individual components
   - Integration tests for component interaction  
   - End-to-end tests for user workflows

2. **Test Implementation Plan**
   - Which tests to write first (TDD order)
   - Test data and mock requirements
   - Success criteria for each test category

3. **Coverage Strategy**
   - Target coverage percentages
   - Critical paths that must be tested
   - Edge cases and error conditions

4. **Quality Gates**
   - When tests should pass before proceeding
   - Performance benchmarks
   - Security test requirements

Generate the test strategy in markdown format following the CG_TDD_TESTS_<number>.md template.
```

### C. Configuration Examples

#### GitHub Project Board Setup
```yaml
# .github/project-config.yml
name: "CG Development Workflow"
columns:
  - name: "Sprint Planning"
    preset: "SPRINT_PLANNING"
  - name: "Analysis" 
    preset: "IN_PROGRESS"
  - name: "Implementation"
    preset: "IN_PROGRESS"
  - name: "Testing"
    preset: "IN_PROGRESS"
  - name: "Code Review"
    preset: "IN_REVIEW"
  - name: "E2E Testing"
    preset: "IN_REVIEW"
  - name: "Done"
    preset: "DONE"

automation:
  issue_opened: "Sprint Planning"
  pull_request_opened: "Code Review"
  pull_request_merged: "Done"
```

#### Claude Code Agent Configuration
```yaml
# .claude/agents/cg-analyzer.md
---
name: cg-analyzer
description: CTO-level analysis agent for comprehensive system impact assessment using Claude Opus 4.1 for maximum reasoning capability
model: claude-opus-4-1-20250805
provider: anthropic
color: purple
tools: mcp__nano-agent__prompt_nano_agent
---

You are a Senior Software Architect and CTO analyzing feature requests for implementation planning...
```

---

**Document Version**: 1.0  
**Last Updated**: 2025-08-13  
**Status**: Ready for Implementation  
**Stakeholder Review**: Pending  

This implementation plan provides a comprehensive roadmap for building the CG workflow system on our proven nano-agent foundation. The phased approach ensures manageable development with clear milestones and success criteria.