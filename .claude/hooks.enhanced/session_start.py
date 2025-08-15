#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from utils.constants import ensure_session_log_dir

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def log_session_start(session_id, input_data):
    """Log session start event to session directory."""
    # Ensure session log directory exists
    log_dir = ensure_session_log_dir(session_id)
    log_file = log_dir / 'session_start.json'
    
    # Read existing log data or initialize empty list
    if log_file.exists():
        with open(log_file, 'r') as f:
            try:
                log_data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                log_data = []
    else:
        log_data = []
    
    # Append the entire input data
    log_data.append(input_data)
    
    # Write back to file with formatting
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)


def get_git_status():
    """Get current git status information."""
    try:
        # Get current branch
        branch_result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5
        )
        current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"
        
        # Get uncommitted changes count
        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if status_result.returncode == 0:
            changes = status_result.stdout.strip().split('\n') if status_result.stdout.strip() else []
            uncommitted_count = len(changes)
        else:
            uncommitted_count = 0
        
        return current_branch, uncommitted_count
    except Exception:
        return None, None


def get_recent_issues():
    """Get recent GitHub issues if gh CLI is available."""
    try:
        # Check if gh is available
        gh_check = subprocess.run(['which', 'gh'], capture_output=True)
        if gh_check.returncode != 0:
            return None
        
        # Get recent open issues
        result = subprocess.run(
            ['gh', 'issue', 'list', '--limit', '5', '--state', 'open'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return None


def is_coding_task(prompt):
    """Detect if the prompt indicates a coding/development task."""
    if not prompt or len(prompt.strip()) < 10:
        return False
        
    prompt_lower = prompt.lower()
    
    # Coding action keywords
    coding_keywords = [
        'implement', 'fix', 'add', 'create', 'refactor', 'update', 'modify', 
        'build', 'develop', 'code', 'debug', 'optimize', 'enhance', 'extend',
        'integrate', 'configure', 'setup', 'install', 'deploy', 'migrate',
        'test', 'write tests', 'unit test', 'integration test'
    ]
    
    # Technical patterns
    technical_patterns = [
        'function', 'class', 'method', 'api', 'endpoint', 'database', 'sql',
        'component', 'module', 'service', 'library', 'framework', 'package',
        'bug', 'issue #', 'error', 'exception', 'performance', 'security'
    ]
    
    # File/code references
    code_patterns = [
        '.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c', '.rb',
        '.php', '.html', '.css', '.json', '.yaml', '.yml', '.md', '.sql',
        'src/', 'lib/', 'test/', 'spec/', 'apps/', 'components/'
    ]
    
    # Check for coding keywords
    if any(keyword in prompt_lower for keyword in coding_keywords):
        return True
    
    # Check for technical patterns
    if any(pattern in prompt_lower for pattern in technical_patterns):
        return True
        
    # Check for file/code references
    if any(pattern in prompt_lower for pattern in code_patterns):
        return True
    
    # Exclude simple questions and greetings
    simple_patterns = [
        'hello', 'hi', 'how are', 'what is', 'explain', 'help me understand',
        'can you tell', 'show me', 'what does', 'where is', 'who is'
    ]
    
    # If it starts with simple question patterns, likely not a coding task
    if any(prompt_lower.strip().startswith(pattern) for pattern in simple_patterns):
        return False
    
    return False


def extract_task_description(prompt):
    """Extract a clean task description from the user prompt."""
    if not prompt:
        return None
    
    # Clean up the prompt
    clean_prompt = prompt.strip()
    
    # Remove common prefixes
    prefixes_to_remove = [
        'can you ', 'could you ', 'please ', 'i need to ', 'help me ',
        'i want to ', 'i would like to ', 'let\'s ', 'we need to '
    ]
    
    clean_lower = clean_prompt.lower()
    for prefix in prefixes_to_remove:
        if clean_lower.startswith(prefix):
            clean_prompt = clean_prompt[len(prefix):]
            break
    
    # Capitalize first letter
    clean_prompt = clean_prompt.strip()
    if clean_prompt:
        clean_prompt = clean_prompt[0].upper() + clean_prompt[1:]
    
    return clean_prompt


def generate_adw_id():
    """Generate a unique ADW ID based on timestamp."""
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def create_auto_plan(prompt):
    """Create a plan automatically for coding tasks."""
    try:
        # Generate unique ADW ID
        adw_id = generate_adw_id()
        
        # Extract clean task description
        task_description = extract_task_description(prompt)
        if not task_description:
            return None
        
        # Use the plan command to create the plan
        # We'll invoke the plan command through subprocess
        plan_command = [
            'uv', 'run', '-c', 
            f'cd /Users/zero2hero/Code/Liveprojects/nano-agent && claude-code /plan {adw_id} "{task_description}"'
        ]
        
        # For now, we'll create a simple announcement that a plan should be created
        # The actual plan creation will be handled by Claude Code when it processes this
        return {
            "auto_plan_suggestion": {
                "adw_id": adw_id,
                "task_description": task_description,
                "plan_command": f"/plan {adw_id} \"{task_description}\"",
                "detected_as_coding_task": True
            }
        }
        
    except Exception as e:
        # If plan creation fails, don't break the session
        return {
            "auto_plan_error": {
                "error": str(e),
                "fallback": "Consider running /plan manually for this coding task"
            }
        }


def get_user_prompt_from_input(input_data):
    """Extract user prompt from session input data."""
    try:
        # The user prompt might be in different fields depending on session type
        if 'user_prompt' in input_data:
            return input_data['user_prompt']
        elif 'prompt' in input_data:
            return input_data['prompt']
        elif 'message' in input_data:
            return input_data['message']
        # Add more potential fields as needed
        return None
    except Exception:
        return None


def load_development_context(source):
    """Load relevant development context based on session source."""
    context_parts = []
    
    # Add timestamp
    context_parts.append(f"Session started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    context_parts.append(f"Session source: {source}")
    
    # Add git information
    branch, changes = get_git_status()
    if branch:
        context_parts.append(f"Git branch: {branch}")
        if changes > 0:
            context_parts.append(f"Uncommitted changes: {changes} files")
    
    # Load project-specific context files if they exist
    context_files = [
        ".claude/CONTEXT.md",
        ".claude/TODO.md",
        "TODO.md",
        ".github/ISSUE_TEMPLATE.md"
    ]
    
    for file_path in context_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        context_parts.append(f"\n--- Content from {file_path} ---")
                        context_parts.append(content[:1000])  # Limit to first 1000 chars
            except Exception:
                pass
    
    # Add recent issues if available
    issues = get_recent_issues()
    if issues:
        context_parts.append("\n--- Recent GitHub Issues ---")
        context_parts.append(issues)
    
    return "\n".join(context_parts)


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--load-context', action='store_true',
                          help='Load development context at session start')
        parser.add_argument('--announce', action='store_true',
                          help='Announce session start via TTS')
        parser.add_argument('--auto-plan', action='store_true',
                          help='Automatically create plan for coding tasks')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = json.loads(sys.stdin.read())
        
        # Extract fields
        session_id = input_data.get('session_id', 'unknown')
        source = input_data.get('source', 'unknown')  # "startup", "resume", or "clear"
        
        # Log the session start event
        log_session_start(session_id, input_data)
        
        # Initialize output
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart"
            }
        }
        
        # Load development context if requested
        if args.load_context:
            context = load_development_context(source)
            if context:
                output["hookSpecificOutput"]["additionalContext"] = context
        
        # Auto-plan functionality
        if args.auto_plan:
            user_prompt = get_user_prompt_from_input(input_data)
            if user_prompt and is_coding_task(user_prompt):
                plan_info = create_auto_plan(user_prompt)
                if plan_info:
                    output["hookSpecificOutput"]["autoPlan"] = plan_info
        
        # Output results if we have any
        if len(output["hookSpecificOutput"]) > 1:  # More than just hookEventName
            print(json.dumps(output))
            sys.exit(0)
        
        # Announce session start if requested
        if args.announce:
            try:
                # Try to use TTS to announce session start
                script_dir = Path(__file__).parent
                tts_script = script_dir / "utils" / "tts" / "pyttsx3_tts.py"
                
                if tts_script.exists():
                    messages = {
                        "startup": "Claude Code session started",
                        "resume": "Resuming previous session",
                        "clear": "Starting fresh session"
                    }
                    message = messages.get(source, "Session started")
                    
                    subprocess.run(
                        ["uv", "run", str(tts_script), message],
                        capture_output=True,
                        timeout=5
                    )
            except Exception:
                pass
        
        # Success
        sys.exit(0)
        
    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)


if __name__ == '__main__':
    main()