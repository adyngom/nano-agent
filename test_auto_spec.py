#!/usr/bin/env python3
"""
Test the auto-spec generation functionality manually
"""

import sys
import os
import json
from pathlib import Path

# Add the hooks directory to path to import our functions
sys.path.append('.claude/hooks')

def test_auto_spec_generation():
    """Test auto-spec generation with the CG workflow plan"""
    
    # Import the functions from our hook
    try:
        from post_tool_use import (
            handle_exit_plan_mode, 
            create_spec_from_plan, 
            generate_adw_id, 
            extract_task_name_from_plan,
            detect_task_complexity
        )
    except ImportError as e:
        print(f"❌ Failed to import functions: {e}")
        return False
    
    # Simulate the ExitPlanMode data from our CG workflow plan
    plan_content = """## Plan: Implement CG Workflow with Nano-Agent Model Switching

### Objective
Implement your Revised CG Workflow using the nano-agent MCP server to achieve reliable LLM/model switching for your three specialized agents: tdd-issue-analyzer (Claude Opus 4.1), tdd-issue-planner (Claude Sonnet 4), and tdd-issue-implementer (Claude Sonnet 4).

### Implementation Strategy
Use the nano-agent MCP server's proven multi-provider architecture to create CG-specific agent configurations that delegate to the exact models your workflow requires.

### Step-by-Step Implementation

#### 1. Create CG Agent Configurations
- Create `.claude/agents/cg-analyzer.md` (Claude Opus 4.1 for CTO-level analysis)
- Create `.claude/agents/cg-planner.md` (Claude Sonnet 4 for test strategy)  
- Create `.claude/agents/cg-implementer.md` (Claude Sonnet 4 for TDD development)
- Each agent delegates to nano-agent MCP server with specific model parameters

#### 2. Implement CG Workflow Commands
- Create `/cg-issue` command that sequentially delegates to the three agents
- Create `/cg-init`, `/cg-legacy`, `/cg-resume`, `/cg-doctor`, `/cg-test` commands
- Each command uses appropriate nano-agent model for cost optimization

#### 3. Add CG-Specific Tools to Nano-Agent
- Extend nano-agent with GitHub issue management tools
- Add project board state management capabilities
- Implement TDD documentation generation tools
- Add test execution and coverage reporting tools

#### 4. Configure Cost-Optimized Model Selection
- Default to Claude Sonnet 4 for most operations (balanced cost/performance)
- Use Claude Opus 4.1 only for deep analysis phase (`/cg-issue` analysis)
- Enable Gemini integration for security reviews and large context analysis
- Implement smart fallback strategies for tool availability

#### 5. Integrate Board State Management
- Create board automation through nano-agent GitHub tools
- Implement automatic column transitions based on TDD progress
- Add failure recovery with proper state rollback
- Track documentation trail throughout workflow

#### 6. Test the Complete Workflow
- Validate model switching works reliably for each agent
- Test sequential agent handoffs with proper context preservation
- Verify cost optimization through targeted expensive model usage
- Ensure board integration and state management works correctly

### Expected Outcome
A fully functional CG workflow that reliably switches between the right LLM models for each phase, automatically manages GitHub board states, and provides cost-optimized development with proper TDD documentation trails."""

    test_data = {
        "session_id": "test-cg-workflow",
        "tool_name": "ExitPlanMode",
        "tool_input": {
            "plan": plan_content
        },
        "tool_result": {
            "success": True
        }
    }
    
    print("🧪 Testing Auto-Spec Generation for CG Workflow...")
    print(f"📄 Plan length: {len(plan_content)} characters")
    
    # Test individual functions first
    adw_id = generate_adw_id()
    task_name = extract_task_name_from_plan(plan_content)
    complexity = detect_task_complexity(plan_content)
    
    print(f"🏷️  Generated ADW ID: {adw_id}")
    print(f"📝 Extracted task name: {task_name}")
    print(f"⚙️  Detected complexity: {complexity}")
    
    # Test the main handler
    result = handle_exit_plan_mode(test_data)
    
    if result:
        print("✅ Auto-spec generation successful!")
        print(f"   🆔 ADW ID: {result['adw_id']}")
        print(f"   📛 Task name: {result['task_name']}")
        print(f"   📄 Spec file: {result['spec_file']}")
        
        # Check if the spec file was actually created
        if result['spec_file'] and Path(result['spec_file']).exists():
            print(f"✅ Spec file created at: {result['spec_file']}")
            
            # Read and display the first few lines
            with open(result['spec_file'], 'r') as f:
                content = f.read()
                lines = content.split('\n')[:15]
                
            print(f"\n📋 Generated spec preview ({len(lines)} lines shown):")
            print("=" * 60)
            for i, line in enumerate(lines, 1):
                print(f"{i:2d}: {line}")
            print("=" * 60)
            print(f"📊 Total spec content: {len(content)} characters, {len(content.split())} words")
            
            return True
        else:
            print(f"❌ Spec file not found at: {result['spec_file']}")
            return False
    else:
        print("❌ Auto-spec generation failed!")
        return False

if __name__ == "__main__":
    success = test_auto_spec_generation()
    if success:
        print("\n🎉 Auto-spec generation test PASSED!")
        print("✅ Ready to implement CG workflow with auto-spec generation")
    else:
        print("\n💥 Auto-spec generation test FAILED!")
        print("❌ Need to debug the implementation")
    
    sys.exit(0 if success else 1)