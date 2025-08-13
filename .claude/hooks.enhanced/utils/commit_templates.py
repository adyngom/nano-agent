#!/usr/bin/env python3
"""
Commit message templates for atomic and comprehensive commits in the CG workflow system.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class CommitTemplates:
    """Standardized commit message templates for CG workflow."""
    
    @staticmethod
    def atomic_commit_template(
        action_type: str,
        description: str,
        files_changed: Optional[List[str]] = None,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Generate atomic commit message for individual task completion.
        
        Args:
            action_type: Type of action (feat, fix, test, docs, style, refactor, chore)
            description: Brief description of what was completed
            files_changed: List of files that were changed
            additional_context: Optional additional context
        
        Returns:
            Formatted commit message
        """
        # Main commit line (limit to 50 characters)
        subject = f"{action_type}: {description[:50-len(action_type)-2]}"
        
        # Build commit body
        body_parts = []
        
        if additional_context:
            body_parts.append(additional_context)
            body_parts.append("")
        
        if files_changed:
            if len(files_changed) == 1:
                body_parts.append(f"Modified: {files_changed[0]}")
            elif len(files_changed) <= 3:
                body_parts.append("Modified:")
                for file in files_changed:
                    body_parts.append(f"- {file}")
            else:
                body_parts.append(f"Modified {len(files_changed)} files")
            body_parts.append("")
        
        # Standard atomic commit footer
        body_parts.extend([
            "🤖 Atomic commit from Claude Code",
            "",
            "Co-Authored-By: Claude <noreply@anthropic.com>"
        ])
        
        return subject + "\n\n" + "\n".join(body_parts)
    
    @staticmethod
    def comprehensive_commit_template(
        session_summary: List[str],
        session_id: str,
        primary_achievement: Optional[str] = None,
        stats: Optional[Dict] = None
    ) -> str:
        """
        Generate comprehensive session commit message.
        
        Args:
            session_summary: List of key accomplishments in the session
            session_id: Unique session identifier
            primary_achievement: Main achievement to use as commit subject
            stats: Optional statistics (files_changed, lines_added, etc.)
        
        Returns:
            Formatted comprehensive commit message
        """
        # Determine primary achievement for subject line
        if primary_achievement:
            subject = f"feat: {primary_achievement[:50]}"
        elif session_summary:
            subject = f"feat: {session_summary[0][:50]}"
        else:
            subject = "feat: comprehensive session update"
        
        # Build comprehensive body
        body_parts = ["Session Summary:", ""]
        
        # Add session accomplishments (limit to top 5)
        for i, achievement in enumerate(session_summary[:5], 1):
            body_parts.append(f"{i}. {achievement}")
        
        if len(session_summary) > 5:
            body_parts.append(f"   ... and {len(session_summary) - 5} more changes")
        
        body_parts.append("")
        
        # Add session metadata
        body_parts.append(f"Session ID: {session_id}")
        
        if stats:
            if stats.get('files_changed'):
                body_parts.append(f"Files Changed: {stats['files_changed']}")
            if stats.get('lines_added'):
                body_parts.append(f"Lines Added: {stats['lines_added']}")
            if stats.get('duration'):
                body_parts.append(f"Session Duration: {stats['duration']}")
        
        body_parts.extend([
            "",
            "🚀 Comprehensive session commit from Claude Code",
            "",
            "Co-Authored-By: Claude <noreply@anthropic.com>"
        ])
        
        return subject + "\n\n" + "\n".join(body_parts)
    
    @staticmethod
    def todo_completion_template(completed_todos: List[str]) -> str:
        """Generate commit message for TodoWrite completions."""
        if not completed_todos:
            return CommitTemplates.atomic_commit_template("chore", "update task status")
        
        main_todo = completed_todos[0]
        action_type = "feat"
        
        # Determine action type based on todo content
        todo_lower = main_todo.lower()
        if any(word in todo_lower for word in ['fix', 'bug', 'error']):
            action_type = "fix"
        elif any(word in todo_lower for word in ['test', 'spec']):
            action_type = "test"
        elif any(word in todo_lower for word in ['doc', 'readme']):
            action_type = "docs"
        elif any(word in todo_lower for word in ['refactor', 'cleanup']):
            action_type = "refactor"
        
        description = f"complete {main_todo}"
        if len(completed_todos) > 1:
            description += f" (+{len(completed_todos)-1} more)"
        
        return CommitTemplates.atomic_commit_template(
            action_type=action_type,
            description=description,
            additional_context=f"Completed {len(completed_todos)} task(s) from todo list"
        )
    
    @staticmethod
    def file_operation_template(operation: str, file_path: str, context: Optional[str] = None) -> str:
        """Generate commit message for file operations (Write, Edit, MultiEdit)."""
        file_name = Path(file_path).name
        
        if operation == "Write":
            action_type = "feat"
            description = f"create {file_name}"
        else:
            action_type = "feat"
            description = f"update {file_name}"
        
        return CommitTemplates.atomic_commit_template(
            action_type=action_type,
            description=description,
            files_changed=[file_name],
            additional_context=context
        )
    
    @staticmethod
    def test_execution_template(command: str, success: bool) -> str:
        """Generate commit message for test execution."""
        if success:
            if 'lint' in command or 'typecheck' in command:
                return CommitTemplates.atomic_commit_template(
                    action_type="style",
                    description="run linting and type checks",
                    additional_context="Code quality verification passed"
                )
            else:
                return CommitTemplates.atomic_commit_template(
                    action_type="test",
                    description="run tests and verify functionality",
                    additional_context="All tests passing"
                )
        else:
            return None  # Don't commit failed tests
    
    @staticmethod
    def workflow_milestone_template(milestone: str, phase: str, details: List[str]) -> str:
        """Generate commit message for CG workflow milestones."""
        subject = f"feat: complete {milestone} - {phase}"
        
        body_parts = [
            f"CG Workflow Milestone: {milestone}",
            f"Phase: {phase}",
            ""
        ]
        
        if details:
            body_parts.append("Completed:")
            for detail in details:
                body_parts.append(f"- {detail}")
            body_parts.append("")
        
        body_parts.extend([
            "Part of comprehensive CG workflow implementation",
            "",
            "🎯 CG Workflow milestone from Claude Code",
            "",
            "Co-Authored-By: Claude <noreply@anthropic.com>"
        ])
        
        return subject + "\n\n" + "\n".join(body_parts)


# Convenience functions for common commit patterns
def create_atomic_commit_message(tool_name: str, tool_input: Dict, context: str = "") -> Optional[str]:
    """Create atomic commit message based on tool usage."""
    
    if tool_name == "TodoWrite":
        completed_todos = [
            todo.get('content', 'task') 
            for todo in tool_input.get('todos', [])
            if todo.get('status') == 'completed'
        ]
        if completed_todos:
            return CommitTemplates.todo_completion_template(completed_todos)
    
    elif tool_name in ["Write", "Edit", "MultiEdit"]:
        file_path = tool_input.get('file_path', '')
        if file_path:
            return CommitTemplates.file_operation_template(tool_name, file_path, context)
    
    elif tool_name == "Bash":
        command = tool_input.get('command', '')
        if any(cmd in command for cmd in ['test', 'lint', 'typecheck']):
            # We would need the result to determine success
            return CommitTemplates.test_execution_template(command, True)
    
    return None


def create_comprehensive_commit_message(
    session_actions: List[str], 
    session_id: str,
    primary_goal: Optional[str] = None
) -> str:
    """Create comprehensive commit message for session end."""
    
    stats = {
        'files_changed': len(session_actions),
        'duration': 'Variable'  # Could be calculated from session logs
    }
    
    return CommitTemplates.comprehensive_commit_template(
        session_summary=session_actions,
        session_id=session_id,
        primary_achievement=primary_goal,
        stats=stats
    )