---
name: gemini-agent-json-bulk-processor
description: High-volume JSON file processor using Google Gemini Flash for cost-effective customer data extraction from thousands of files
model: gemini
color: green
tools: mcp__nano-agent__prompt_nano_agent
---

# Gemini Agent - JSON Bulk Data Processor

## Purpose

Specialized agent for processing thousands of JSON files and extracting customer data efficiently. Uses Google Gemini Flash for maximum cost-effectiveness on high-volume, repetitive data processing tasks. Ideal for processing 10,000+ files where cost savings of 85-90% over Claude native execution are critical.

## Execute

mcp__nano-agent__prompt_nano_agent(
  agentic_prompt="As a JSON bulk data processing specialist, I need to extract customer data from multiple JSON files efficiently and cost-effectively.

Task: ${PROMPT}

Processing Guidelines:
1. **File Handling**: Process JSON files systematically, handling malformed data gracefully
2. **Data Extraction**: Focus on customer-specific fields (id, name, email, phone, address, purchase_history, etc.)
3. **Output Format**: Provide structured CSV or JSON output for easy import/analysis
4. **Error Handling**: Log files with parsing errors separately for manual review
5. **Performance**: Optimize for batch processing and memory efficiency
6. **Validation**: Ensure data integrity and consistency across all records

Output Requirements:
- Summary of total files processed
- Count of successful vs failed extractions
- Clean, structured data format
- Error log with problematic files
- Processing statistics (time, cost, throughput)

Focus on accuracy, consistency, and cost-effective bulk processing.",
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

This agent uses Gemini Flash which offers exceptional value for bulk processing:
- **Pricing**: ~$0.075 per 1M input tokens, ~$0.30 per 1M output tokens
- **Cost Savings**: 85-90% cheaper than Claude Sonnet for bulk data tasks
- **Best For**: High-volume file processing, repetitive data extraction, batch operations
- **Trade-offs**: Optimized for throughput over complex reasoning, excellent for structured data tasks
- **When to Use**: Any task processing 1000+ files, cost-sensitive projects, production data pipelines

## Processing Capacity

Estimated capacity for JSON file processing:
- **Small files** (1-5KB): 10,000+ files for ~$2-5
- **Medium files** (10-50KB): 5,000+ files for ~$5-15  
- **Large files** (100KB+): 1,000+ files for ~$10-30
- **Compared to Claude**: Same task would cost $150-500 with native execution

## Alternative Models

For different processing requirements:
- **gemini-1.5-flash**: Default - optimal cost/performance for bulk processing
  ```
  model="gemini-1.5-flash", provider="google"
  ```
- **gemini-1.5-pro**: When complex data relationships need analysis
  ```
  model="gemini-1.5-pro", provider="google"
  ```
- **gpt-5-nano**: Alternative cost-effective option with different strengths
  ```
  model="gpt-5-nano", provider="openai"
  ```

## Usage Examples

### Basic Customer Data Extraction
```
@gemini-agent-json-bulk-processor "Process all JSON files in /data/customers/ and extract customer profiles with contact information"
```

### Advanced Processing with Validation
```
@gemini-agent-json-bulk-processor "Process customer JSON files, validate email formats, standardize phone numbers, and output clean CSV for CRM import"
```

### Error-Resilient Batch Processing  
```
@gemini-agent-json-bulk-processor "Process 10,000 JSON files from /data/batch/, skip malformed files, extract core customer data, and provide detailed processing report"
```

## Integration Notes

- **API Key Required**: GOOGLE_API_KEY environment variable
- **Rate Limits**: 1,000 requests per minute (suitable for bulk processing)
- **Context Window**: 1M+ tokens (can process very large JSON files)
- **Memory Efficiency**: Optimized for streaming large datasets
- **Error Recovery**: Built-in handling for malformed JSON and missing fields
- **Output Formats**: Supports CSV, JSON, and structured text output