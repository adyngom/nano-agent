# Problem #6: Documentation Quality Test
## Instructions
- Test documentation generation capabilities by having agents document a compound interest function
- Compare quality between a specialized documenter agent and a general-purpose line counter agent
- The documenter agent should excel, while the line counter should struggle with this task

## Variables
PROMPT: "Document this Python function with comprehensive developer-friendly documentation:

```python
def calculate_compound_interest(principal, rate, time, n=12):
    return principal * (1 + rate/n)**(n*time)
```

Create documentation that includes:
1. Function description and purpose
2. Parameter descriptions with types and expected ranges
3. Return value description
4. Usage examples with realistic values
5. Mathematical formula explanation
6. Edge cases and error conditions
7. Docstring in proper Python format

Respond with your entire JSON response structure as is."

## Agents
Test with documentation specialist vs general purpose agent:
@claude-agent-api-documenter PROMPT
@claude-agent-line-counter PROMPT

## Expected Output
The api-documenter should produce comprehensive, well-structured documentation while the line-counter should struggle with this complex documentation task.

Expected JSON structure:
```json
{
    "success": true,
    "result": "<comprehensive documentation>",
    "error": null,
    "metadata": {
        "agent": "agent-name",
        "model": "model-name",
        "provider": "provider-name",
        "tokens_used": X,
        "cost_usd": X.XXXX
    },
    "execution_time_seconds": X.XX
}
```

## Grading Rubric

### Accuracy (35%)
- **Excellent (90-100%)**: All documentation elements present and technically correct
- **Good (80-89%)**: Most elements present with minor technical errors
- **Fair (70-79%)**: Basic documentation with some missing or incorrect elements
- **Poor (0-69%)**: Minimal documentation or significant errors

### Completeness (25%)
- **Excellent (90-100%)**: All 7 required elements included comprehensively
- **Good (80-89%)**: 5-6 elements included with good detail
- **Fair (70-79%)**: 3-4 elements included with basic detail
- **Poor (0-69%)**: 1-2 elements or incomplete coverage

### Format and Structure (15%)
- **Excellent (90-100%)**: Perfect Python docstring format, clear organization
- **Good (80-89%)**: Proper format with minor structural issues
- **Fair (70-79%)**: Basic format but some organization problems
- **Poor (0-69%)**: Poor formatting or unclear structure

### Examples and Usability (15%)
- **Excellent (90-100%)**: Multiple realistic examples with clear explanations
- **Good (80-89%)**: Good examples with adequate explanation
- **Fair (70-79%)**: Basic examples with minimal explanation
- **Poor (0-69%)**: No examples or poor example quality

### Technical Depth (10%)
- **Excellent (90-100%)**: Deep mathematical explanation and edge case coverage
- **Good (80-89%)**: Good technical detail with some edge cases
- **Fair (70-79%)**: Basic technical explanation
- **Poor (0-69%)**: Minimal or incorrect technical detail

## Expected Agent Performance

### claude-agent-api-documenter
**Expected Score**: 85-95%
- **Strengths**: Should excel at comprehensive documentation, proper formatting, technical depth
- **Model**: Claude Sonnet 4 (balanced for technical writing)
- **Specialty**: API documentation and technical writing

### claude-agent-line-counter  
**Expected Score**: 40-60%
- **Strengths**: Basic task completion
- **Weaknesses**: Not optimized for documentation, limited technical writing capability
- **Model**: Claude Haiku 3 (optimized for simple counting tasks)
- **Specialty**: File analysis and line counting, not documentation

## Success Metrics
- API documenter should score at least 25 points higher than line counter
- API documenter should include all 7 documentation elements
- Line counter likely to miss technical depth and proper formatting
- Clear demonstration of task-appropriate agent selection importance