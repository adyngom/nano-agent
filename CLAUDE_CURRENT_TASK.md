CG Workflow Agent Creation Implementation Plan                  
                                                              
 Executive Summary                                            
                                                              
 Following the architectural revision to an agent-centric     
 approach, we are now implementing the core CG workflow       
 agents in Claude Code's .claude/agents/ directory. The       
 modus operandi is "agent creation and coordination" -        
 users interact via @agent-name with intelligent hooks        
 providing workflow automation and suggestions.               
                                                              
 Key Implementation Focus                                     
                                                              
 🎯 Primary Architecture: Agent Creation & Coordination       
                                                              
 The CG workflow operates through specialized Claude Code     
 agents that coordinate via file-based state management:     
 1. @cg-init → Smart project initialization and routing       
 2. @cg-analyzer → CTO-level technical analysis               
 3. @cg-planner → Comprehensive test strategy development     
 4. @cg-implementer → TDD implementation with specialized     
    agent coordination                                        
 5. @cg-doctor → Workflow diagnostics and recovery            
 6. @cg-legacy → Legacy code modernization                    
                                                              
 🏗️ Coordination Mechanism: File-Based State Management      
                                                              
 Agents coordinate through structured markdown files:         
 - PRD_*.md → Business requirements (from TOP_OF_WORKFLOW)    
 - UX_STRATEGY_*.md → Design strategy (from TOP_OF_WORKFLOW)  
 - CG_TDD_<issue>.md → Technical analysis (@cg-analyzer)      
 - CG_TDD_TESTS_<issue>.md → Test strategy (@cg-planner)      
 - CG_TDD_IMPLEMENTATION_<issue>.md → Implementation docs     
   (@cg-implementer)                                          
 - CG_WORKFLOW_STATE.md → Overall workflow state tracking    
                                                              
 🔍 Hook Enhancement Strategy                                 
                                                              
 Intelligent workflow automation through enhanced hooks:      
 - Session hooks detect user intent and suggest appropriate   
   agents                                                     
 - Post-tool hooks coordinate agent handoffs and suggest     
   next workflow steps                                        
 - File-based state preservation across agent executions     
                                                              
 Current Implementation Status                                
                                                              
 Phase 1: Core Agent Creation (Week 1-2) - IN PROGRESS       
                                                              
 ✅ Architecture Revision Complete                            
 - CG_WORKFLOW_IMPLEMENTATION_PLAN.md updated to             
   agent-centric approach                                     
 - Clear specification of agent responsibilities and          
   coordination protocols                                     
 - File-based state management design completed               
                                                              
 🚧 Agent Creation Tasks (Priority 1)                        
                                                              
 1. Create @cg-init Agent                                     
    - Smart project initialization and workflow routing       
    - Detect existing PRD/UX files vs. new project start     
    - Coordinate with TOP_OF_WORKFLOW agents for new         
      projects                                                
    - Transition to technical implementation for continuing   
      projects                                                
                                                              
 2. Create @cg-analyzer Agent                                 
    - CTO-level technical analysis using Claude Opus 4.1     
    - System impact assessment and architecture strategy      
    - Generate CG_TDD_<issue>.md technical analysis          
      documents                                               
    - Read PRD/UX context for comprehensive analysis         
                                                              
 3. Create @cg-planner Agent                                  
    - Senior Test Engineer using Claude Sonnet 4             
    - Comprehensive test strategy development                 
    - Generate CG_TDD_TESTS_<issue>.md test plan documents   
    - TDD-first planning with coverage and quality gates     
                                                              
 4. Create @cg-implementer Agent                              
    - Senior Developer using Claude Sonnet 4                 
    - TDD implementation with specialized agent coordination  
    - Access to @gemini-security-agent, @architecture-       
      reviewer, @claude-git-assistant                         
    - Generate CG_TDD_IMPLEMENTATION_<issue>.md              
      documentation                                           
                                                              
 🎯 Agent Frontmatter Standards                               
                                                              
 All CG agents follow standardized frontmatter format:       
 ---                                                          
 name: agent-name                                             
 description: Clear description with coordination             
 capabilities                                                 
 model: opus|sonnet|gemini                                    
 color: blue|purple|green|orange|red|yellow                  
 tools: mcp__nano-agent__prompt_nano_agent                   
 ---                                                          
                                                              
 Implementation Strategy                                      
                                                              
 Phase 1: Core Agents (Days 1-7)                             
                                                              
 Day 1-2: @cg-init Agent Creation                             
 - Implement project state detection logic                   
 - Create routing logic for new vs. continuing projects      
 - Add coordination with TOP_OF_WORKFLOW agents              
 - Test with existing PRD/UX files                           
                                                              
 Day 3-4: @cg-analyzer Agent Creation                         
 - Implement technical analysis system prompts               
 - Create CG_TDD_<issue>.md output format                    
 - Add context reading from PRD/UX files                     
 - Test with sample GitHub issues                            
                                                              
 Day 5-6: @cg-planner Agent Creation                          
 - Implement test strategy development prompts               
 - Create CG_TDD_TESTS_<issue>.md output format              
 - Add analysis context reading capabilities                 
 - Test TDD planning workflows                               
                                                              
 Day 7: @cg-implementer Agent Creation                        
 - Implement TDD development system prompts                  
 - Add specialized agent coordination capabilities           
 - Create implementation documentation format                
 - Test end-to-end agent workflow                            
                                                              
 Phase 2: Agent Coordination (Days 8-14)                     
                                                              
 Day 8-10: File-Based State Management                       
 - Implement workflow state tracking                         
 - Create CG_WORKFLOW_STATE.md management                    
 - Add agent context loading protocols                       
 - Test context preservation across agent handoffs          
                                                              
 Day 11-12: Hook Enhancement                                  
 - Enhance session_start.py for agent suggestions           
 - Create post_tool_use.py workflow coordination            
 - Add implicit agent detection patterns                     
 - Test intelligent workflow automation                       
                                                              
 Day 13-14: Integration Testing                               
 - Test complete agent workflows                             
 - Validate file-based coordination                          
 - Test hook automation and suggestions                      
 - Document agent usage patterns                             
                                                              
 Integration with Existing Components                        
                                                              
 🔗 TOP_OF_WORKFLOW Integration                               
                                                              
 CG agents integrate seamlessly with existing                
 TOP_OF_WORKFLOW agents:                                      
 - @cg-init coordinates with @business-analyst-expert for    
   PRD creation                                               
 - @cg-init coordinates with @ui-ux-strategy-expert for      
   design strategy                                            
 - @cg-analyzer reads PRD/UX context for technical          
   analysis                                                   
                                                              
 🔗 Specialized Agent Integration                             
                                                              
 @cg-implementer coordinates with specialized agents:        
 - @gemini-security-agent for cost-effective security        
   reviews                                                    
 - @architecture-reviewer for code quality analysis          
 - @claude-git-assistant for commit automation               
 - @error-pattern-analyzer for debugging support             
                                                              
 🔗 Nano-Agent MCP Server Foundation                          
                                                              
 All CG agents use mcp__nano-agent__prompt_nano_agent        
 tool for:                                                    
 - Multi-provider LLM orchestration                          
 - File system operations and documentation generation       
 - Specialized task execution and coordination               
                                                              
 Success Criteria                                             
                                                              
 Phase 1 Completion Metrics                                  
                                                              
 - [ ] @cg-init agent functional and tested                  
 - [ ] @cg-analyzer generates proper CG_TDD_*.md files       
 - [ ] @cg-planner creates comprehensive test strategies     
 - [ ] @cg-implementer coordinates with specialized agents   
 - [ ] File-based state management operational               
 - [ ] Hook suggestions working for agent workflow           
 - [ ] Context preservation across agent handoffs           
                                                              
 User Experience Goals                                        
                                                              
 - Users can start projects with natural language ("I want  
   to build...")                                             
 - Hooks suggest appropriate agents automatically            
 - Agents coordinate seamlessly through file-based state    
 - Clear workflow progression from idea to implementation    
 - Intelligent recovery and diagnostics via @cg-doctor      
                                                              
 Next Steps                                                   
                                                              
 Immediate Actions (Today)                                    
                                                              
 1. Create @cg-init agent with project state detection       
 2. Test integration with existing TOP_OF_WORKFLOW agents    
 3. Implement basic file-based coordination                  
 4. Begin @cg-analyzer agent development                      
                                                              
 Week 1 Milestones                                           
                                                              
 1. All 4 core CG agents created and functional              
 2. Basic agent coordination through file state working      
 3. Integration with TOP_OF_WORKFLOW agents tested           
 4. Hook enhancements for agent suggestions implemented      
                                                              
 Week 2 Completion                                            
                                                              
 1. Advanced agent features (@cg-doctor, @cg-legacy)         
 2. Comprehensive testing and validation                     
 3. Documentation and usage examples                         
 4. Ready for production use and team adoption               
                                                              
 Architecture Benefits                                        
                                                              
 Agent-Centric Advantages                                     
                                                              
 - Natural Integration: Works within Claude Code's existing  
   @agent-name interface                                      
 - Intelligent Coordination: Hooks provide smart            
   suggestions and automation                                 
 - State Preservation: File-based coordination maintains     
   context across sessions                                    
 - Specialized Expertise: Each agent has deep domain        
   knowledge and optimal model selection                     
 - Cost Optimization: Strategic model usage (Opus for       
   analysis, Sonnet for implementation, Gemini for security) 
                                                              
 Workflow Completeness                                        
                                                              
 - Complete Coverage: From business idea (TOP_OF_WORKFLOW)   
   to production code (CG agents)                            
 - Quality Assurance: Built-in TDD methodology and          
   specialized reviews                                        
 - Documentation: Comprehensive documentation generation     
   at every step                                             
 - Recovery: @cg-doctor for workflow diagnostics and        
   state recovery                                            
 - Legacy Support: @cg-legacy for modernizing existing      
   codebases                                                 
                                                              
 This implementation creates a complete agent ecosystem      
 that transforms business ideas into production-ready       
 applications through intelligent coordination and          
 specialized expertise.                    