#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime
from utils.constants import ensure_session_log_dir
from utils.commit_templates import create_atomic_commit_message


def generate_adw_id():
    """Generate a unique ADW ID based on timestamp."""
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def extract_task_name_from_plan(plan_content):
    """Extract a meaningful task name from the plan content."""
    if not plan_content:
        return "task"
    
    # Try to extract from the first line or header
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


def detect_task_complexity(plan_content):
    """Analyze plan content to determine task complexity."""
    if not plan_content:
        return "simple"
    
    content_lower = plan_content.lower()
    
    # Complex indicators
    complex_indicators = [
        'architecture', 'design pattern', 'database', 'api', 'security',
        'integration', 'performance', 'scalability', 'testing strategy',
        'multiple phases', 'dependencies', 'migration', 'refactor'
    ]
    
    # Medium indicators  
    medium_indicators = [
        'component', 'module', 'service', 'endpoint', 'authentication',
        'validation', 'error handling', 'configuration', 'logging'
    ]
    
    complex_count = sum(1 for indicator in complex_indicators if indicator in content_lower)
    medium_count = sum(1 for indicator in medium_indicators if indicator in content_lower)
    
    # Count implementation phases/steps
    phase_patterns = [
        r'phase \d+', r'step \d+', r'stage \d+', 
        r'### \d+\.', r'## \d+\.', r'# \d+\.'
    ]
    phase_count = sum(len(re.findall(pattern, content_lower)) for pattern in phase_patterns)
    
    if complex_count >= 2 or phase_count >= 4:
        return "complex"
    elif medium_count >= 2 or phase_count >= 2:
        return "medium" 
    else:
        return "simple"


def extract_sections_from_plan(plan_content):
    """Extract key sections from plan content for spec generation."""
    if not plan_content:
        return {}
    
    sections = {
        'objective': '',
        'problem_statement': '',
        'solution_approach': '',
        'steps': [],
        'acceptance_criteria': [],
        'validation_commands': []
    }
    
    # Split into lines for processing
    lines = plan_content.split('\n')
    current_section = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        line_lower = line.lower()
        
        # Detect section headers
        if any(keyword in line_lower for keyword in ['objective', 'goal', 'purpose']):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = 'objective'
            current_content = []
        elif any(keyword in line_lower for keyword in ['problem', 'issue', 'challenge']):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = 'problem_statement'
            current_content = []
        elif any(keyword in line_lower for keyword in ['solution', 'approach', 'strategy']):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = 'solution_approach'
            current_content = []
        elif any(keyword in line_lower for keyword in ['step', 'implementation', 'task']):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = 'steps'
            current_content = []
        elif any(keyword in line_lower for keyword in ['acceptance', 'criteria', 'success']):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = 'acceptance_criteria'
            current_content = []
        elif any(keyword in line_lower for keyword in ['validation', 'test', 'verify']):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = 'validation_commands'
            current_content = []
        elif line:
            current_content.append(line)
    
    # Don't forget the last section
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content)
    
    return sections


def create_spec_from_plan(plan_content, adw_id, task_name):
    """Create a spec file from approved plan content."""
    try:
        # Ensure specs directory exists
        specs_dir = Path('specs')
        specs_dir.mkdir(exist_ok=True)
        
        # Generate spec filename
        spec_filename = f"plan-{adw_id}-{task_name}.md"
        spec_path = specs_dir / spec_filename
        
        # Extract sections from plan
        sections = extract_sections_from_plan(plan_content)
        complexity = detect_task_complexity(plan_content)
        
        # Determine task type based on content
        content_lower = plan_content.lower()
        if any(word in content_lower for word in ['fix', 'bug', 'error']):
            task_type = 'fix'
        elif any(word in content_lower for word in ['refactor', 'restructure', 'reorganize']):
            task_type = 'refactor'
        elif any(word in content_lower for word in ['enhance', 'improve', 'optimize']):
            task_type = 'enhancement'
        elif any(word in content_lower for word in ['implement', 'create', 'add', 'build']):
            task_type = 'feature'
        else:
            task_type = 'chore'
        
        # Create spec content
        spec_content = f"""# Plan: {task_name.replace('-', ' ').title()}

## Metadata
adw_id: `{adw_id}`
prompt: `Auto-generated from plan mode approval`
task_type: {task_type}
complexity: {complexity}

## Task Description
{sections.get('objective', 'Task description extracted from plan mode approval')}

## Objective
{sections.get('objective', 'Complete the implementation as outlined in the approved plan')}
"""

        # Add complex task sections
        if complexity in ['medium', 'complex']:
            if sections.get('problem_statement'):
                spec_content += f"""
## Problem Statement
{sections['problem_statement']}
"""
            
            if sections.get('solution_approach'):
                spec_content += f"""
## Solution Approach
{sections['solution_approach']}
"""

        spec_content += """
## Relevant Files
Use these files to complete the task:

- Files will be determined during implementation based on the specific requirements

"""

        # Add implementation phases for complex tasks
        if complexity == 'complex':
            spec_content += """## Implementation Phases
### Phase 1: Foundation
- Analyze existing codebase and understand current patterns
- Set up any necessary dependencies or configurations

### Phase 2: Core Implementation  
- Implement the main functionality as outlined in the plan
- Follow existing code conventions and patterns

### Phase 3: Integration & Polish
- Integrate with existing systems
- Add proper error handling and validation
- Update documentation as needed

"""

        # Add step-by-step tasks
        steps_content = sections.get('steps', plan_content)
        spec_content += f"""## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Implementation
{steps_content}

### 2. Validation
- Test the implementation thoroughly
- Verify all requirements are met
- Run any applicable test suites

"""

        # Add testing strategy for complex tasks
        if complexity in ['medium', 'complex']:
            spec_content += """## Testing Strategy
- Unit tests for individual components
- Integration tests for system interactions  
- Manual testing for user-facing features
- Edge case validation

"""

        # Add acceptance criteria
        acceptance_criteria = sections.get('acceptance_criteria', """- Implementation matches the approved plan
- All functionality works as expected
- Code follows existing patterns and conventions
- No breaking changes to existing functionality""")
        
        spec_content += f"""## Acceptance Criteria
{acceptance_criteria}

## Validation Commands
Execute these commands to validate the task is complete:

"""
        
        # Add validation commands
        validation_commands = sections.get('validation_commands', """- `uv run python -m py_compile apps/nano_agent_mcp_server/src/**/*.py` - Test code compilation
- Run any applicable test suites
- Verify functionality through manual testing""")
        
        spec_content += validation_commands + """

## Notes
This plan was auto-generated from plan mode approval. Refer to the original plan discussion for additional context and details.
"""

        # Write the spec file
        with open(spec_path, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        return spec_path
        
    except Exception as e:
        # Don't break the hook if spec creation fails
        return None


def handle_exit_plan_mode(input_data):
    """Handle ExitPlanMode tool completion and generate spec file."""
    try:
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        tool_result = input_data.get('tool_result', {})
        
        # Check if this is an ExitPlanMode call
        if tool_name != 'ExitPlanMode':
            return None
        
        # Check if the plan was approved (success result)
        if not tool_result.get('success', False):
            return None
        
        # Extract plan content from tool input
        plan_content = tool_input.get('plan', '')
        if not plan_content:
            return None
        
        # Generate ADW ID and task name
        adw_id = generate_adw_id()
        task_name = extract_task_name_from_plan(plan_content)
        
        # Create the spec file
        spec_path = create_spec_from_plan(plan_content, adw_id, task_name)
        
        return {
            'auto_spec_generated': True,
            'spec_file': str(spec_path) if spec_path else None,
            'adw_id': adw_id,
            'task_name': task_name
        }
        
    except Exception:
        # Don't break the hook on errors
        return None


def detect_task_completion(input_data):
    """Detect if a task was completed based on tool usage patterns."""
    try:
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        tool_result = input_data.get('tool_result', {})
        
        # Completion indicators
        completion_indicators = [
            # TodoWrite completions
            (tool_name == 'TodoWrite' and any(
                todo.get('status') == 'completed' 
                for todo in tool_input.get('todos', [])
            )),
            # Successful file operations (Write, Edit, MultiEdit)
            (tool_name in ['Write', 'Edit', 'MultiEdit'] and 
             tool_result.get('success', True)),
            # Successful test runs
            (tool_name == 'Bash' and 
             any(cmd in tool_input.get('command', '') for cmd in ['test', 'lint', 'typecheck']) and
             tool_result.get('returncode', 0) == 0),
            # Successful git operations
            (tool_name == 'Bash' and 
             'git' in tool_input.get('command', '') and
             tool_result.get('returncode', 0) == 0)
        ]
        
        return any(completion_indicators)
        
    except Exception:
        return False


def get_git_status():
    """Get current git status for commit decisions."""
    try:
        import subprocess
        
        # Check if there are changes to commit
        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if status_result.returncode == 0:
            changes = status_result.stdout.strip()
            return len(changes.split('\n')) if changes else 0
        
    except Exception:
        pass
    
    return 0


def create_atomic_commit(input_data):
    """Create an atomic commit for a completed task."""
    try:
        import subprocess
        
        # Check if there are changes to commit
        if get_git_status() == 0:
            return None
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Skip git commands to avoid recursive commits
        if tool_name == 'Bash' and 'git' in tool_input.get('command', ''):
            return None
        
        # Generate commit message using templates
        commit_msg = create_atomic_commit_message(tool_name, tool_input)
        
        if not commit_msg:
            return None  # No commit message generated
        
        # Create the commit
        subprocess.run(['git', 'add', '.'], capture_output=True, timeout=10)
        
        commit_result = subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if commit_result.returncode == 0:
            return {
                'atomic_commit_created': True,
                'commit_message': commit_msg,
                'commit_hash': commit_result.stdout.strip()
            }
        else:
            return {
                'atomic_commit_error': commit_result.stderr.strip()
            }
            
    except Exception as e:
        return {
            'atomic_commit_error': str(e)
        }
    
    return None


def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        # Handle ExitPlanMode tool completion
        plan_result = handle_exit_plan_mode(input_data)
        
        # Handle atomic commits for completed tasks
        commit_result = None
        if detect_task_completion(input_data):
            commit_result = create_atomic_commit(input_data)
        
        # Extract session_id
        session_id = input_data.get('session_id', 'unknown')
        
        # Ensure session log directory exists
        log_dir = ensure_session_log_dir(session_id)
        log_path = log_dir / 'post_tool_use.json'
        
        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # Add plan result if generated
        if plan_result:
            input_data['auto_spec_result'] = plan_result
        
        # Add commit result if generated
        if commit_result:
            input_data['atomic_commit_result'] = commit_result
        
        # Append new data
        log_data.append(input_data)
        
        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # Output results
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse"
            }
        }
        
        if plan_result:
            output["hookSpecificOutput"]["autoSpecGenerated"] = plan_result
        
        if commit_result:
            output["hookSpecificOutput"]["atomicCommit"] = commit_result
        
        # Only output if we have results
        if len(output["hookSpecificOutput"]) > 1:
            print(json.dumps(output))
        
        sys.exit(0)
        
    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Exit cleanly on any other error
        sys.exit(0)

if __name__ == '__main__':
    main()