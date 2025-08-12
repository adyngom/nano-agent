# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Nano Agent is an experimental MCP (Model Context Protocol) server for autonomous engineering agents with multi-provider LLM support. It's designed to test and compare agentic capabilities across OpenAI (GPT-5), Anthropic (Claude), and local Ollama models in terms of Performance, Speed, and Cost.

## Essential Commands

### Development Setup
```bash
cd apps/nano_agent_mcp_server
uv sync --extra test  # Include test dependencies for development
```

### Running Tests
```bash
# Full test suite (requires API keys)
uv run pytest tests/ -v

# Test specific functionality
uv run pytest tests/nano_agent/modules/test_nano_agent.py::TestExecuteNanoAgent -v

# Quick validation without API calls
uv run nano-cli test-tools
```

### CLI Testing and Development
```bash
cd apps/nano_agent_mcp_server

# Test basic functionality (requires OPENAI_API_KEY)
uv run nano-cli run "What is 2+2?"

# Test different providers
uv run nano-cli run "Hello" --model claude-3-haiku-20240307 --provider anthropic
uv run nano-cli run "List files" --model gpt-oss:20b --provider ollama

# Verbose mode for debugging
uv run nano-cli run "Create a test file" --verbose
```

### Multi-Model Evaluation
```bash
# Run performance benchmarks
/perf:hop_evaluate_nano_agents .claude/commands/perf/lop_eval_1__dummy_test.md
/perf:hop_evaluate_nano_agents .claude/commands/perf/lop_eval_3__file_operations_test.md
```

### MCP Server Usage
The nano-agent can be used through Claude Code or any MCP client:
```prompt
mcp nano-agent: prompt_nano_agent "Create a hello world script" --model gpt-5
@agent-nano-agent-claude-sonnet-4 "Analyze this codebase"
```

## Architecture

### Nested Agent System
The core architecture uses a **nested agent pattern** with three layers:

1. **Outer Agent** (Claude Code) - Communicates via MCP protocol, sees only `prompt_nano_agent` tool
2. **Nano-Agent MCP Server** - Receives prompts and spawns internal OpenAI agents  
3. **Inner Agent** - OpenAI SDK agent with file system tools (read_file, write_file, etc.)

### Multi-Provider Support
All providers use OpenAI-compatible endpoints for consistency:
- **OpenAI**: Direct API (gpt-5, gpt-5-mini, gpt-5-nano)
- **Anthropic**: OpenAI-compatible endpoint at `https://api.anthropic.com/v1/`
- **Ollama**: Local OpenAI-compatible API at `http://localhost:11434/v1`

### HOP/LOP Evaluation Pattern
The evaluation system uses a hierarchical orchestration:
- **HOP (Higher Order Prompt)**: Orchestrates parallel model testing
- **LOP (Lower Order Prompt)**: Defines test cases and grading rubrics
- **Sub-Agents**: 9 pre-configured model combinations for parallel execution

## Key Implementation Details

### Provider Configuration
- Provider selection is handled in `apps/nano_agent_mcp_server/src/nano_agent/modules/provider_config.py`
- Model constants are in `modules/constants.py`
- Default model is `gpt-5-mini` for efficiency

### Tool Implementation
Agent tools are defined in `modules/nano_agent_tools.py`:
- `read_file`: Read file contents
- `write_file`: Create/overwrite files
- `edit_file`: Replace exact text matches
- `list_directory`: Explore directory structure
- `get_file_info`: File metadata

### Token Tracking
Cost and performance tracking is implemented in `modules/token_tracking.py` for all providers.

### Environment Configuration
Required environment variables:
- `OPENAI_API_KEY` - For OpenAI models
- `ANTHROPIC_API_KEY` - For Anthropic models
- `OLLAMA` service running locally for local models

Copy `.env.sample` to `.env` and fill in API keys.

## Claude Code Integration

### Hook System
The project includes enhanced Claude Code hooks for:
- **Session Start**: Auto-planning for coding tasks detected via keywords
- **Post Tool Use**: Auto-spec generation from approved ExitPlanMode plans
- Comprehensive logging and event tracking

### Auto-Planning Workflow
1. Session starts with coding-related prompt → Hook detects task → Suggests `/plan` command
2. Plan mode activated → Present implementation steps → User approves → Auto-generates spec in `specs/`

### Planning Command
Use `/plan {adw_id} "{task_description}"` to create structured specification documents with:
- Metadata, objectives, step-by-step tasks
- Adaptive complexity (simple/medium/complex)
- Validation commands and acceptance criteria

## Testing Philosophy

The project emphasizes **real API testing** over mocking to validate actual model behavior. Tests are organized into:
- **Unit tests**: Individual module functionality
- **Integration tests**: Provider-specific testing in `tests/isolated/`
- **Performance benchmarks**: HOP/LOP evaluation system

## Development Workflow

### UV Dependency Management
- `uv sync` - Main dependencies only
- `uv sync --extra test` - Include test dependencies (required for development)
- `uv sync --all-extras` - All optional dependencies

### Adding New Providers
1. Add provider config to `provider_config.py`
2. Update `constants.py` with new models
3. Add sub-agent configuration in `.claude/agents/`
4. Create test cases in appropriate evaluation files

### Code Structure
All application code is in `apps/nano_agent_mcp_server/`:
- `src/nano_agent/` - Main package
- `src/nano_agent/modules/` - Core functionality modules
- `tests/` - Test suite
- `scripts/` - Installation and utility scripts

The project uses Python 3.12+ with uv for dependency management and includes comprehensive type hints throughout.