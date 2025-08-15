# Plan: Add Google Gemini Models

## Metadata
adw_id: `20250812_183400`
prompt: `Auto-generated from plan mode approval`
task_type: feature
complexity: medium

## Task Description
Add Google Gemini models support to the nano-agent MCP server to enable access to Google's AI models through OpenAI-compatible endpoints.

## Objective
Integrate Google Gemini models (gemini-2.0-flash, gemini-2.5-flash, gemini-1.5-pro, gemini-1.5-flash) into the nano-agent MCP server using Google's OpenAI-compatible API endpoints, providing users with additional model options for cost optimization and enhanced reasoning capabilities.

## Problem Statement
The nano-agent MCP server currently supports OpenAI, Anthropic, and Ollama providers but lacks access to Google's Gemini models, which offer competitive pricing and advanced reasoning capabilities. Users need access to these models for:
- Cost optimization in CG workflows
- Enhanced reasoning capabilities 
- Model diversity for different use cases
- Integration with existing OpenAI-compatible architecture

## Solution Approach
Leverage Google's OpenAI-compatible API endpoint (https://generativelanguage.googleapis.com/v1beta/openai/) to integrate Gemini models seamlessly into the existing provider architecture without requiring major code changes.

## Relevant Files
Use these files to complete the task:

- `apps/nano_agent_mcp_server/src/nano_agent/modules/constants.py` - Add model definitions
- `apps/nano_agent_mcp_server/src/nano_agent/modules/provider_config.py` - Add provider logic
- `apps/nano_agent_mcp_server/.env` - Add API key configuration
- `apps/nano_agent_mcp_server/tests/test_multi_provider.py` - Add test coverage
- `.claude/agents/artist/*.md` - Optional CG workflow integration

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Implementation

#### Step 1: Update Constants Configuration ⏳ IN PROGRESS
- Add Gemini models to `AVAILABLE_MODELS` dict in constants.py
- Add Gemini model descriptions to `MODEL_INFO` dict
- Add Google API key requirement to `PROVIDER_REQUIREMENTS`

**Models to Add:**
- `gemini-2.0-flash` (Latest flagship model)
- `gemini-2.5-flash` (Enhanced reasoning model)
- `gemini-1.5-pro` (Established professional model)
- `gemini-1.5-flash` (Fast and efficient model)

#### Step 2: Update Provider Configuration
- Add `"google"` provider case in `create_agent()` method in provider_config.py
- Configure OpenAI client with Gemini API base URL
- Use `GOOGLE_API_KEY` environment variable
- Add Google-specific validation in `validate_provider_setup()`

#### Step 3: Environment Configuration
- Add `GOOGLE_API_KEY=` entry to .env file for user configuration

#### Step 4: Add Test Coverage
- Add test cases for Google/Gemini provider in test_multi_provider.py
- Test agent creation with Gemini models
- Validate API key requirements and model availability

#### Step 5: Update CG Workflow Agents (Optional Enhancement)
- Add Gemini model options to existing CG agents
- Configure cost-optimal model selection utilizing Gemini's competitive pricing

### 2. Validation
- Test basic model communication with Gemini API
- Verify tool calling functionality works with Gemini models
- Test integration with existing CG workflow commands
- Validate cost tracking and token counting
- Ensure error handling works properly

## Testing Strategy
- Unit tests for provider configuration
- Integration tests for model communication
- Manual testing for CG workflow integration
- Error handling validation for API key and model availability

## Acceptance Criteria
- Google provider is properly configured in provider_config.py
- All 4 Gemini models are available through the nano-agent MCP server
- Environment configuration supports GOOGLE_API_KEY
- Test coverage includes Google provider validation
- Error handling provides clear messages for configuration issues
- No breaking changes to existing functionality
- CG workflow agents can optionally use Gemini models

## Validation Commands
Execute these commands to validate the task is complete:

- `uv run python -m py_compile apps/nano_agent_mcp_server/src/**/*.py` - Test code compilation
- `pytest apps/nano_agent_mcp_server/tests/test_multi_provider.py -v` - Run provider tests
- Test manual usage: `mcp__nano-agent__prompt_nano_agent(agentic_prompt="Test", model="gemini-2.0-flash", provider="google")`

## Notes
This plan leverages Google's OpenAI-compatible API endpoint, allowing seamless integration with the existing provider architecture. The implementation follows the same pattern as Anthropic and Ollama providers, ensuring consistency and maintainability.

Google Gemini models offer competitive pricing and advanced reasoning capabilities, making them valuable additions to the CG workflow system for cost optimization and enhanced AI capabilities.