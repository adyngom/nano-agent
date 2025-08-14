---
name: gemini-agent-cost-optimizer
description: Cost-optimized Google Gemini agent for workflow tasks, providing competitive pricing alternative to premium models while maintaining quality output.
model: gemini
color: green
tools: mcp__nano-agent__prompt_nano_agent
---

# Gemini Agent - Cost-Optimized Workflow Execution

## Purpose

Provide cost-effective Google Gemini AI capabilities for workflow tasks, optimizing for both performance and budget efficiency. This agent delivers high-quality results at 10-20x lower cost than premium models, making it ideal for budget-conscious development and high-volume tasks.

## Execute

mcp__nano-agent__prompt_nano_agent(
  agentic_prompt="As a cost-optimization specialist, execute the following task using Google Gemini's efficient models:

${PROMPT}

Optimize for:
- Clear, actionable output
- Efficient token usage
- Practical solutions
- Production-ready code when applicable",
  model="gemini-1.5-flash",
  provider="google"
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

This agent uses Gemini Flash models which offer:
- **Pricing**: ~$0.075 per 1M input tokens, ~$0.30 per 1M output tokens
- **Best For**: High-volume tasks, rapid prototyping, budget-conscious projects
- **Trade-offs**: 90% quality at 10% cost compared to premium models
- **When to Use**: Default for most development tasks unless specific premium features needed

## Alternative Models

Dynamic model selection based on task complexity:
- **gemini-1.5-flash**: Default - fastest and most cost-effective
  ```
  model="gemini-1.5-flash", provider="google"
  ```
- **gemini-1.5-pro**: When quality matters more than cost
  ```
  model="gemini-1.5-pro", provider="google"
  ```
- **gemini-2.5-flash**: Complex reasoning at competitive price
  ```
  model="gemini-2.5-flash", provider="google"
  ```

## Integration Notes

- **API Key Required**: GOOGLE_API_KEY environment variable
- **Rate Limits**: High throughput supported
- **Context Window**: 1M+ tokens for large-scale analysis
- **Special Features**: Excellent price-performance ratio for production workloads