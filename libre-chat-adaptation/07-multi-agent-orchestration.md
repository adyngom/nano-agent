# Multi-Agent Orchestration for ARTIST Core

## Executive Summary

This document details the multi-agent orchestration approach for ARTIST Core, leveraging LibreChat's sophisticated agent system to coordinate multiple AI agents across the A.R.T.I.S.T. workflow phases. The orchestration system provides seamless agent handoffs, shared context management, and cost-optimized task routing while maintaining the user-friendly interface that eliminates terminal intimidation.

## LibreChat Agent System Foundation

### Agent Conversation Management

**LibreChat's Multi-Agent Architecture:**
```javascript
// api/models/Agent.js - Core agent model
const Agent = {
  id: String,
  name: String,
  author: ObjectId,
  instructions: String,
  model: String,
  tools: [String],
  model_parameters: {
    max_tokens: Number,
    temperature: Number,
    top_p: Number,
    presence_penalty: Number,
    frequency_penalty: Number
  },
  tool_resources: {
    code_interpreter: Object,
    file_search: Object
  },
  versions: [Object],
  category: String,
  projectIds: [ObjectId],
  is_promoted: Boolean,
  support_contact: String
};
```

**ARTIST Agent Registry Enhancement:**
```javascript
// artist-core/services/orchestration/AgentRegistry.js
class ArtistAgentRegistry {
  constructor(librechatAPI) {
    this.api = librechatAPI;
    this.agentTemplates = new Map();
    this.activeAgents = new Map();
    this.workflowCoordination = new Map();
    this.initializeArtistAgents();
  }

  async initializeArtistAgents() {
    const artistAgentTemplates = [
      {
        name: 'Claude Business Analyst',
        key: 'claude-business-analyst',
        phase: 'A',
        role: 'analyst',
        instructions: `You are an expert business analyst specializing in SaaS product strategy.
Your role in the ARTIST workflow is to:
- Analyze market opportunities and competitive landscape
- Define user personas and customer journey mapping
- Create comprehensive business requirements
- Establish success metrics and KPIs

ARTIST Context Integration:
- Always consider the project's target market and business model
- Coordinate findings with UI/UX strategist for user experience alignment
- Prepare analysis for GitHub project board creation
- Document insights for development team handoff`,
        tools: ['traversaal_search', 'tavily_search_results_json', 'web-browser'],
        model: 'claude-3-5-sonnet-20241022',
        cost_tier: 'high-reasoning'
      },
      {
        name: 'Claude UI/UX Strategist',
        key: 'claude-ui-ux-strategist',
        phase: 'A',
        role: 'designer',
        instructions: `You are a senior UI/UX strategist focused on modern SaaS applications.
Your role in the ARTIST workflow is to:
- Design user-centered interface strategies
- Create wireframes and user flow diagrams
- Establish design system foundations
- Plan responsive and accessible experiences

ARTIST Context Integration:
- Build upon business analyst findings for user experience design
- Coordinate with development team for feasible implementation
- Consider cost optimization in design complexity
- Prepare design specifications for development sprints`,
        tools: ['web-browser', 'dalle', 'flux'],
        model: 'claude-3-5-sonnet-20241022',
        cost_tier: 'high-reasoning'
      },
      {
        name: 'Nano GitHub Manager',
        key: 'nano-github-manager',
        phase: 'R',
        role: 'project-manager',
        instructions: `You are a GitHub project management specialist using cost-optimized operations.
Your role in the ARTIST workflow is to:
- Set up comprehensive GitHub project boards
- Create epic and story structures
- Configure issue templates and workflows
- Establish development process automation

ARTIST Context Integration:
- Transform business analysis into actionable development tasks
- Create sprint-ready backlogs from design specifications
- Optimize project structure for team collaboration
- Prepare development environment for implementation phase`,
        tools: ['github-automation', 'project-board-setup'],
        model: 'gpt-4o-mini',
        provider: 'nano-agent-mcp',
        cost_tier: 'bulk-operations',
        cost_savings: 0.948
      },
      {
        name: 'Claude Sprint Developer',
        key: 'claude-sprint-developer',
        phase: 'I',
        role: 'developer',
        instructions: `You are a senior full-stack developer specializing in rapid SaaS development.
Your role in the ARTIST workflow is to:
- Implement features based on GitHub issues and design specifications
- Generate high-quality, maintainable code
- Create comprehensive tests and documentation
- Optimize for performance and scalability

ARTIST Context Integration:
- Execute development tasks from GitHub project boards
- Maintain consistency with design system and business requirements
- Coordinate with testing and deployment agents
- Document implementation decisions for team knowledge sharing`,
        tools: ['claude-code-bridge', 'github-operations', 'code-analysis'],
        model: 'claude-3-5-sonnet-20241022',
        cost_tier: 'high-reasoning'
      },
      {
        name: 'Nano Documentation Specialist',
        key: 'nano-documentation-specialist',
        phase: 'S',
        role: 'documenter',
        instructions: `You are a technical documentation specialist using cost-optimized operations.
Your role in the ARTIST workflow is to:
- Generate comprehensive API documentation
- Create user guides and onboarding materials
- Document deployment and scaling procedures
- Prepare knowledge base for team handoff

ARTIST Context Integration:
- Document all implementation decisions and architectural choices
- Create user-facing documentation from UI/UX specifications
- Prepare scaling guides based on business growth projections
- Generate training materials for development team knowledge transfer`,
        tools: ['documentation-generation', 'api-docs-generator'],
        model: 'gpt-4o-mini',
        provider: 'nano-agent-mcp',
        cost_tier: 'bulk-operations',
        cost_savings: 0.948
      },
      {
        name: 'Claude Test Engineer',
        key: 'claude-test-engineer',
        phase: 'T',
        role: 'tester',
        instructions: `You are a senior test engineer specializing in SaaS application quality assurance.
Your role in the ARTIST workflow is to:
- Design comprehensive testing strategies
- Implement automated test suites
- Perform integration and end-to-end testing
- Validate against business requirements and user scenarios

ARTIST Context Integration:
- Test against original business requirements and user personas
- Validate UI/UX implementation matches design specifications
- Ensure GitHub workflows and deployment processes function correctly
- Prepare production readiness assessment for stakeholder review`,
        tools: ['test-generation', 'integration-testing', 'performance-testing'],
        model: 'claude-3-5-sonnet-20241022',
        cost_tier: 'high-reasoning'
      }
    ];

    // Register each agent template with LibreChat
    for (const template of artistAgentTemplates) {
      await this.registerAgentTemplate(template);
    }
  }

  async registerAgentTemplate(template) {
    const agentConfig = {
      name: template.name,
      instructions: template.instructions,
      model: template.model,
      tools: template.tools,
      model_parameters: this.getOptimalModelParameters(template.cost_tier),
      category: 'artist',
      metadata: {
        artist_phase: template.phase,
        artist_role: template.role,
        cost_tier: template.cost_tier,
        cost_savings: template.cost_savings || 0,
        provider: template.provider || 'anthropic'
      },
      is_promoted: true,
      support_contact: 'support@artist-framework.com'
    };

    const registeredAgent = await this.api.agents.create(agentConfig);
    this.agentTemplates.set(template.key, {
      ...template,
      agentId: registeredAgent.id
    });

    return registeredAgent;
  }

  getOptimalModelParameters(costTier) {
    const parameterProfiles = {
      'high-reasoning': {
        max_tokens: 8192,
        temperature: 0.1,
        top_p: 0.95,
        presence_penalty: 0.0,
        frequency_penalty: 0.0
      },
      'bulk-operations': {
        max_tokens: 4096,
        temperature: 0.2,
        top_p: 0.9,
        presence_penalty: 0.1,
        frequency_penalty: 0.1
      },
      'creative': {
        max_tokens: 6144,
        temperature: 0.7,
        top_p: 0.95,
        presence_penalty: 0.3,
        frequency_penalty: 0.3
      }
    };

    return parameterProfiles[costTier] || parameterProfiles['high-reasoning'];
  }
}
```

## Workflow Orchestration Engine

### Phase-Based Agent Coordination

**ARTIST Workflow Orchestrator:**
```javascript
// artist-core/services/orchestration/WorkflowOrchestrator.js
class ArtistWorkflowOrchestrator {
  constructor(librechatAPI, agentRegistry) {
    this.api = librechatAPI;
    this.agentRegistry = agentRegistry;
    this.activeWorkflows = new Map();
    this.phaseDefinitions = this.initializePhaseDefinitions();
    this.handoffStrategies = new Map();
  }

  initializePhaseDefinitions() {
    return {
      'A': {
        name: 'Analysis',
        description: 'Business analysis and UI/UX strategy',
        agents: ['claude-business-analyst', 'claude-ui-ux-strategist'],
        coordination: 'parallel-with-synthesis',
        success_criteria: [
          'Business requirements documented',
          'User personas defined',
          'UI/UX strategy established',
          'Success metrics identified'
        ],
        deliverables: [
          'business_analysis_report.md',
          'user_personas.md',
          'ui_ux_strategy.md',
          'success_metrics.md'
        ]
      },
      'R': {
        name: 'Repository',
        description: 'GitHub project setup and management',
        agents: ['nano-github-manager'],
        coordination: 'sequential',
        depends_on: ['A'],
        success_criteria: [
          'GitHub repository created',
          'Project boards configured',
          'Issue templates established',
          'Development workflows automated'
        ],
        deliverables: [
          'github_project_structure.md',
          'development_workflows.yml',
          'issue_templates/',
          'project_board_setup.md'
        ]
      },
      'T': {
        name: 'Team',
        description: 'Development team coordination and sprint planning',
        agents: ['nano-github-manager', 'claude-sprint-developer'],
        coordination: 'collaborative',
        depends_on: ['A', 'R'],
        success_criteria: [
          'Sprint backlogs created',
          'Development tasks prioritized',
          'Team roles assigned',
          'Sprint 1 ready'
        ],
        deliverables: [
          'sprint_1_backlog.md',
          'team_coordination_plan.md',
          'development_priorities.md'
        ]
      },
      'I': {
        name: 'Implementation',
        description: 'Code development and feature implementation',
        agents: ['claude-sprint-developer'],
        coordination: 'iterative',
        depends_on: ['A', 'R', 'T'],
        success_criteria: [
          'Core features implemented',
          'Code quality standards met',
          'Integration tests passing',
          'Documentation updated'
        ],
        deliverables: [
          'implemented_features/',
          'test_suites/',
          'api_documentation.md',
          'deployment_guide.md'
        ]
      },
      'S': {
        name: 'Scale',
        description: 'Optimization and scaling preparation',
        agents: ['nano-documentation-specialist', 'claude-sprint-developer'],
        coordination: 'parallel',
        depends_on: ['I'],
        success_criteria: [
          'Performance optimized',
          'Scaling strategies documented',
          'Monitoring implemented',
          'Documentation complete'
        ],
        deliverables: [
          'performance_optimization_report.md',
          'scaling_strategy.md',
          'monitoring_setup.md',
          'complete_documentation/'
        ]
      },
      'T': {
        name: 'Test',
        description: 'Comprehensive testing and validation',
        agents: ['claude-test-engineer'],
        coordination: 'comprehensive',
        depends_on: ['I', 'S'],
        success_criteria: [
          'All tests passing',
          'Business requirements validated',
          'User acceptance criteria met',
          'Production readiness confirmed'
        ],
        deliverables: [
          'test_results_report.md',
          'validation_checklist.md',
          'production_readiness_assessment.md'
        ]
      }
    };
  }

  async executeWorkflow(workflowConfig) {
    const { projectName, projectPath, template, costBudget, userPreferences } = workflowConfig;
    
    // Create master workflow conversation
    const workflowConversation = await this.api.conversations.create({
      title: `ARTIST: ${projectName}`,
      endpoint: 'agents',
      metadata: {
        workflow_type: 'artist',
        template,
        project_path: projectPath,
        cost_budget: costBudget,
        user_preferences: userPreferences,
        phases: Object.keys(this.phaseDefinitions),
        current_phase: 'A',
        workflow_state: 'active'
      }
    });

    const workflowContext = {
      workflowId: workflowConversation.conversationId,
      projectName,
      projectPath,
      template,
      costBudget,
      userPreferences,
      startTime: new Date(),
      phases: {},
      sharedContext: {}
    };

    this.activeWorkflows.set(workflowConversation.conversationId, workflowContext);

    // Execute phases sequentially with proper handoffs
    const results = {};
    for (const phase of Object.keys(this.phaseDefinitions)) {
      results[phase] = await this.executePhase(phase, workflowContext);
      
      // Update shared context after each phase
      await this.updateSharedContext(workflowContext, phase, results[phase]);
    }

    // Generate final workflow summary
    const summary = await this.generateWorkflowSummary(workflowContext, results);
    
    return {
      workflowId: workflowConversation.conversationId,
      results,
      summary,
      totalCost: this.calculateTotalCost(results),
      savings: this.calculateSavings(results),
      duration: Date.now() - workflowContext.startTime
    };
  }

  async executePhase(phaseKey, workflowContext) {
    const phaseDefinition = this.phaseDefinitions[phaseKey];
    const phaseStartTime = Date.now();

    // Create phase-specific conversation
    const phaseConversation = await this.api.conversations.create({
      title: `${phaseDefinition.name} Phase - ${workflowContext.projectName}`,
      endpoint: 'agents',
      parentId: workflowContext.workflowId,
      metadata: {
        workflow_type: 'artist_phase',
        phase: phaseKey,
        phase_name: phaseDefinition.name,
        parent_workflow: workflowContext.workflowId
      }
    });

    const phaseContext = {
      ...workflowContext,
      phase: phaseKey,
      phaseConversationId: phaseConversation.conversationId,
      phaseDefinition,
      phaseStartTime
    };

    let phaseResults;

    // Execute based on coordination strategy
    switch (phaseDefinition.coordination) {
      case 'parallel-with-synthesis':
        phaseResults = await this.executeParallelWithSynthesis(phaseContext);
        break;
      case 'sequential':
        phaseResults = await this.executeSequential(phaseContext);
        break;
      case 'collaborative':
        phaseResults = await this.executeCollaborative(phaseContext);
        break;
      case 'iterative':
        phaseResults = await this.executeIterative(phaseContext);
        break;
      case 'parallel':
        phaseResults = await this.executeParallel(phaseContext);
        break;
      case 'comprehensive':
        phaseResults = await this.executeComprehensive(phaseContext);
        break;
      default:
        phaseResults = await this.executeSequential(phaseContext);
    }

    // Validate phase completion
    const validation = await this.validatePhaseCompletion(phaseKey, phaseResults);
    if (!validation.success) {
      throw new Error(`Phase ${phaseKey} validation failed: ${validation.issues.join(', ')}`);
    }

    return {
      phase: phaseKey,
      name: phaseDefinition.name,
      results: phaseResults,
      validation,
      duration: Date.now() - phaseStartTime,
      agents: phaseDefinition.agents,
      deliverables: phaseDefinition.deliverables
    };
  }
}
```

### Agent Coordination Strategies

**Parallel with Synthesis (Analysis Phase):**
```javascript
// artist-core/services/orchestration/coordination/ParallelWithSynthesis.js
class ParallelWithSynthesisCoordination {
  constructor(orchestrator) {
    this.orchestrator = orchestrator;
  }

  async execute(phaseContext) {
    const { phaseDefinition, workflowContext } = phaseContext;
    const agents = phaseDefinition.agents;

    // Execute agents in parallel
    const agentPromises = agents.map(agentKey => 
      this.executeAgentWithContext(agentKey, phaseContext)
    );

    const agentResults = await Promise.all(agentPromises);

    // Synthesize results from multiple agents
    const synthesisAgent = await this.selectSynthesisAgent(phaseContext);
    const synthesizedResults = await this.synthesizeResults(
      synthesisAgent, 
      agentResults, 
      phaseContext
    );

    return {
      individual_results: agentResults,
      synthesized_results: synthesizedResults,
      coordination_type: 'parallel-with-synthesis'
    };
  }

  async executeAgentWithContext(agentKey, phaseContext) {
    const agentTemplate = this.orchestrator.agentRegistry.agentTemplates.get(agentKey);
    const { workflowContext, phaseConversationId } = phaseContext;

    // Prepare agent-specific context
    const agentContext = this.prepareAgentContext(agentTemplate, workflowContext);
    
    // Execute agent with enhanced instructions
    const agentInstructions = this.enhanceInstructionsWithContext(
      agentTemplate.instructions,
      agentContext
    );

    const agentExecution = await this.orchestrator.api.agents.execute({
      conversationId: phaseConversationId,
      agent_id: agentTemplate.agentId,
      message: agentInstructions,
      model_parameters: agentTemplate.model_parameters,
      context: agentContext
    });

    return {
      agent: agentKey,
      result: agentExecution,
      context: agentContext,
      cost: agentExecution.usage?.cost || 0,
      tokens: agentExecution.usage?.total_tokens || 0
    };
  }

  prepareAgentContext(agentTemplate, workflowContext) {
    return {
      project_name: workflowContext.projectName,
      project_path: workflowContext.projectPath,
      template: workflowContext.template,
      cost_budget: workflowContext.costBudget,
      user_preferences: workflowContext.userPreferences,
      shared_context: workflowContext.sharedContext,
      agent_role: agentTemplate.role,
      phase: agentTemplate.phase,
      cost_tier: agentTemplate.cost_tier,
      coordination_strategy: 'parallel-with-synthesis'
    };
  }

  enhanceInstructionsWithContext(baseInstructions, context) {
    return `
${baseInstructions}

# Current Workflow Context
Project: ${context.project_name}
Template: ${context.template}
Phase: ${context.phase}
Agent Role: ${context.agent_role}
Cost Tier: ${context.cost_tier}

# Project Details
Path: ${context.project_path}
Budget: $${context.cost_budget.max}
User Preferences: ${JSON.stringify(context.user_preferences, null, 2)}

# Coordination Instructions
You are working in parallel with other agents in this phase.
Your results will be synthesized with other agents' outputs.
Focus on your specific expertise area while considering the overall project context.
Document your findings clearly for synthesis with other agents' work.

# Shared Context
${context.shared_context ? JSON.stringify(context.shared_context, null, 2) : 'No prior context available'}

Please execute your role-specific tasks while maintaining awareness of the broader ARTIST workflow.
    `;
  }

  async synthesizeResults(synthesisAgent, agentResults, phaseContext) {
    const synthesisPrompt = this.buildSynthesisPrompt(agentResults, phaseContext);

    const synthesis = await this.orchestrator.api.agents.execute({
      conversationId: phaseContext.phaseConversationId,
      agent_id: synthesisAgent.agentId,
      message: synthesisPrompt,
      model_parameters: synthesisAgent.model_parameters
    });

    return {
      synthesis_agent: synthesisAgent.key,
      synthesis_result: synthesis,
      input_results: agentResults.map(r => ({
        agent: r.agent,
        summary: this.extractResultSummary(r.result)
      }))
    };
  }

  buildSynthesisPrompt(agentResults, phaseContext) {
    const resultSummaries = agentResults.map(result => `
## ${result.agent} Results:
${this.extractResultSummary(result.result)}
    `).join('\n');

    return `
# ARTIST Phase Synthesis Task

You are responsible for synthesizing the results from multiple agents in the ${phaseContext.phaseDefinition.name} phase.

## Agent Results to Synthesize:
${resultSummaries}

## Synthesis Requirements:
1. Identify key themes and insights across all agent results
2. Resolve any conflicts or contradictions between agents
3. Create a unified perspective that incorporates all valuable insights
4. Ensure alignment with ARTIST workflow objectives
5. Prepare actionable outputs for the next phase

## Project Context:
- Project: ${phaseContext.workflowContext.projectName}
- Template: ${phaseContext.workflowContext.template}
- Phase: ${phaseContext.phase}

## Expected Deliverables:
${phaseContext.phaseDefinition.deliverables.map(d => `- ${d}`).join('\n')}

Please provide a comprehensive synthesis that combines the best insights from all agents while maintaining consistency with the ARTIST framework methodology.
    `;
  }
}
```

### Handoff Management System

**Agent Handoff Coordination:**
```javascript
// artist-core/services/orchestration/HandoffManager.js
class AgentHandoffManager {
  constructor(orchestrator) {
    this.orchestrator = orchestrator;
    this.handoffStrategies = new Map();
    this.handoffHistory = new Map();
    this.initializeHandoffStrategies();
  }

  initializeHandoffStrategies() {
    // A → R Handoff: Analysis to Repository
    this.handoffStrategies.set('A→R', {
      fromPhase: 'A',
      toPhase: 'R',
      contextTransfer: [
        'business_requirements',
        'user_personas',
        'ui_ux_strategy',
        'success_metrics'
      ],
      validation: [
        'business_analysis_complete',
        'user_personas_defined',
        'ui_strategy_established'
      ],
      transformation: 'analysis_to_github_structure'
    });

    // R → T Handoff: Repository to Team
    this.handoffStrategies.set('R→T', {
      fromPhase: 'R',
      toPhase: 'T',
      contextTransfer: [
        'github_project_structure',
        'issue_templates',
        'development_workflows',
        'project_board_configuration'
      ],
      validation: [
        'github_repository_ready',
        'project_boards_configured',
        'workflows_automated'
      ],
      transformation: 'github_to_sprint_planning'
    });

    // T → I Handoff: Team to Implementation
    this.handoffStrategies.set('T→I', {
      fromPhase: 'T',
      toPhase: 'I',
      contextTransfer: [
        'sprint_backlogs',
        'prioritized_tasks',
        'team_assignments',
        'development_environment'
      ],
      validation: [
        'sprint_1_ready',
        'tasks_prioritized',
        'team_coordinated'
      ],
      transformation: 'sprint_planning_to_development'
    });

    // Continue for all phase transitions...
  }

  async executeHandoff(fromPhase, toPhase, workflowContext, fromResults) {
    const handoffKey = `${fromPhase}→${toPhase}`;
    const strategy = this.handoffStrategies.get(handoffKey);

    if (!strategy) {
      throw new Error(`No handoff strategy defined for ${handoffKey}`);
    }

    // Validate handoff prerequisites
    const validation = await this.validateHandoffPrerequisites(strategy, fromResults);
    if (!validation.success) {
      throw new Error(`Handoff validation failed: ${validation.issues.join(', ')}`);
    }

    // Transform context for next phase
    const transformedContext = await this.transformContext(
      strategy,
      workflowContext,
      fromResults
    );

    // Update shared context
    await this.updateSharedContext(workflowContext, transformedContext);

    // Record handoff for audit trail
    this.recordHandoff(workflowContext.workflowId, {
      from: fromPhase,
      to: toPhase,
      strategy: strategy,
      context: transformedContext,
      timestamp: new Date(),
      validation: validation
    });

    return {
      success: true,
      strategy: handoffKey,
      transformedContext,
      validation
    };
  }

  async transformContext(strategy, workflowContext, fromResults) {
    const transformer = this.getContextTransformer(strategy.transformation);
    
    return await transformer.transform({
      workflowContext,
      fromResults,
      transferElements: strategy.contextTransfer,
      targetPhase: strategy.toPhase
    });
  }

  getContextTransformer(transformationType) {
    const transformers = {
      'analysis_to_github_structure': new AnalysisToGitHubTransformer(),
      'github_to_sprint_planning': new GitHubToSprintTransformer(),
      'sprint_planning_to_development': new SprintToDevelopmentTransformer(),
      'development_to_scaling': new DevelopmentToScalingTransformer(),
      'scaling_to_testing': new ScalingToTestingTransformer()
    };

    return transformers[transformationType] || new DefaultTransformer();
  }
}
```

### Cost-Aware Agent Selection

**Dynamic Agent Selection Based on Cost and Quality:**
```javascript
// artist-core/services/orchestration/CostAwareAgentSelector.js
class CostAwareAgentSelector {
  constructor(orchestrator) {
    this.orchestrator = orchestrator;
    this.costMatrix = this.buildCostMatrix();
    this.qualityProfiles = this.buildQualityProfiles();
  }

  buildCostMatrix() {
    return {
      'claude-3-5-sonnet-20241022': {
        input: 0.003,
        output: 0.015,
        quality: 0.95,
        reasoning: 0.98,
        creativity: 0.92
      },
      'gpt-4o-mini': {
        input: 0.00015,
        output: 0.0006,
        quality: 0.80,
        reasoning: 0.75,
        creativity: 0.70,
        via_nano_agent: true,
        savings: 0.948
      },
      'claude-3-haiku-20240307': {
        input: 0.00025,
        output: 0.00125,
        quality: 0.75,
        reasoning: 0.70,
        creativity: 0.80
      }
    };
  }

  async selectOptimalAgent(task, context) {
    const { phase, taskType, complexity, budget, quality_requirements } = task;
    const { costBudget } = context;

    // Calculate remaining budget
    const remainingBudget = costBudget.max - (costBudget.used || 0);

    // Get candidate agents for this phase
    const candidates = this.getCandidateAgents(phase, taskType);

    // Score each candidate
    const scoredCandidates = candidates.map(candidate => {
      const score = this.calculateAgentScore(candidate, task, remainingBudget);
      return { ...candidate, score };
    });

    // Sort by score (higher is better)
    scoredCandidates.sort((a, b) => b.score - a.score);

    // Select best candidate that meets budget constraints
    const selectedAgent = scoredCandidates.find(candidate => 
      this.meetsBudgetConstraints(candidate, remainingBudget)
    );

    if (!selectedAgent) {
      throw new Error(`No suitable agent found within budget constraints`);
    }

    return {
      agent: selectedAgent,
      rationale: this.generateSelectionRationale(selectedAgent, task, scoredCandidates),
      cost_estimate: this.estimateTaskCost(selectedAgent, task)
    };
  }

  calculateAgentScore(agent, task, remainingBudget) {
    const costMatrix = this.costMatrix[agent.model];
    const { complexity, quality_requirements, priority } = task;

    // Quality score (0-1)
    const qualityScore = this.calculateQualityScore(costMatrix, quality_requirements);
    
    // Cost efficiency score (0-1, higher for lower cost)
    const costEfficiencyScore = this.calculateCostEfficiencyScore(costMatrix, remainingBudget);
    
    // Capability match score (0-1)
    const capabilityScore = this.calculateCapabilityScore(agent, task);

    // Weighted combination
    const weights = {
      quality: priority === 'high' ? 0.5 : 0.3,
      cost_efficiency: remainingBudget < 10 ? 0.5 : 0.3,
      capability: 0.4
    };

    return (
      qualityScore * weights.quality +
      costEfficiencyScore * weights.cost_efficiency +
      capabilityScore * weights.capability
    );
  }

  generateSelectionRationale(selectedAgent, task, allCandidates) {
    const costMatrix = this.costMatrix[selectedAgent.model];
    const savings = costMatrix.via_nano_agent ? 
      `${(costMatrix.savings * 100).toFixed(1)}% cost savings via nano-agent MCP` : 
      'Direct model usage';

    return {
      agent: selectedAgent.name,
      model: selectedAgent.model,
      cost_tier: selectedAgent.cost_tier,
      selection_reason: this.getSelectionReason(selectedAgent, task),
      cost_optimization: savings,
      quality_level: this.getQualityLevel(costMatrix),
      alternatives_considered: allCandidates.length,
      trade_offs: this.analyzeTradeOffs(selectedAgent, allCandidates)
    };
  }

  getSelectionReason(agent, task) {
    const { complexity, priority, phase } = task;
    
    if (agent.cost_tier === 'bulk-operations') {
      return `Selected for cost efficiency (94.8% savings) suitable for ${phase} phase bulk operations`;
    } else if (agent.cost_tier === 'high-reasoning') {
      return `Selected for maximum reasoning capability required for ${complexity} complexity task`;
    } else {
      return `Balanced selection for quality and cost optimization in ${phase} phase`;
    }
  }
}
```

### Real-Time Workflow Monitoring

**Workflow Status and Progress Tracking:**
```javascript
// artist-core/services/orchestration/WorkflowMonitor.js
class WorkflowMonitor {
  constructor(orchestrator) {
    this.orchestrator = orchestrator;
    this.activeMonitors = new Map();
    this.statusCallbacks = new Map();
    this.progressMetrics = new Map();
  }

  async startWorkflowMonitoring(workflowId, callbacks = {}) {
    const monitor = {
      workflowId,
      startTime: Date.now(),
      callbacks,
      status: 'active',
      currentPhase: null,
      phases: {},
      costs: { total: 0, by_phase: {} },
      agents: { active: [], completed: [] }
    };

    this.activeMonitors.set(workflowId, monitor);

    // Set up real-time updates
    await this.setupRealTimeUpdates(workflowId, monitor);

    return monitor;
  }

  async updatePhaseProgress(workflowId, phase, progress) {
    const monitor = this.activeMonitors.get(workflowId);
    if (!monitor) return;

    monitor.currentPhase = phase;
    monitor.phases[phase] = {
      ...monitor.phases[phase],
      ...progress,
      lastUpdate: Date.now()
    };

    // Calculate overall workflow progress
    const overallProgress = this.calculateOverallProgress(monitor);
    monitor.overallProgress = overallProgress;

    // Notify subscribers
    await this.notifyProgressUpdate(workflowId, {
      phase,
      phaseProgress: progress,
      overallProgress,
      costs: monitor.costs,
      activeAgents: monitor.agents.active
    });

    // Update LibreChat conversation metadata
    await this.updateConversationMetadata(workflowId, monitor);
  }

  async trackAgentExecution(workflowId, agentExecution) {
    const monitor = this.activeMonitors.get(workflowId);
    if (!monitor) return;

    const { agentId, phase, status, cost, tokens } = agentExecution;

    // Update agent tracking
    if (status === 'started') {
      monitor.agents.active.push({
        agentId,
        phase,
        startTime: Date.now()
      });
    } else if (status === 'completed') {
      const activeIndex = monitor.agents.active.findIndex(a => a.agentId === agentId);
      if (activeIndex !== -1) {
        const activeAgent = monitor.agents.active.splice(activeIndex, 1)[0];
        monitor.agents.completed.push({
          ...activeAgent,
          endTime: Date.now(),
          duration: Date.now() - activeAgent.startTime,
          cost,
          tokens
        });
      }
    }

    // Update cost tracking
    if (cost) {
      monitor.costs.total += cost;
      monitor.costs.by_phase[phase] = (monitor.costs.by_phase[phase] || 0) + cost;
    }

    // Calculate cost savings
    if (agentExecution.cost_savings) {
      monitor.costs.savings = (monitor.costs.savings || 0) + agentExecution.cost_savings;
    }

    // Notify cost updates
    await this.notifyCostUpdate(workflowId, monitor.costs);
  }

  calculateOverallProgress(monitor) {
    const phaseWeights = {
      'A': 0.20, // Analysis
      'R': 0.10, // Repository
      'T': 0.15, // Team
      'I': 0.35, // Implementation (largest)
      'S': 0.10, // Scale
      'T': 0.10  // Test
    };

    let totalProgress = 0;
    let totalWeight = 0;

    for (const [phase, weight] of Object.entries(phaseWeights)) {
      if (monitor.phases[phase]) {
        totalProgress += (monitor.phases[phase].progress || 0) * weight;
        totalWeight += weight;
      }
    }

    return totalWeight > 0 ? totalProgress / totalWeight : 0;
  }

  async generateProgressReport(workflowId) {
    const monitor = this.activeMonitors.get(workflowId);
    if (!monitor) return null;

    const currentTime = Date.now();
    const duration = currentTime - monitor.startTime;

    return {
      workflowId,
      status: monitor.status,
      currentPhase: monitor.currentPhase,
      overallProgress: monitor.overallProgress,
      duration: {
        total: duration,
        formatted: this.formatDuration(duration)
      },
      phases: Object.entries(monitor.phases).map(([phase, data]) => ({
        phase,
        name: this.orchestrator.phaseDefinitions[phase]?.name,
        progress: data.progress || 0,
        status: data.status,
        duration: data.endTime ? data.endTime - data.startTime : currentTime - data.startTime
      })),
      costs: {
        total: monitor.costs.total,
        by_phase: monitor.costs.by_phase,
        savings: monitor.costs.savings || 0,
        savings_percentage: monitor.costs.savings ? 
          (monitor.costs.savings / (monitor.costs.total + monitor.costs.savings)) * 100 : 0
      },
      agents: {
        active: monitor.agents.active.length,
        completed: monitor.agents.completed.length,
        performance: this.calculateAgentPerformance(monitor.agents.completed)
      }
    };
  }
}
```

This comprehensive multi-agent orchestration system leverages LibreChat's sophisticated agent architecture to provide seamless coordination across the ARTIST workflow phases, with intelligent cost optimization, real-time monitoring, and robust handoff management between specialized agents.

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "Analyze LibreChat repository structure and architecture", "status": "completed", "id": "1"}, {"content": "Study LibreChat's agent system and extensibility patterns", "status": "completed", "id": "2"}, {"content": "Examine LibreChat's multi-model integration capabilities", "status": "completed", "id": "3"}, {"content": "Evaluate LibreChat's plugin and extension architecture", "status": "completed", "id": "4"}, {"content": "Design ARTIST Core integration strategy for LibreChat", "status": "completed", "id": "5"}, {"content": "Create Claude Code wrapper integration plan", "status": "completed", "id": "6"}, {"content": "Document multi-agent orchestration approach within LibreChat", "status": "completed", "id": "7"}]