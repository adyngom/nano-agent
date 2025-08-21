# Claude Code Wrapper Integration Plan for ARTIST Core

## Executive Summary

This document outlines the technical implementation plan for integrating Claude Code CLI as a wrapper service within the LibreChat-based ARTIST Core framework. The goal is to provide seamless access to Claude Code's powerful file manipulation and project management capabilities while maintaining LibreChat's user-friendly web interface and multi-agent orchestration features.

## Claude Code Integration Architecture

### Core Integration Strategy

**Bridge Pattern Implementation:**
```javascript
// artist-core/services/claude-code/ClaudeCodeWrapper.js
class ClaudeCodeWrapper {
  constructor(librechatAPI, options = {}) {
    this.api = librechatAPI;
    this.claudeCodePath = options.claudeCodePath || process.env.CLAUDE_CODE_PATH || 'claude-code';
    this.activeProcesses = new Map();
    this.sessionManager = new ClaudeCodeSessionManager();
    this.contextManager = new ProjectContextManager();
  }

  // Primary interface for ARTIST agents to access Claude Code
  async executeClaudeCodeOperation(operation) {
    const { agentId, projectPath, command, context, streamCallback } = operation;
    
    // Validate and prepare context
    const preparedContext = await this.contextManager.prepareContext(projectPath, context);
    
    // Execute Claude Code with enhanced context
    const execution = await this.spawnClaudeCodeProcess({
      command,
      projectPath,
      context: preparedContext,
      agentId,
      streamCallback
    });
    
    // Track execution and return results
    return this.trackExecution(execution, agentId);
  }
}
```

### Project Context Management

**Enhanced Context Injection:**
```javascript
// artist-core/services/claude-code/ProjectContextManager.js
class ProjectContextManager {
  constructor() {
    this.projectRegistry = new Map();
    this.contextTemplates = new Map();
  }

  async prepareContext(projectPath, artistContext) {
    const { phase, agentRole, workflowId, objectives } = artistContext;
    
    // Create comprehensive context file
    const contextData = {
      // ARTIST Framework Context
      workflow: {
        id: workflowId,
        phase: phase,
        agent_role: agentRole,
        objectives: objectives,
        phase_requirements: this.getPhaseRequirements(phase)
      },
      
      // Project Information
      project: {
        path: projectPath,
        type: await this.detectProjectType(projectPath),
        structure: await this.analyzeProjectStructure(projectPath),
        dependencies: await this.analyzeDependencies(projectPath),
        git_status: await this.getGitStatus(projectPath)
      },
      
      // Agent Coordination
      coordination: {
        active_agents: await this.getActiveAgents(workflowId),
        shared_state: await this.getSharedWorkflowState(workflowId),
        handoff_data: await this.getPendingHandoffs(workflowId)
      }
    };

    // Write context to temporary file for Claude Code
    const contextFilePath = await this.writeContextFile(contextData, workflowId);
    
    return {
      contextFilePath,
      environmentVars: this.buildEnvironmentVars(contextData),
      claudeProjectConfig: this.buildClaudeProjectConfig(contextData)
    };
  }

  buildClaudeProjectConfig(contextData) {
    return {
      // Claude Code specific configuration
      '.claude/settings.json': {
        project_context: {
          type: contextData.project.type,
          framework: contextData.project.framework,
          main_directories: contextData.project.structure.main_dirs
        },
        artist_workflow: {
          phase: contextData.workflow.phase,
          agent_role: contextData.workflow.agent_role,
          objectives: contextData.workflow.objectives
        },
        tools: this.getPhaseSpecificTools(contextData.workflow.phase),
        hooks: this.getPhaseSpecificHooks(contextData.workflow.phase)
      }
    };
  }
}
```

### Claude Code Process Management

**Advanced Process Orchestration:**
```javascript
// artist-core/services/claude-code/ProcessManager.js
class ClaudeCodeProcessManager {
  constructor(librechatAPI) {
    this.api = librechatAPI;
    this.processes = new Map();
    this.outputStreams = new Map();
    this.errorHandlers = new Map();
  }

  async spawnClaudeCodeProcess(config) {
    const { command, projectPath, context, agentId, streamCallback } = config;
    
    // Prepare Claude Code command with ARTIST enhancements
    const claudeArgs = this.buildClaudeCodeArgs(command, projectPath, context);
    
    // Spawn process with enhanced monitoring
    const process = spawn(this.claudeCodePath, claudeArgs, {
      cwd: projectPath,
      stdio: ['pipe', 'pipe', 'pipe'],
      env: {
        ...process.env,
        ...context.environmentVars,
        ARTIST_WORKFLOW_ID: context.workflowId,
        ARTIST_PHASE: context.phase,
        ARTIST_AGENT_ROLE: context.agentRole
      }
    });

    const processId = `claude-code-${agentId}-${Date.now()}`;
    this.processes.set(processId, process);

    // Set up real-time output streaming
    await this.setupOutputStreaming(process, processId, streamCallback);
    
    // Set up error handling and recovery
    await this.setupErrorHandling(process, processId, context);
    
    return {
      processId,
      process,
      promise: this.createProcessPromise(process, processId)
    };
  }

  buildClaudeCodeArgs(command, projectPath, context) {
    const baseArgs = [];
    
    // Basic Claude Code arguments
    if (command.type === 'interactive') {
      baseArgs.push('--interactive');
    } else if (command.type === 'task') {
      baseArgs.push('--task', command.task);
    }
    
    // Project context
    baseArgs.push('--project', projectPath);
    
    // Agent context if available
    if (context.agentFilePath) {
      baseArgs.push('--agent', context.agentFilePath);
    }
    
    // ARTIST-specific enhancements
    if (context.phase) {
      baseArgs.push('--context', `artist_phase=${context.phase}`);
    }
    
    if (context.claudeProjectConfig) {
      baseArgs.push('--config', context.configFilePath);
    }
    
    // Output format for integration
    baseArgs.push('--output-format', 'json-stream');
    
    return baseArgs;
  }

  async setupOutputStreaming(process, processId, streamCallback) {
    const outputBuffer = [];
    
    process.stdout.on('data', (data) => {
      const chunk = data.toString();
      outputBuffer.push(chunk);
      
      // Parse structured output from Claude Code
      const lines = chunk.split('\n');
      for (const line of lines) {
        if (line.trim()) {
          try {
            const parsed = JSON.parse(line);
            this.handleStructuredOutput(parsed, processId, streamCallback);
          } catch (e) {
            // Handle plain text output
            this.handlePlainTextOutput(line, processId, streamCallback);
          }
        }
      }
    });

    process.stderr.on('data', (data) => {
      const errorChunk = data.toString();
      this.handleErrorOutput(errorChunk, processId);
    });
  }

  handleStructuredOutput(output, processId, streamCallback) {
    const { type, content, metadata } = output;
    
    switch (type) {
      case 'file_operation':
        this.handleFileOperation(content, metadata, processId);
        break;
      case 'tool_execution':
        this.handleToolExecution(content, metadata, processId);
        break;
      case 'agent_message':
        this.handleAgentMessage(content, metadata, processId);
        break;
      case 'workflow_update':
        this.handleWorkflowUpdate(content, metadata, processId);
        break;
    }
    
    // Stream to LibreChat interface
    if (streamCallback) {
      streamCallback({
        type: 'claude_code_output',
        content: output,
        processId,
        timestamp: new Date().toISOString()
      });
    }
  }
}
```

### Agent-to-Claude-Code Bridge

**Seamless Agent Integration:**
```javascript
// artist-core/services/claude-code/AgentBridge.js
class AgentClaudeCodeBridge {
  constructor(librechatAPI, claudeCodeWrapper) {
    this.api = librechatAPI;
    this.claudeCode = claudeCodeWrapper;
    this.agentRegistry = new Map();
  }

  // Register an agent for Claude Code operations
  async registerAgent(agentConfig, workflowContext) {
    const enhancedAgent = {
      ...agentConfig,
      claudeCodeCapabilities: this.analyzeClaudeCodeCapabilities(agentConfig),
      workflowContext,
      projectPath: workflowContext.projectPath
    };

    this.agentRegistry.set(agentConfig.id, enhancedAgent);
    
    // Create agent-specific Claude Code configuration
    await this.createAgentClaudeCodeConfig(enhancedAgent);
    
    return enhancedAgent;
  }

  // Execute agent task via Claude Code
  async executeAgentTask(agentId, task, options = {}) {
    const agent = this.agentRegistry.get(agentId);
    if (!agent) {
      throw new Error(`Agent ${agentId} not registered for Claude Code operations`);
    }

    // Prepare task for Claude Code execution
    const claudeCodeTask = await this.prepareClaudeCodeTask(agent, task, options);
    
    // Execute via Claude Code with agent context
    const execution = await this.claudeCode.executeClaudeCodeOperation({
      agentId,
      projectPath: agent.projectPath,
      command: claudeCodeTask.command,
      context: claudeCodeTask.context,
      streamCallback: (output) => this.handleAgentOutput(agentId, output)
    });

    // Process results and update agent state
    return this.processExecutionResults(agentId, execution);
  }

  async prepareClaudeCodeTask(agent, task, options) {
    const { instructions, files, tools, context } = task;
    
    // Create enhanced agent instructions for Claude Code
    const enhancedInstructions = `
# Agent Context
Agent ID: ${agent.id}
Agent Role: ${agent.workflowContext.agentRole}
Workflow Phase: ${agent.workflowContext.phase}
Project Type: ${agent.workflowContext.projectType}

# Task Instructions
${instructions}

# ARTIST Framework Integration
- Maintain project context: ${agent.projectPath}
- Coordinate with workflow: ${agent.workflowContext.workflowId}
- Report progress to: ARTIST orchestrator
- Use tools: ${tools?.join(', ') || 'default'}

# File Context
${files ? `Focus on files: ${files.join(', ')}` : 'Full project scope'}

# Success Criteria
${task.successCriteria || 'Complete task successfully with proper documentation'}
    `;

    return {
      command: {
        type: 'task',
        task: enhancedInstructions
      },
      context: {
        ...agent.workflowContext,
        agentId: agent.id,
        agentRole: agent.workflowContext.agentRole,
        taskId: task.id || generateTaskId(),
        tools: tools || agent.tools,
        files: files || []
      }
    };
  }

  handleAgentOutput(agentId, output) {
    const agent = this.agentRegistry.get(agentId);
    
    // Update LibreChat conversation with Claude Code output
    this.api.messages.streamUpdate(agent.conversationId, {
      type: 'agent_output',
      content: output.content,
      metadata: {
        agent_id: agentId,
        claude_code_process: output.processId,
        timestamp: output.timestamp
      }
    });

    // Update workflow state if needed
    if (output.type === 'workflow_update') {
      this.updateWorkflowState(agent.workflowContext.workflowId, output.content);
    }
  }
}
```

### Tool Integration Bridge

**Claude Code Tools via LibreChat:**
```javascript
// artist-core/services/claude-code/ToolBridge.js
class ClaudeCodeToolBridge {
  constructor(librechatAPI, claudeCodeWrapper) {
    this.api = librechatAPI;
    this.claudeCode = claudeCodeWrapper;
    this.toolRegistry = new Map();
  }

  // Register Claude Code as a tool provider for LibreChat
  async registerClaudeCodeTools() {
    const claudeCodeTools = [
      {
        name: 'claude_code_file_operation',
        description: 'Perform file operations via Claude Code CLI',
        parameters: {
          operation: 'string',
          files: 'array',
          content: 'string',
          projectPath: 'string'
        }
      },
      {
        name: 'claude_code_project_analysis',
        description: 'Analyze project structure and dependencies',
        parameters: {
          projectPath: 'string',
          analysisType: 'string'
        }
      },
      {
        name: 'claude_code_code_generation',
        description: 'Generate code via Claude Code with project context',
        parameters: {
          requirements: 'string',
          fileType: 'string',
          projectPath: 'string',
          context: 'object'
        }
      }
    ];

    // Register with LibreChat's tool system
    for (const tool of claudeCodeTools) {
      await this.api.tools.register(tool.name, {
        description: tool.description,
        parameters: tool.parameters,
        handler: (params) => this.handleClaudeCodeTool(tool.name, params)
      });
    }
  }

  async handleClaudeCodeTool(toolName, params) {
    switch (toolName) {
      case 'claude_code_file_operation':
        return this.handleFileOperation(params);
      case 'claude_code_project_analysis':
        return this.handleProjectAnalysis(params);
      case 'claude_code_code_generation':
        return this.handleCodeGeneration(params);
      default:
        throw new Error(`Unknown Claude Code tool: ${toolName}`);
    }
  }

  async handleFileOperation(params) {
    const { operation, files, content, projectPath } = params;
    
    const command = {
      type: 'task',
      task: `Perform ${operation} operation on files: ${files.join(', ')}\nContent: ${content}`
    };

    const result = await this.claudeCode.executeClaudeCodeOperation({
      agentId: 'tool-bridge',
      projectPath,
      command,
      context: {
        operation: 'file_operation',
        tool_initiated: true
      }
    });

    return {
      success: result.success,
      output: result.output,
      files_modified: result.filesModified || [],
      metadata: result.metadata
    };
  }

  async handleCodeGeneration(params) {
    const { requirements, fileType, projectPath, context } = params;
    
    const enhancedRequirements = `
Generate ${fileType} code with the following requirements:
${requirements}

Project Context:
- Path: ${projectPath}
- Type: ${context.projectType || 'unknown'}
- Framework: ${context.framework || 'unknown'}

ARTIST Context:
- Phase: ${context.phase || 'unknown'}
- Agent Role: ${context.agentRole || 'unknown'}

Please ensure the generated code:
1. Follows project conventions
2. Integrates properly with existing codebase
3. Includes appropriate error handling
4. Follows ARTIST framework best practices
    `;

    const command = {
      type: 'task',
      task: enhancedRequirements
    };

    const result = await this.claudeCode.executeClaudeCodeOperation({
      agentId: 'code-generator',
      projectPath,
      command,
      context: {
        operation: 'code_generation',
        fileType,
        tool_initiated: true,
        ...context
      }
    });

    return {
      success: result.success,
      generatedCode: result.output,
      files: result.filesCreated || [],
      suggestions: result.suggestions || [],
      metadata: result.metadata
    };
  }
}
```

### Real-Time Streaming Integration

**WebSocket Bridge for Claude Code Output:**
```javascript
// artist-core/services/claude-code/StreamingBridge.js
class ClaudeCodeStreamingBridge {
  constructor(librechatAPI, socketIO) {
    this.api = librechatAPI;
    this.io = socketIO;
    this.activeStreams = new Map();
  }

  // Set up real-time streaming from Claude Code to LibreChat interface
  setupStreaming(conversationId, processId) {
    const streamHandler = {
      conversationId,
      processId,
      lastUpdate: Date.now(),
      buffer: []
    };

    this.activeStreams.set(processId, streamHandler);

    return (output) => {
      this.handleStreamOutput(streamHandler, output);
    };
  }

  handleStreamOutput(streamHandler, output) {
    const { conversationId, processId } = streamHandler;
    
    // Parse Claude Code output
    const parsedOutput = this.parseClaudeCodeOutput(output);
    
    // Format for LibreChat interface
    const formattedOutput = this.formatForLibreChat(parsedOutput);
    
    // Stream to frontend via WebSocket
    this.io.to(conversationId).emit('claude_code_stream', {
      processId,
      content: formattedOutput,
      timestamp: new Date().toISOString(),
      type: parsedOutput.type || 'output'
    });

    // Update conversation in LibreChat
    this.api.messages.appendStream(conversationId, {
      content: formattedOutput.content,
      type: 'tool_output',
      metadata: {
        source: 'claude_code',
        processId,
        outputType: parsedOutput.type
      }
    });
  }

  parseClaudeCodeOutput(output) {
    try {
      // Try to parse as JSON first
      return JSON.parse(output);
    } catch {
      // Handle plain text output
      return {
        type: 'text',
        content: output,
        timestamp: new Date().toISOString()
      };
    }
  }

  formatForLibreChat(output) {
    switch (output.type) {
      case 'file_operation':
        return {
          content: `📁 File Operation: ${output.operation}\n\`\`\`\n${output.details}\n\`\`\``,
          type: 'file_operation',
          metadata: output.metadata
        };
      
      case 'code_generation':
        return {
          content: `🔧 Code Generated:\n\`\`\`${output.language || ''}\n${output.code}\n\`\`\``,
          type: 'code_generation',
          metadata: output.metadata
        };
      
      case 'agent_thinking':
        return {
          content: `💭 ${output.content}`,
          type: 'thinking',
          metadata: output.metadata
        };
      
      case 'tool_execution':
        return {
          content: `⚡ Tool: ${output.tool}\n${output.result}`,
          type: 'tool_execution',
          metadata: output.metadata
        };
      
      default:
        return {
          content: output.content || output,
          type: 'text',
          metadata: output.metadata || {}
        };
    }
  }
}
```

### Error Handling and Recovery

**Robust Error Management:**
```javascript
// artist-core/services/claude-code/ErrorHandler.js
class ClaudeCodeErrorHandler {
  constructor(librechatAPI, claudeCodeWrapper) {
    this.api = librechatAPI;
    this.claudeCode = claudeCodeWrapper;
    this.errorPatterns = new Map();
    this.recoveryStrategies = new Map();
    this.initializeErrorPatterns();
  }

  initializeErrorPatterns() {
    // Common Claude Code error patterns and recovery strategies
    this.errorPatterns.set(/Permission denied/, {
      type: 'permission_error',
      severity: 'high',
      recovery: 'check_file_permissions'
    });

    this.errorPatterns.set(/No such file or directory/, {
      type: 'file_not_found',
      severity: 'medium',
      recovery: 'create_missing_file'
    });

    this.errorPatterns.set(/API rate limit exceeded/, {
      type: 'rate_limit',
      severity: 'medium',
      recovery: 'retry_with_backoff'
    });

    this.errorPatterns.set(/Invalid project structure/, {
      type: 'project_structure',
      severity: 'high',
      recovery: 'initialize_project_structure'
    });
  }

  async handleError(error, context) {
    const errorInfo = this.analyzeError(error);
    const recoveryStrategy = this.getRecoveryStrategy(errorInfo);
    
    // Log error for debugging
    this.logError(error, errorInfo, context);
    
    // Attempt recovery if possible
    if (recoveryStrategy) {
      const recoveryResult = await this.attemptRecovery(recoveryStrategy, context);
      if (recoveryResult.success) {
        return recoveryResult;
      }
    }
    
    // If recovery fails, provide user-friendly error message
    return this.createUserFriendlyError(errorInfo, context);
  }

  analyzeError(error) {
    const errorMessage = error.message || error.toString();
    
    for (const [pattern, info] of this.errorPatterns) {
      if (pattern.test(errorMessage)) {
        return {
          ...info,
          originalError: error,
          message: errorMessage,
          timestamp: new Date().toISOString()
        };
      }
    }
    
    return {
      type: 'unknown',
      severity: 'medium',
      originalError: error,
      message: errorMessage,
      timestamp: new Date().toISOString()
    };
  }

  async attemptRecovery(strategy, context) {
    switch (strategy) {
      case 'check_file_permissions':
        return this.fixFilePermissions(context);
      case 'create_missing_file':
        return this.createMissingFile(context);
      case 'retry_with_backoff':
        return this.retryWithBackoff(context);
      case 'initialize_project_structure':
        return this.initializeProjectStructure(context);
      default:
        return { success: false, reason: 'No recovery strategy available' };
    }
  }

  createUserFriendlyError(errorInfo, context) {
    const userMessages = {
      permission_error: 'File permission issue detected. Please check if Claude Code has proper access to your project directory.',
      file_not_found: 'Required file not found. This might be due to incorrect project structure.',
      rate_limit: 'API rate limit reached. Please wait a moment before retrying.',
      project_structure: 'Project structure issue detected. Consider reinitializing your project.',
      unknown: 'An unexpected error occurred. Please check the logs for more details.'
    };

    return {
      success: false,
      error: {
        type: errorInfo.type,
        userMessage: userMessages[errorInfo.type] || userMessages.unknown,
        technicalDetails: errorInfo.message,
        suggestions: this.getErrorSuggestions(errorInfo.type),
        timestamp: errorInfo.timestamp
      }
    };
  }
}
```

## Integration Testing Strategy

### Test Suite Architecture

**Comprehensive Testing Framework:**
```javascript
// artist-core/tests/claude-code-integration.test.js
describe('Claude Code Integration', () => {
  let claudeCodeWrapper;
  let librechatAPI;
  let testProjectPath;

  beforeEach(async () => {
    librechatAPI = new MockLibreChatAPI();
    claudeCodeWrapper = new ClaudeCodeWrapper(librechatAPI);
    testProjectPath = await createTestProject();
  });

  describe('Basic Integration', () => {
    test('should initialize Claude Code wrapper successfully', async () => {
      expect(claudeCodeWrapper).toBeDefined();
      expect(claudeCodeWrapper.claudeCodePath).toBeTruthy();
    });

    test('should execute simple Claude Code operation', async () => {
      const result = await claudeCodeWrapper.executeClaudeCodeOperation({
        agentId: 'test-agent',
        projectPath: testProjectPath,
        command: { type: 'task', task: 'List project files' },
        context: { phase: 'A', agentRole: 'analyst' }
      });

      expect(result.success).toBe(true);
      expect(result.output).toContain(testProjectPath);
    });
  });

  describe('Agent Integration', () => {
    test('should register agent for Claude Code operations', async () => {
      const agentBridge = new AgentClaudeCodeBridge(librechatAPI, claudeCodeWrapper);
      
      const agent = await agentBridge.registerAgent({
        id: 'test-agent',
        name: 'Test Agent'
      }, {
        workflowId: 'test-workflow',
        phase: 'A',
        agentRole: 'analyst',
        projectPath: testProjectPath
      });

      expect(agent.claudeCodeCapabilities).toBeDefined();
    });

    test('should execute agent task via Claude Code', async () => {
      const agentBridge = new AgentClaudeCodeBridge(librechatAPI, claudeCodeWrapper);
      
      await agentBridge.registerAgent({
        id: 'test-agent',
        name: 'Test Agent'
      }, {
        workflowId: 'test-workflow',
        phase: 'A',
        agentRole: 'analyst',
        projectPath: testProjectPath
      });

      const result = await agentBridge.executeAgentTask('test-agent', {
        instructions: 'Analyze project structure',
        successCriteria: 'Provide comprehensive project analysis'
      });

      expect(result.success).toBe(true);
      expect(result.analysis).toBeDefined();
    });
  });

  describe('Error Handling', () => {
    test('should handle Claude Code process errors gracefully', async () => {
      const result = await claudeCodeWrapper.executeClaudeCodeOperation({
        agentId: 'test-agent',
        projectPath: '/nonexistent/path',
        command: { type: 'task', task: 'Test task' },
        context: { phase: 'A' }
      });

      expect(result.success).toBe(false);
      expect(result.error.userMessage).toContain('File permission issue');
    });
  });
});
```

## Deployment and Monitoring

### Performance Monitoring

**Claude Code Integration Metrics:**
```javascript
// artist-core/monitoring/ClaudeCodeMetrics.js
class ClaudeCodeMetrics {
  constructor() {
    this.metrics = {
      executions: 0,
      successRate: 0,
      averageExecutionTime: 0,
      errorsByType: new Map(),
      agentPerformance: new Map()
    };
  }

  trackExecution(execution) {
    this.metrics.executions++;
    
    if (execution.success) {
      this.updateSuccessRate();
    } else {
      this.trackError(execution.error);
    }
    
    this.updateExecutionTime(execution.duration);
    this.trackAgentPerformance(execution.agentId, execution);
  }

  generateReport() {
    return {
      total_executions: this.metrics.executions,
      success_rate: this.metrics.successRate,
      average_execution_time: this.metrics.averageExecutionTime,
      error_breakdown: Object.fromEntries(this.metrics.errorsByType),
      top_performing_agents: this.getTopPerformingAgents(),
      recommendations: this.generateRecommendations()
    };
  }
}
```

This comprehensive Claude Code wrapper integration plan provides a robust foundation for seamlessly incorporating Claude Code's powerful capabilities into the LibreChat-based ARTIST Core framework, enabling sophisticated multi-agent workflows with direct access to Claude Code's file manipulation and project management features.