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
import random
import subprocess
from pathlib import Path
from datetime import datetime
from utils.constants import ensure_session_log_dir

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def get_completion_messages():
    """Return list of friendly completion messages."""
    return [
        "Work complete!",
        "All done!",
        "Task finished!",
        "Job complete!",
        "Ready for next task!",
    ]


def get_tts_script_path():
    """
    Determine which TTS script to use based on available API keys.
    Priority order: ElevenLabs > OpenAI > pyttsx3
    """
    # Get current script directory and construct utils/tts path
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"

    # Check for ElevenLabs API key (highest priority)
    if os.getenv("ELEVENLABS_API_KEY"):
        elevenlabs_script = tts_dir / "elevenlabs_tts.py"
        if elevenlabs_script.exists():
            return str(elevenlabs_script)

    # Check for OpenAI API key (second priority)
    if os.getenv("OPENAI_API_KEY"):
        openai_script = tts_dir / "openai_tts.py"
        if openai_script.exists():
            return str(openai_script)

    # Fall back to pyttsx3 (no API key required)
    pyttsx3_script = tts_dir / "pyttsx3_tts.py"
    if pyttsx3_script.exists():
        return str(pyttsx3_script)

    return None


def get_llm_completion_message():
    """
    Generate completion message using available LLM services.
    Priority order: OpenAI > Anthropic > fallback to random message

    Returns:
        str: Generated or fallback completion message
    """
    # Get current script directory and construct utils/llm path
    script_dir = Path(__file__).parent
    llm_dir = script_dir / "utils" / "llm"

    # Try OpenAI first (highest priority)
    if os.getenv("OPENAI_API_KEY"):
        oai_script = llm_dir / "oai.py"
        if oai_script.exists():
            try:
                result = subprocess.run(
                    ["uv", "run", str(oai_script), "--completion"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                pass

    # Try Anthropic second
    if os.getenv("ANTHROPIC_API_KEY"):
        anth_script = llm_dir / "anth.py"
        if anth_script.exists():
            try:
                result = subprocess.run(
                    ["uv", "run", str(anth_script), "--completion"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                pass

    # Fallback to random predefined message
    messages = get_completion_messages()
    return random.choice(messages)


def announce_completion():
    """Announce completion using the best available TTS service."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # No TTS scripts available

        # Get completion message (LLM-generated or fallback)
        completion_message = get_llm_completion_message()

        # Call the TTS script with the completion message
        subprocess.run(
            ["uv", "run", tts_script, completion_message],
            capture_output=True,  # Suppress output
            timeout=10,  # 10-second timeout
        )

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        # Fail silently if TTS encounters issues
        pass
    except Exception:
        # Fail silently for any other errors
        pass


def get_session_summary(session_id):
    """Generate a summary of the session for commit message."""
    try:
        log_dir = ensure_session_log_dir(session_id)
        
        # Read session logs to understand what was done
        session_actions = []
        
        # Check post_tool_use log for completed tasks
        post_tool_log = log_dir / "post_tool_use.json"
        if post_tool_log.exists():
            try:
                with open(post_tool_log, "r") as f:
                    post_tool_data = json.load(f)
                    
                for entry in post_tool_data:
                    tool_name = entry.get('tool_name', '')
                    tool_input = entry.get('tool_input', {})
                    
                    if tool_name == 'TodoWrite':
                        completed_todos = [
                            todo.get('content', 'task')
                            for todo in tool_input.get('todos', [])
                            if todo.get('status') == 'completed'
                        ]
                        session_actions.extend(completed_todos)
                    
                    elif tool_name in ['Write', 'Edit', 'MultiEdit']:
                        file_path = tool_input.get('file_path', '')
                        if file_path:
                            file_name = Path(file_path).name
                            action = "created" if tool_name == 'Write' else "updated"
                            session_actions.append(f"{action} {file_name}")
            except Exception:
                pass
        
        # Check for spec files created this session
        specs_dir = Path("specs")
        if specs_dir.exists():
            today = datetime.now().strftime('%Y%m%d')
            for spec_file in specs_dir.glob(f"plan-{today}*.md"):
                session_actions.append(f"created spec {spec_file.name}")
        
        return session_actions[:10]  # Limit to top 10 actions
        
    except Exception:
        return []


def create_comprehensive_commit(session_id):
    """Create a comprehensive commit for the entire session."""
    try:
        # Check if there are changes to commit
        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if status_result.returncode != 0:
            return None
            
        changes = status_result.stdout.strip()
        if not changes:
            return None  # No changes to commit
        
        # Get session summary
        session_actions = get_session_summary(session_id)
        
        # Generate comprehensive commit message
        if session_actions:
            # Use the first action as the main subject
            main_action = session_actions[0]
            commit_subject = f"feat: {main_action}"
            
            # Add details in commit body
            commit_body_parts = [
                "Session Summary:",
                ""
            ]
            
            for i, action in enumerate(session_actions[:5], 1):
                commit_body_parts.append(f"{i}. {action}")
            
            if len(session_actions) > 5:
                commit_body_parts.append(f"   ... and {len(session_actions) - 5} more changes")
            
            commit_body_parts.extend([
                "",
                f"Session ID: {session_id}",
                "",
                "🚀 Comprehensive session commit from Claude Code",
                "",
                "Co-Authored-By: Claude <noreply@anthropic.com>"
            ])
            
            commit_msg = commit_subject + "\n\n" + "\n".join(commit_body_parts)
        else:
            # Fallback message
            commit_msg = f"""feat: comprehensive session update

Session ID: {session_id}

🚀 Comprehensive session commit from Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"""
        
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
                'comprehensive_commit_created': True,
                'commit_message': commit_msg,
                'commit_hash': commit_result.stdout.strip(),
                'session_actions': session_actions
            }
        else:
            return {
                'comprehensive_commit_error': commit_result.stderr.strip()
            }
            
    except Exception as e:
        return {
            'comprehensive_commit_error': str(e)
        }


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--chat", action="store_true", help="Copy transcript to chat.json"
        )
        parser.add_argument(
            "--notify", action="store_true", help="Enable TTS notifications"
        )
        parser.add_argument(
            "--commit", action="store_true", help="Create comprehensive session commit"
        )
        args = parser.parse_args()

        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract required fields
        session_id = input_data.get("session_id", "")
        stop_hook_active = input_data.get("stop_hook_active", False)

        # Create comprehensive commit if requested
        commit_result = None
        if args.commit:
            commit_result = create_comprehensive_commit(session_id)

        # Ensure session log directory exists
        log_dir = ensure_session_log_dir(session_id)
        log_path = log_dir / "stop.json"

        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, "r") as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Add commit result if generated
        if commit_result:
            input_data['comprehensive_commit_result'] = commit_result

        # Append new data
        log_data.append(input_data)

        # Write back to file with formatting
        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=2)

        # Handle --chat switch
        if args.chat and "transcript_path" in input_data:
            transcript_path = input_data["transcript_path"]
            if os.path.exists(transcript_path):
                # Read .jsonl file and convert to JSON array
                chat_data = []
                try:
                    with open(transcript_path, "r") as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    chat_data.append(json.loads(line))
                                except json.JSONDecodeError:
                                    pass  # Skip invalid lines

                    # Write to logs/chat.json
                    chat_file = os.path.join(log_dir, "chat.json")
                    with open(chat_file, "w") as f:
                        json.dump(chat_data, f, indent=2)
                except Exception:
                    pass  # Fail silently

        # Output commit result if applicable
        if commit_result:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "Stop",
                    "comprehensiveCommit": commit_result
                }
            }
            print(json.dumps(output))

        # Announce completion via TTS only if --notify flag is set
        if args.notify:
            announce_completion()

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)


if __name__ == "__main__":
    main()
