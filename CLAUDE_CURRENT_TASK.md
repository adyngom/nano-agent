CG Workflow Agent Adaptation Plan                            │ │
│ │                                                              │ │
│ │ Analysis Summary                                             │ │
│ │                                                              │ │
│ │ I've analyzed the 28 agents in the agents-library and        │ │
│ │ identified highly relevant agents that align perfectly with  │ │
│ │ our CG workflow implementation goals. The library follows a  │ │
│ │ clean frontmatter format that we can adapt while maintaining │ │
│ │  consistency with the existing .claude/agents/ structure.    │ │
│ │                                                              │ │
│ │ Key Findings                                                 │ │
│ │                                                              │ │
│ │ 🎯 Perfect Matches for CG Workflow                           │ │
│ │                                                              │ │
│ │ 1. architecture-reviewer - Exactly what we need for our      │ │
│ │ cg-analyzer role                                             │ │
│ │ 2. claude-testing-specialist - Perfect for our cg-planner    │ │
│ │ test strategy role                                           │ │
│ │ 3. context-orchestrator - Ideal for coordinating our         │ │
│ │ multi-agent CG workflow                                      │ │
│ │ 4. claude-git-assistant - Essential for our commit           │ │
│ │ automation                                                   │ │
│ │ 5. error-pattern-analyzer - Critical for debugging CG        │ │
│ │ workflow issues                                              │ │
│ │ 6. gemini-security-agent - Perfect for cost-effective        │ │
│ │ security analysis                                            │ │
│ │                                                              │ │
│ │ 📋 Agent Mapping Strategy                                    │ │
│ │                                                              │ │
│ │ Core CG Workflow Agents (Migrate to .claude/agents/)         │ │
│ │                                                              │ │
│ │ - architecture-reviewer → Enhanced foundation for system     │ │
│ │ analysis                                                     │ │
│ │ - claude-testing-specialist → TDD strategy and test planning │ │
│ │  expert                                                      │ │
│ │ - context-orchestrator → Multi-agent workflow coordination   │ │
│ │ - claude-git-assistant → Commit automation and branch        │ │
│ │ management                                                   │ │
│ │ - error-pattern-analyzer → CG workflow debugging and         │ │
│ │ diagnostics                                                  │ │
│ │                                                              │ │
│ │ Specialized Security & Quality (Keep nano-agent integration) │ │
│ │                                                              │ │
│ │ - gemini-security-agent → Cost-optimized security reviews    │ │
│ │ via Gemini                                                   │ │
│ │ - debugger-expert → Advanced debugging for complex issues    │ │
│ │                                                              │ │
│ │ Implementation Plan                                          │ │
│ │                                                              │ │
│ │ Phase 1: Core Agent Migration (Priority 1)                   │ │
│ │                                                              │ │
│ │ 1. Migrate architecture-reviewer to                          │ │
│ │ .claude/agents/architecture-reviewer.md                      │ │
│ │   - Adapt frontmatter to match project format (add tools: *) │ │
│ │   - Perfect foundation for our cg-analyzer system impact     │ │
│ │ analysis                                                     │ │
│ │   - Already has ARCHITECTURE.md generation capability        │ │
│ │ 2. Migrate claude-testing-specialist to                      │ │
│ │ .claude/agents/claude-testing-specialist.md                  │ │
│ │   - Ideal for TDD strategy development (our cg-planner role) │ │
│ │   - Focused on comprehensive test planning and               │ │
│ │ implementation                                               │ │
│ │   - Matches our test-first development methodology           │ │
│ │ 3. Migrate context-orchestrator to                           │ │
│ │ .claude/agents/context-orchestrator.md                       │ │
│ │   - Essential for managing our multi-agent CG workflow       │ │
│ │   - Handles complex project coordination and context         │ │
│ │ preservation                                                 │ │
│ │   - Perfect for breaking down large CG tasks across multiple │ │
│ │  sessions                                                    │ │
│ │                                                              │ │
│ │ Phase 2: Workflow Support Agents (Priority 2)                │ │
│ │                                                              │ │
│ │ 1. Migrate claude-git-assistant to                           │ │
│ │ .claude/agents/claude-git-assistant.md                       │ │
│ │   - Critical for our automated commit strategies             │ │
│ │   - Handles branch management and commit message generation  │ │
│ │   - Supports our "atomic commits" requirement                │ │
│ │ 2. Migrate error-pattern-analyzer to                         │ │
│ │ .claude/agents/error-pattern-analyzer.md                     │ │
│ │   - Essential for /cg-doctor command implementation          │ │
│ │   - Provides comprehensive debugging capabilities            │ │
│ │   - Handles complex error correlation and root cause         │ │
│ │ analysis                                                     │ │
│ │                                                              │ │
│ │ Phase 3: Security & Quality Integration (Priority 3)         │ │
│ │                                                              │ │
│ │ 1. Adapt gemini-security-agent for nano-agent integration    │ │
│ │   - Modify to use tools: mcp__nano-agent__prompt_nano_agent  │ │
│ │   - Configure for cost-effective Gemini security analysis    │ │
│ │   - Integrate with our CG workflow for automated security    │ │
│ │ reviews                                                      │ │
│ │                                                              │ │
│ │ Format Standardization                                       │ │
│ │                                                              │ │
│ │ Current Project Format (Target)                              │ │
│ │                                                              │ │
│ │ ---                                                          │ │
│ │ name: agent-name                                             │ │
│ │ description: Clear description with usage examples           │ │
│ │ model: opus|sonnet|gemini                                    │ │
│ │ color: blue|purple|yellow|red                                │ │
│ │ tools: *|mcp__nano-agent__prompt_nano_agent                  │ │
│ │ ---                                                          │ │
│ │                                                              │ │
│ │ Library Format (Source)                                      │ │
│ │                                                              │ │
│ │ ---                                                          │ │
│ │ name: agent-name                                             │ │
│ │ description: Extended description with examples and use      │ │
│ │ cases                                                        │ │
│ │ color: blue                                                  │ │
│ │ tools: * (sometimes)                                         │ │
│ │ model: sonnet (sometimes)                                    │ │
│ │ ---                                                          │ │
│ │                                                              │ │
│ │ Adaptation Strategy                                          │ │
│ │                                                              │ │
│ │ 1. Preserve Core Functionality: Keep all specialized logic   │ │
│ │ and expertise                                                │ │
│ │ 2. Standardize Frontmatter: Adapt to project format          │ │
│ │ requirements                                                 │ │
│ │ 3. Add Tool Integration: Specify appropriate tools for each  │ │
│ │ agent                                                        │ │
│ │ 4. Model Assignment: Assign optimal models based on agent    │ │
│ │ complexity                                                   │ │
│ │ 5. Color Coding: Maintain visual organization system         │ │
│ │                                                              │ │
│ │ Benefits                                                     │ │
│ │                                                              │ │
│ │ Immediate Value                                              │ │
│ │                                                              │ │
│ │ - Proven Agents: These agents are already tested and refined │ │
│ │ - Specialized Expertise: Each agent has deep domain          │ │
│ │ knowledge                                                    │ │
│ │ - Workflow Ready: Direct integration with our CG commands    │ │
│ │ - Time Savings: Avoid rebuilding specialized functionality   │ │
│ │                                                              │ │
│ │ CG Workflow Enhancement                                      │ │
│ │                                                              │ │
│ │ - System Analysis: architecture-reviewer provides CTO-level  │ │
│ │ analysis                                                     │ │
│ │ - Test Strategy: claude-testing-specialist handles           │ │
│ │ comprehensive TDD planning                                   │ │
│ │ - Coordination: context-orchestrator manages complex         │ │
│ │ multi-agent workflows                                        │ │
│ │ - Quality Assurance: Integrated debugging and security       │ │
│ │ analysis                                                     │ │
│ │ - Git Automation: Professional commit and branch management  │ │
│ │                                                              │ │
│ │ Architecture Alignment                                       │ │
│ │                                                              │ │
│ │ - Multi-Agent Support: context-orchestrator enables our      │ │
│ │ sequential agent execution                                   │ │
│ │ - Documentation Generation: architecture-reviewer creates    │ │
│ │ ARCHITECTURE.md                                              │ │
│ │ - Error Recovery: error-pattern-analyzer supports /cg-doctor │ │
│ │  command                                                     │ │
│ │ - Cost Optimization: gemini-security-agent provides          │ │
│ │ cost-effective security analysis                             │ │
│ │                                                              │ │
│ │ Next Steps                                                   │ │
│ │                                                              │ │
│ │ 1. Execute Migration: Move priority agents to                │ │
│ │ .claude/agents/                                              │ │
│ │ 2. Test Integration: Verify agents work with existing        │ │
│ │ nano-agent infrastructure                                    │ │
│ │ 3. Update CG Commands: Integrate migrated agents into        │ │
│ │ workflow commands                                            │ │
│ │ 4. Documentation: Update CG_WORKFLOW_IMPLEMENTATION_PLAN.md  │ │
│ │ with new agent assignments                    