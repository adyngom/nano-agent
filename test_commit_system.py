#!/usr/bin/env python3
"""
Test script for the comprehensive commit system.
Tests atomic commits, comprehensive commits, and template generation.
"""

import json
import sys
import subprocess
from pathlib import Path

# Add the hooks directory to the path so we can import modules
hooks_dir = Path(__file__).parent / '.claude' / 'hooks'
sys.path.append(str(hooks_dir))
sys.path.append(str(hooks_dir / 'utils'))

from commit_templates import (
    CommitTemplates,
    create_atomic_commit_message,
    create_comprehensive_commit_message
)


def test_atomic_commit_templates():
    """Test atomic commit message generation."""
    print("=== Testing Atomic Commit Templates ===")
    
    # Test TodoWrite completion
    todo_input = {
        'todos': [
            {'content': 'Create CG analyzer agent', 'status': 'completed'},
            {'content': 'Update configuration files', 'status': 'completed'},
            {'content': 'Test the implementation', 'status': 'pending'}
        ]
    }
    
    message = create_atomic_commit_message('TodoWrite', todo_input)
    print("TodoWrite completion message:")
    print(message)
    print("\n" + "="*50 + "\n")
    
    # Test file creation
    write_input = {
        'file_path': '/path/to/.claude/agents/artist/cg-analyzer.md'
    }
    
    message = create_atomic_commit_message('Write', write_input)
    print("File creation message:")
    print(message)
    print("\n" + "="*50 + "\n")
    
    # Test file edit
    edit_input = {
        'file_path': '/path/to/.claude/settings.json'
    }
    
    message = create_atomic_commit_message('Edit', edit_input)
    print("File edit message:")
    print(message)
    print("\n" + "="*50 + "\n")


def test_comprehensive_commit_templates():
    """Test comprehensive commit message generation."""
    print("=== Testing Comprehensive Commit Templates ===")
    
    session_actions = [
        "Create CG Analyzer agent (.claude/agents/artist/cg-analyzer.md)",
        "Create CG Planner agent (.claude/agents/artist/cg-planner.md)",
        "Create CG Implementer agent (.claude/agents/artist/cg-implementer.md)",
        "Create /cg-issue command (.claude/commands/artist/cg-issue.md)",
        "Create /cg-init command (.claude/commands/artist/cg-init.md)",
        "Create /cg-legacy command (.claude/commands/artist/cg-legacy.md)",
        "Update plan document with completed tasks"
    ]
    
    session_id = "test_session_20250812_123456"
    
    message = create_comprehensive_commit_message(
        session_actions=session_actions,
        session_id=session_id,
        primary_goal="implement CG workflow with nano-agent"
    )
    
    print("Comprehensive session commit message:")
    print(message)
    print("\n" + "="*50 + "\n")


def test_workflow_milestone_template():
    """Test CG workflow milestone commit template."""
    print("=== Testing CG Workflow Milestone Template ===")
    
    milestone_details = [
        "Created 3 specialized agents with optimal model selection",
        "Implemented nano-agent delegation for cost optimization",
        "Added proper error handling and state management"
    ]
    
    message = CommitTemplates.workflow_milestone_template(
        milestone="CG Agent Configuration",
        phase="Phase 1",
        details=milestone_details
    )
    
    print("Workflow milestone message:")
    print(message)
    print("\n" + "="*50 + "\n")


def test_git_status():
    """Test git status checking."""
    print("=== Testing Git Status ===")
    
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            changes = result.stdout.strip()
            if changes:
                print(f"Git status shows {len(changes.split())} changes:")
                print(changes)
            else:
                print("No git changes detected")
        else:
            print("Git status failed:", result.stderr)
            
    except Exception as e:
        print(f"Git status error: {e}")
    
    print("\n" + "="*50 + "\n")


def main():
    """Run all commit system tests."""
    print("🧪 Testing Claude Code Commit System")
    print("="*60)
    
    try:
        test_atomic_commit_templates()
        test_comprehensive_commit_templates()
        test_workflow_milestone_template()
        test_git_status()
        
        print("✅ All commit system tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())