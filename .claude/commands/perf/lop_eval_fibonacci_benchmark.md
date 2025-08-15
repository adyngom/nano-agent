# Fibonacci Function Benchmark - Comprehensive Agent Comparison

## Instructions

- Pass the prompt into each nano-agent AS IS. Do not change the prompt in any way.
- Each agent will implement the same task to allow for direct performance comparison.
- Measure execution time, token usage, cost, and output quality.

## Variables

PROMPT: "Generate a Python function to calculate fibonacci numbers with memoization. Requirements:
1. Function name should be 'fibonacci_memo'
2. Use a dictionary or cache to store previously calculated values
3. Handle edge cases (n <= 0, n = 1, n = 2)
4. Include proper type hints
5. Add docstring with examples
6. Write the function to a file called 'fibonacci_MODEL_NAME.py' (replace MODEL_NAME with your actual model name)
7. Include basic test cases that verify the function works correctly
8. Respond with your entire JSON response structure as is."

## Agents

IMPORTANT: You're calling the respective claude code sub agents - do not call the `mcp__nano-agent__prompt_nano_agent` tool directly, let the sub agent's handle that.

@agent-nano-agent-gpt-5-nano PROMPT
@agent-nano-agent-gpt-5-mini PROMPT
@agent-nano-agent-gpt-5 PROMPT
@agent-nano-agent-claude-opus-4-1 PROMPT
@agent-nano-agent-claude-opus-4 PROMPT
@agent-nano-agent-claude-sonnet-4 PROMPT
@agent-nano-agent-claude-3-haiku PROMPT
@agent-nano-agent-gpt-oss-20b PROMPT
@agent-nano-agent-gpt-oss-120b PROMPT

## Expected Output

Each agent should create a Python file with a complete fibonacci function implementation including:
- Proper memoization implementation
- Type hints
- Comprehensive docstring
- Edge case handling
- Test cases

IMPORTANT: All agents must respond with this JSON structure. Don't change the structure or add any additional fields. Output it as the given structure as raw JSON for each agent with no preamble.

```json
{
    "success": true,
    "result": "<summary of implementation and file creation>",
    "error": null,
    "metadata": {
        ...keep all fields given
    },
    "execution_time_seconds": X.XX
}
```

## Grading Rubric

### Performance Grade (S-F)
- **S**: Perfect implementation with all requirements, efficient memoization, comprehensive tests
- **A**: Minor issues, 90%+ requirements met, good memoization implementation
- **B**: Good implementation, 80%+ requirements, basic memoization
- **C**: Acceptable implementation, 70%+ requirements, some memoization
- **D**: Poor implementation, 60%+ requirements, minimal memoization
- **F**: Failed or <60% requirements, incorrect/missing memoization

### Quality Assessment Criteria:
1. **Correctness**: Does the function produce correct Fibonacci numbers?
2. **Memoization**: Is memoization properly implemented and effective?
3. **Edge Cases**: Are edge cases (n <= 0, n = 1, n = 2) handled correctly?
4. **Type Hints**: Are proper type hints included?
5. **Documentation**: Is there a comprehensive docstring with examples?
6. **Testing**: Are test cases included and do they verify correctness?
7. **Code Style**: Is the code clean, readable, and well-structured?
8. **File Creation**: Was the file created with the correct naming convention?

### Speed Comparison:
- Measure execution time from prompt to completion
- Compare relative performance across models

### Cost Analysis:
- Token usage (input/output)
- Estimated API costs per provider
- Cost per quality unit

### Expected Benchmark Results:
The evaluation should produce a comprehensive comparison table showing:
- Model performance rankings
- Speed analysis (fastest to slowest)
- Cost efficiency rankings
- Quality grades for each implementation
- Overall recommendations for different use cases