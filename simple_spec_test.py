#!/usr/bin/env python3
"""
Simple test to verify spec generation works with direct function implementation
"""

import re
from pathlib import Path
from datetime import datetime

def generate_adw_id():
    """Generate a unique ADW ID based on timestamp."""
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def extract_task_name_from_plan(plan_content):
    """Extract a meaningful task name from the plan content."""
    if not plan_content:
        return "task"
    
    lines = plan_content.strip().split('\n')
    first_line = lines[0].strip()
    
    # Remove markdown headers
    first_line = re.sub(r'^#+\s*', '', first_line)
    
    # Clean up common prefixes
    prefixes = ['plan:', 'task:', 'implementation:', 'objective:']
    for prefix in prefixes:
        if first_line.lower().startswith(prefix):
            first_line = first_line[len(prefix):].strip()
    
    # Convert to filename-friendly format
    task_name = re.sub(r'[^\w\s-]', '', first_line)
    task_name = re.sub(r'\s+', '-', task_name.strip())
    task_name = task_name.lower()
    
    # Limit length
    if len(task_name) > 30:
        task_name = task_name[:30].rstrip('-')
    
    return task_name or "task"

def create_simple_spec(plan_content, adw_id, task_name):
    """Create a spec file from plan content."""
    try:
        # Ensure specs directory exists
        specs_dir = Path('specs')
        specs_dir.mkdir(exist_ok=True)
        
        # Generate spec filename
        spec_filename = f"plan-{adw_id}-{task_name}.md"
        spec_path = specs_dir / spec_filename
        
        # Create spec content
        spec_content = f"""# Plan: {task_name.replace('-', ' ').title()}

## Metadata
adw_id: `{adw_id}`
prompt: `Auto-generated from plan mode approval`
task_type: feature
complexity: complex

## Task Description
Implement CG Workflow with Nano-Agent Model Switching

## Objective
{plan_content.split('### Objective')[1].split('###')[0].strip() if '### Objective' in plan_content else 'Complete the implementation as outlined in the approved plan'}

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Implementation
{plan_content}

### 2. Validation
- Test the implementation thoroughly
- Verify all requirements are met
- Run any applicable test suites

## Acceptance Criteria
- Implementation matches the approved plan
- All functionality works as expected
- Code follows existing patterns and conventions
- No breaking changes to existing functionality

## Validation Commands
Execute these commands to validate the task is complete:

- `uv run python -m py_compile apps/nano_agent_mcp_server/src/**/*.py` - Test code compilation
- Run any applicable test suites
- Verify functionality through manual testing

## Notes
This plan was auto-generated from plan mode approval. Refer to the original plan discussion for additional context and details.
"""

        # Write the spec file
        with open(spec_path, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        return spec_path
        
    except Exception as e:
        print(f"Error creating spec: {e}")
        return None

def test_simple_spec_generation():
    """Test the spec generation with our CG workflow plan"""
    
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
- Each command uses appropriate nano-agent model for cost optimization"""

    print("🧪 Testing Simple Spec Generation...")
    
    # Generate components
    adw_id = generate_adw_id()
    task_name = extract_task_name_from_plan(plan_content)
    
    print(f"🏷️  Generated ADW ID: {adw_id}")
    print(f"📝 Extracted task name: {task_name}")
    
    # Create the spec
    spec_path = create_simple_spec(plan_content, adw_id, task_name)
    
    if spec_path and spec_path.exists():
        print(f"✅ Spec file created successfully at: {spec_path}")
        
        # Show preview
        with open(spec_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')[:20]
        
        print(f"\n📋 Generated spec preview:")
        print("=" * 60)
        for i, line in enumerate(lines, 1):
            print(f"{i:2d}: {line}")
        print("=" * 60)
        
        return True
    else:
        print(f"❌ Failed to create spec file")
        return False

if __name__ == "__main__":
    success = test_simple_spec_generation()
    print(f"\n{'🎉 SUCCESS!' if success else '💥 FAILED!'}")