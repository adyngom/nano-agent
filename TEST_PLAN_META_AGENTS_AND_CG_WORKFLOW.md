# Unified Test Plan: Meta-Agents and CG Workflow

## Test Execution Date: 2025-08-14

This document provides a sequential test plan for validating both the newly created meta-agents and the refactored CG workflow with new agent naming conventions.

---

## Phase 1: Meta-Agent Unit Tests

### Test 1.1: Claude Agent Factory
**Purpose**: Validate dynamic Claude agent creation based on task complexity

#### Test Case A: Simple Task (Should create Haiku agent)
```bash
@claude-agent-factory "Create an agent to count lines in files"
```
**Expected**: Creates `claude-agent-line-counter` with Haiku model

#### Test Case B: Medium Complexity (Should create Sonnet agent)
```bash
@claude-agent-factory "Create an agent for API documentation generation"
```
**Expected**: Creates `claude-agent-api-documenter` with Sonnet model

#### Test Case C: Complex Task (Should create Opus agent)
```bash
@claude-agent-factory "Create an agent for deep security vulnerability analysis"
```
**Expected**: Creates `claude-agent-security-analyzer` with Opus model

**Success Criteria**:
- [ ] Agent files created in `.claude/agents/`
- [ ] Correct model selection based on complexity
- [ ] Proper tool configuration
- [ ] Self-documenting names follow convention

---

### Test 1.2: Nano Agent Factory
**Purpose**: Validate external model agent creation for cost optimization

#### Test Case A: Bulk Processing (Should select Gemini Flash)
```bash
@nano-agent-factory "I need to process 10,000 JSON files and extract customer data"
```
**Expected**: Creates `gemini-agent-bulk-processor` with gemini-1.5-flash

#### Test Case B: Local Processing (Should select Ollama)
```bash
@nano-agent-factory "Process sensitive financial data offline without external APIs"
```
**Expected**: Creates `ollama-agent-financial-processor` with gpt-oss model

#### Test Case C: Specialized Coding (Should select GPT)
```bash
@nano-agent-factory "Create a React component generator with TypeScript"
```
**Expected**: Creates `gpt-agent-react-generator` with gpt-5

**Success Criteria**:
- [ ] Correct provider selection based on requirements
- [ ] Cost optimization documented
- [ ] API key requirements specified
- [ ] Uses nano-agent MCP wrapper

---

### Test 1.3: Claude Agent Orchestrator
**Purpose**: Validate parallel execution and comparison

#### Test Case A: Model Comparison
```bash
@claude-agent-orchestrator "Compare 'What is 2+2?' across models" --agents "claude-agent-calculator,gemini-agent-cost-optimizer,nano-agent-gpt-5-mini"
```

**Expected Output Table**:
```markdown
| Agent | Model | Response | Time | Cost | Grade |
|-------|-------|----------|------|------|-------|
| claude-agent-calculator | Sonnet | 4 | 0.5s | $0.002 | S |
| gemini-agent-cost-optimizer | Gemini | 4 | 0.3s | $0.0001 | S |
| nano-agent-gpt-5-mini | GPT-5-mini | 4 | 0.2s | $0.0005 | S |
```

#### Test Case B: Complex Task Comparison
```bash
@claude-agent-orchestrator "Create a fibonacci function" --agents "claude-agent-tdd-implementer,gemini-agent-cost-optimizer"
```

**Success Criteria**:
- [ ] All agents execute in parallel
- [ ] Performance metrics collected
- [ ] Cost comparison provided
- [ ] Quality grades assigned
- [ ] Final ranking with recommendations

---

### Test 1.4: Claude Agent Evaluator
**Purpose**: Validate LOP-style evaluation and grading

#### Test Case A: Code Quality Evaluation
```bash
@claude-agent-evaluator "Evaluate code generation quality" --test "Create a Python class for user authentication" --agents "claude-agent-python-developer,gpt-agent-coder"
```

**Expected**: Detailed evaluation report with:
- [ ] Test specification
- [ ] Grading criteria
- [ ] Score breakdown (accuracy, completeness, format, efficiency)
- [ ] Recommendations

#### Test Case B: Documentation Evaluation
```bash
@claude-agent-evaluator "Evaluate documentation quality" --test "Document this function: def calculate_tax(income, rate)" --agents "claude-agent-documenter"
```

**Success Criteria**:
- [ ] Objective scoring algorithm applied
- [ ] Detailed strengths/weaknesses identified
- [ ] Actionable recommendations provided

---

### Test 1.5: Claude Agent Workflow Composer
**Purpose**: Validate complex workflow orchestration

#### Test Case A: Sequential Workflow
```bash
@claude-agent-workflow-composer "Execute: analyze → plan → implement for adding user authentication"
```

**Expected Workflow**:
1. `claude-agent-project-analyzer` → analyzes requirements
2. `claude-agent-architect` → designs solution
3. `claude-agent-implementer` → writes code

#### Test Case B: Conditional Workflow
```bash
@claude-agent-workflow-composer "Run tests and fix issues until all pass"
```

**Expected**: Loop workflow with conditional branching

**Success Criteria**:
- [ ] Workflow state file created
- [ ] Steps execute in correct order
- [ ] State passed between agents
- [ ] Conditional logic works
- [ ] Error handling implemented

---

## Phase 2: CG Workflow Integration Test

### Test 2.1: Complete CG Workflow with New Agent Names

**Test Scenario**: Implement a new feature using the full CG workflow

#### Step 1: Project Initialization
```bash
@claude-agent-project-init "Add a new feature for exporting user data to CSV format in the freelancer-invoice project"
```

**Expected Output**:
- [ ] Project analyzed
- [ ] Workflow routing determined
- [ ] Next agent recommended

#### Step 2: Issue Analysis
```bash
@claude-agent-issue-analyzer "Analyze issue #42: Export user data to CSV"
```

**Expected Output**:
- [ ] Creates `specs/CG_TDD_42.md`
- [ ] Contains: Context, Requirements, Architecture, Tasks
- [ ] Complexity assessment
- [ ] Dependencies identified

#### Step 3: Test Planning
```bash
@claude-agent-test-planner "Create test plan from specs/CG_TDD_42.md"
```

**Expected Output**:
- [ ] Creates `specs/CG_TDD_TESTS_42.md`
- [ ] Unit tests defined
- [ ] Integration tests defined
- [ ] Edge cases covered
- [ ] Test implementation code

#### Step 4: TDD Implementation
```bash
@claude-agent-tdd-implementer "Implement issue #42 using specs/CG_TDD_42.md and specs/CG_TDD_TESTS_42.md"
```

**Expected Output**:
- [ ] Tests written first
- [ ] Implementation follows TDD cycle
- [ ] All tests pass
- [ ] Code follows project conventions

#### Step 5: Quality Checks (Parallel)
```bash
@claude-agent-orchestrator "Run quality checks" --agents "gemini-security-agent,claude-agent-architecture-reviewer"
```

**Expected**:
- [ ] Security review completed
- [ ] Architecture review completed
- [ ] Both reviews pass

#### Step 6: Git Operations
```bash
@claude-agent-git-assistant "Create PR for issue #42 implementation"
```

**Expected**:
- [ ] Code committed
- [ ] PR created with proper description
- [ ] Links to issue #42

**Overall Workflow Success Criteria**:
- [ ] All agents execute with new names
- [ ] State maintained throughout workflow
- [ ] Files created in correct locations
- [ ] No errors in agent handoffs
- [ ] Complete feature implemented

---

## Phase 3: Advanced Integration Tests

### Test 3.1: Meta-Agent Composition
**Purpose**: Test meta-agents working together

```bash
@claude-agent-workflow-composer "Use claude-agent-factory to create agents, then orchestrate them with claude-agent-orchestrator, and evaluate with claude-agent-evaluator"
```

**Expected**: Meta-agents successfully compose and coordinate

### Test 3.2: Cost Optimization Workflow
```bash
@claude-agent-workflow-composer "Optimize costs: Use nano-agent-factory for bulk tasks and claude-agent-factory for complex tasks"
```

**Expected**: Hybrid workflow with cost optimization

### Test 3.3: Error Recovery
```bash
@claude-agent-workflow-composer "Execute workflow with deliberate failure and recovery"
```

**Expected**: Proper error handling and recovery mechanisms

---

## Phase 4: Performance and Cost Analysis

### Test 4.1: Benchmark Comparison
Run identical task across all agent types and compare:
- Execution time
- Token usage
- Cost
- Output quality

### Test 4.2: Cost Report
Generate comprehensive cost analysis:
- Claude native vs External models
- Savings achieved through optimization
- Recommendations for future tasks

---

## Test Execution Checklist

### Pre-Test Setup
- [ ] All agent files exist in `.claude/agents/`
- [ ] API keys configured (OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY)
- [ ] Ollama running locally (if testing local models)
- [ ] Clean test environment

### During Testing
- [ ] Document any errors or unexpected behavior
- [ ] Capture execution times
- [ ] Note token usage where applicable
- [ ] Save all generated artifacts

### Post-Test Actions
- [ ] Update CG_WORKFLOW_STATE.md with results
- [ ] Document lessons learned
- [ ] Create issues for any bugs found
- [ ] Optimize based on findings

---

## Success Metrics

1. **Functional Success**
   - All test cases pass
   - Agents work with new naming convention
   - Workflow completes end-to-end

2. **Performance Success**
   - Parallel execution works
   - No timeout issues
   - Reasonable execution times

3. **Cost Success**
   - External models provide cost savings
   - Appropriate model selection
   - Cost tracking accurate

4. **Quality Success**
   - Output quality meets expectations
   - Proper error handling
   - Clear documentation generated

---

## Notes for Test Execution

1. **Start with Phase 1** to validate individual meta-agents
2. **Phase 2 is critical** - this validates our refactored CG workflow
3. **Phase 3 and 4** are stretch goals for comprehensive validation
4. **Document all findings** in this file as comments under each test

## Test Results Section
<!-- Add test results here as we execute -->

### Test 1.1.A Results:
**Status**: ✅ PASS

Created agent file: `.claude/agents/claude-agent-line-counter.md`
- Model selected: Claude Haiku 3 (correct for simple task)
- Tools configured: [Read, Write, Glob, Bash]
- Reasoning: Simple task → minimal computational needs → Haiku selected
- File created successfully with proper naming convention
- Agent is immediately usable

### Test 1.1.B Results:
**Status**: ✅ PASS

Created agent file: `.claude/agents/claude-agent-api-documenter.md`
- Model selected: Claude Sonnet 4 (correct for medium complexity)
- Tools configured: [Read, Write, Edit, Glob, Grep, WebFetch]
- Reasoning: Medium complexity → balanced capabilities → Sonnet selected
- Multi-framework support implemented
- Proper documentation structure defined

### Test 1.1.C Results:
**Status**: ✅ PASS

Created agent file: `.claude/agents/claude-agent-security-vulnerability-analyzer.md`
- Model selected: Claude Opus 4.1 (correct for complex task)
- Tools configured: [Read, Write, Edit, Bash, Task, WebFetch, Glob, Grep]
- Reasoning: High complexity → maximum reasoning needed → Opus selected
- Multi-phase security analysis workflow defined
- Cost justification included

### Test 1.2.A Results:
**Status**: ✅ PASS

Created agent file: `.claude/agents/gemini-agent-json-bulk-processor.md`
- Model selected: Gemini Flash (correct for bulk processing)
- Provider: Google Gemini via nano-agent
- Cost optimization: 85-90% savings vs Claude
- Reasoning: High volume → cost critical → Gemini Flash selected

### Test 1.2.B Results:
**Status**: ✅ PASS

Created agent file: `.claude/agents/ollama-agent-financial-processor.md`
- Model selected: gpt-oss:120b with Ollama (correct for offline)
- Provider: Ollama (local)
- Security: Complete offline operation, no API calls
- Reasoning: Security compliance → local only → Ollama selected

### Test 1.2.C Results:
**Status**: ✅ PASS

Created agent file: `.claude/agents/gpt-agent-react-component-generator.md`
- Model selected: GPT-5 (correct for specialized coding)
- Provider: OpenAI via nano-agent
- Expertise: React patterns and TypeScript
- Reasoning: Specialized knowledge → GPT expertise → GPT-5 selected

<!-- Continue for all tests -->