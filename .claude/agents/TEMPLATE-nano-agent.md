---
name: [provider]-agent-[name]
description: [Clear description focusing on external model usage and cost optimization]
model: opus|sonnet|gemini|gpt
color: blue|purple|green|orange|red|yellow
tools: mcp__nano-agent__prompt_nano_agent
---

# [Provider] Agent - [Title]

## Purpose

[Clear statement of what this agent does using external models. Emphasize when to use this over Claude native agents.]

## Execute

mcp__nano-agent__prompt_nano_agent(
  agentic_prompt="[Complete prompt template with clear instructions for the external model. Include:
  - Role definition
  - Task breakdown
  - Expected deliverables
  - Format requirements
  
  Use ${PROMPT} for variable substitution where user input goes]",
  model="[specific-model-name]",
  provider="[openai|anthropic|google|ollama]"
)

## Response

IMPORTANT: The nano-agent MCP server returns a JSON structure. You MUST respond with the COMPLETE JSON response EXACTLY as returned, including ALL fields:
- success (boolean)
- result (string with the actual output)
- error (null or error message)
- metadata (object with execution details including token usage and cost)
- execution_time_seconds (number)

Do NOT extract just the 'result' field. Return the ENTIRE JSON structure as your response.

## Cost Optimization Note

This agent uses [Provider] [Model] which offers:
- **Pricing**: [Cost per token or comparison]
- **Best For**: [Specific use cases where this model excels]
- **Trade-offs**: [What you gain/lose vs Claude native]
- **When to Use**: [Clear guidance on when this is the right choice]

## Alternative Models

For different cost/performance trade-offs, consider:
- **[Alternative 1]**: [When and why to use]
  ```
  model="[model-name]", provider="[provider]"
  ```
- **[Alternative 2]**: [When and why to use]
  ```
  model="[model-name]", provider="[provider]"
  ```

## Integration Notes

- **API Key Required**: [Which environment variable needed]
- **Rate Limits**: [Any known limitations]
- **Context Window**: [Size and implications]
- **Special Features**: [Unique capabilities of this model]