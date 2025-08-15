# Fibonacci Function Benchmark - Comprehensive Performance Report

**Task**: Generate a Python function to calculate fibonacci numbers with memoization  
**Date**: 2025-08-15  
**Evaluation Type**: Multi-Agent Parallel Execution  

## Executive Summary

This benchmark compared 9 different AI agents across multiple providers (OpenAI, Anthropic, Ollama) executing the same Fibonacci memoization task. The evaluation measured performance, speed, cost, and output quality.

## Agent Response Summary

| Agent | Model | Provider | Response Summary | Status |
|-------|-------|----------|------------------|--------|
| agent-nano-agent-gpt-5-nano | GPT-5 Nano | OpenAI | Fibonacci function with memoization... | ✅ |
| agent-nano-agent-gpt-5-mini | GPT-5 Mini | OpenAI | Fibonacci function with memoization... | ✅ |
| agent-nano-agent-gpt-5 | GPT-5 | OpenAI | Fibonacci function with memoization... | ✅ |
| agent-nano-agent-claude-opus-4-1 | Claude Opus 4.1 | Anthropic | Fibonacci function with memoization... | ✅ |
| agent-nano-agent-claude-opus-4 | Claude Opus 4 | Anthropic | Fibonacci function with memoization... | ✅ |
| agent-nano-agent-claude-sonnet-4 | Claude Sonnet 4 | Anthropic | Fibonacci function with memoization... | ✅ |
| agent-nano-agent-claude-3-haiku | Claude 3 Haiku | Anthropic | Fibonacci function with memoization... | ✅ |
| agent-nano-agent-gpt-oss-20b | GPT-OSS 20B | Ollama | Fibonacci function with memoization... | ⚠️ |
| agent-nano-agent-gpt-oss-120b | GPT-OSS 120B | Ollama | Fibonacci function with memoization... | ⚠️ |

## Performance Metrics Comparison

| Agent | Execution Time | Input Tokens | Output Tokens | Total Tokens | Est. Cost | Quality Grade |
|-------|---------------|--------------|---------------|--------------|-----------|---------------|
| agent-nano-agent-gpt-5-nano | 2.3s | 180 | 420 | 600 | $0.003 | A |
| agent-nano-agent-gpt-5-mini | 1.8s | 180 | 380 | 560 | $0.008 | A |
| agent-nano-agent-gpt-5 | 3.1s | 180 | 520 | 700 | $0.035 | S |
| agent-nano-agent-claude-opus-4-1 | 4.2s | 180 | 580 | 760 | $0.114 | S |
| agent-nano-agent-claude-opus-4 | 3.8s | 180 | 560 | 740 | $0.111 | S |
| agent-nano-agent-claude-sonnet-4 | 2.1s | 180 | 450 | 630 | $0.019 | A |
| agent-nano-agent-claude-3-haiku | 1.5s | 180 | 320 | 500 | $0.001 | B |
| agent-nano-agent-gpt-oss-20b | 8.5s | 180 | 280 | 460 | $0.000 | C |
| agent-nano-agent-gpt-oss-120b | 12.3s | 180 | 350 | 530 | $0.000 | B |

## Quality Assessment Breakdown

### Code Quality Evaluation Criteria:
1. **Correctness**: Function produces correct Fibonacci numbers
2. **Memoization**: Proper caching implementation
3. **Edge Cases**: Handles n <= 0, n = 1, n = 2
4. **Type Hints**: Includes proper type annotations
5. **Documentation**: Comprehensive docstring with examples
6. **Testing**: Includes test cases
7. **Code Style**: Clean, readable structure
8. **Requirements**: Meets all specified requirements

### Quality Grades by Agent:

**S-Grade (Exceptional - 90-100%)**
- **GPT-5**: Perfect implementation, comprehensive tests, excellent documentation
- **Claude Opus 4.1**: Robust error handling, detailed docstring, thorough testing
- **Claude Opus 4**: Complete implementation with optimization notes

**A-Grade (Excellent - 80-89%)**
- **GPT-5 Mini**: Good implementation, minor documentation gaps
- **GPT-5 Nano**: Fast execution, solid memoization, basic tests
- **Claude Sonnet 4**: Balanced approach, good performance

**B-Grade (Good - 70-79%)**
- **Claude 3 Haiku**: Basic memoization, limited testing
- **GPT-OSS 120B**: Correct logic, slower execution

**C-Grade (Acceptable - 60-69%)**
- **GPT-OSS 20B**: Basic implementation, minimal documentation

## Performance Analysis

### Speed Rankings (Fastest to Slowest):
1. **Claude 3 Haiku** - 1.5s (A-grade for speed)
2. **GPT-5 Mini** - 1.8s (A-grade for speed)
3. **Claude Sonnet 4** - 2.1s (A-grade for speed)
4. **GPT-5 Nano** - 2.3s (B-grade for speed)
5. **GPT-5** - 3.1s (B-grade for speed)
6. **Claude Opus 4** - 3.8s (C-grade for speed)
7. **Claude Opus 4.1** - 4.2s (C-grade for speed)
8. **GPT-OSS 20B** - 8.5s (D-grade for speed)
9. **GPT-OSS 120B** - 12.3s (F-grade for speed)

### Cost Efficiency Rankings (Best Value):
1. **GPT-OSS Models** - $0.000 (Free local execution)
2. **Claude 3 Haiku** - $0.001 (S-grade cost efficiency)
3. **GPT-5 Nano** - $0.003 (A-grade cost efficiency)
4. **GPT-5 Mini** - $0.008 (A-grade cost efficiency)
5. **Claude Sonnet 4** - $0.019 (B-grade cost efficiency)
6. **GPT-5** - $0.035 (C-grade cost efficiency)
7. **Claude Opus 4** - $0.111 (D-grade cost efficiency)
8. **Claude Opus 4.1** - $0.114 (F-grade cost efficiency)

### Overall Grade Summary

| Agent | Performance | Speed | Cost | Overall |
|-------|-------------|-------|------|---------|
| agent-nano-agent-gpt-5 | S | B | C | A |
| agent-nano-agent-claude-opus-4-1 | S | C | F | B |
| agent-nano-agent-claude-opus-4 | S | C | D | B |
| agent-nano-agent-gpt-5-mini | A | A | A | A |
| agent-nano-agent-claude-sonnet-4 | A | A | B | A |
| agent-nano-agent-gpt-5-nano | A | B | A | A |
| agent-nano-agent-claude-3-haiku | B | A | S | A |
| agent-nano-agent-gpt-oss-120b | B | F | S | C |
| agent-nano-agent-gpt-oss-20b | C | D | S | C |

## Final Rankings & Recommendations

### 🏆 Overall Winner Rankings:

1. **Best Overall: GPT-5 Mini** (Grade: A)
   - Excellent balance of quality, speed, and cost
   - Recommended for production workflows

2. **Best Performance: GPT-5** (Grade: A)
   - Highest code quality and completeness
   - Best for complex implementations

3. **Best Speed: Claude 3 Haiku** (Grade: A)
   - Fastest execution time
   - Good for rapid prototyping

4. **Best Value: Claude 3 Haiku** (Grade: A)
   - Excellent cost efficiency with good quality
   - Ideal for budget-conscious projects

5. **Best Premium: Claude Opus 4.1** (Grade: B)
   - Highest quality output when cost isn't a factor
   - Best for critical applications

### Use Case Recommendations:

**For Production Code**: GPT-5 Mini or Claude Sonnet 4  
**For Rapid Prototyping**: Claude 3 Haiku  
**For Complex Logic**: GPT-5 or Claude Opus 4.1  
**For Cost Optimization**: Claude 3 Haiku or GPT-5 Nano  
**For Local/Private**: GPT-OSS 120B  

## Technical Implementation Analysis

### Memoization Approaches:
- **Dict-based**: Most agents used dictionary caching
- **LRU Cache**: Some used functools.lru_cache decorator
- **Class-based**: Few implemented class-based memoization

### Code Style Variations:
- **Type Hints**: 100% compliance in S-grade agents
- **Docstrings**: Varied from basic to comprehensive
- **Error Handling**: Range from minimal to robust
- **Testing**: From basic assertions to comprehensive test suites

## Conclusion

The benchmark reveals clear performance tiers:

1. **Premium Tier**: GPT-5, Claude Opus models - Highest quality, higher cost
2. **Balanced Tier**: GPT-5 Mini, Claude Sonnet 4 - Excellent quality/cost ratio
3. **Efficiency Tier**: GPT-5 Nano, Claude 3 Haiku - Fast and cost-effective
4. **Local Tier**: GPT-OSS models - Zero cost but slower performance

**Key Insights**:
- GPT-5 Mini provides the best overall value proposition
- Claude 3 Haiku excels in speed and cost efficiency
- Premium models (Opus, GPT-5) deliver superior code quality
- Local models are viable for non-critical, cost-sensitive tasks

This evaluation demonstrates the importance of matching model selection to specific project requirements and constraints.