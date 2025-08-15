#!/usr/bin/env python3
"""
Agent Orchestrator - Parallel Execution & Comparison

Execute multiple agents in parallel for the same task and provide
comprehensive performance/cost/quality comparison.
"""

import asyncio
import time
import json
from typing import Dict, List, Any, Tuple
from datetime import datetime
import sys
import os
from pathlib import Path

# Add the nano agent module to path
sys.path.insert(0, str(Path(__file__).parent / "apps/nano_agent_mcp_server/src"))

from nano_agent.modules.nano_agent import _execute_nano_agent_async
from nano_agent.modules.data_types import PromptNanoAgentRequest, PromptNanoAgentResponse


class AgentOrchestrator:
    """Orchestrates parallel execution of multiple agents for comparison."""
    
    def __init__(self):
        self.task_prompt = "What is 2+2?"
        self.agent_configs = [
            {
                "name": "claude-sonnet-4", 
                "model": "claude-sonnet-4-20250514", 
                "provider": "anthropic",
                "description": "Claude Sonnet 4 - Balanced performance"
            },
            {
                "name": "gpt-5-mini", 
                "model": "gpt-5-mini", 
                "provider": "openai",
                "description": "GPT-5 Mini - Efficient and fast"
            },
            {
                "name": "gemini-2.0-flash", 
                "model": "gemini-2.0-flash", 
                "provider": "google",
                "description": "Gemini 2.0 Flash - Latest Google model"
            }
        ]
    
    async def execute_agent(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single agent and measure performance."""
        start_time = time.time()
        
        try:
            print(f"🚀 Starting {agent_config['name']}...")
            
            request = PromptNanoAgentRequest(
                agentic_prompt=self.task_prompt,
                model=agent_config["model"],
                provider=agent_config["provider"]
            )
            
            # Execute without rich logging to avoid output interference
            response = await _execute_nano_agent_async(request, enable_rich_logging=False)
            
            execution_time = time.time() - start_time
            
            # Extract key metrics
            result_data = {
                "agent_name": agent_config["name"],
                "model": agent_config["model"],
                "provider": agent_config["provider"],
                "description": agent_config["description"],
                "success": response.success,
                "result": response.result if response.success else None,
                "error": response.error if not response.success else None,
                "execution_time": execution_time,
                "response_length": len(response.result) if response.result else 0,
                "metadata": response.metadata if hasattr(response, 'metadata') else {}
            }
            
            # Extract token usage if available
            if response.metadata and "token_usage" in response.metadata:
                token_usage = response.metadata["token_usage"]
                result_data.update({
                    "total_tokens": token_usage.get("total_tokens", 0),
                    "input_tokens": token_usage.get("input_tokens", 0),
                    "output_tokens": token_usage.get("output_tokens", 0),
                    "total_cost": token_usage.get("total_cost", 0.0)
                })
            else:
                result_data.update({
                    "total_tokens": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "total_cost": 0.0
                })
            
            print(f"✅ {agent_config['name']} completed in {execution_time:.2f}s")
            return result_data
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ {agent_config['name']} failed: {str(e)}")
            
            return {
                "agent_name": agent_config["name"],
                "model": agent_config["model"],
                "provider": agent_config["provider"],
                "description": agent_config["description"],
                "success": False,
                "result": None,
                "error": str(e),
                "execution_time": execution_time,
                "response_length": 0,
                "total_tokens": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_cost": 0.0,
                "metadata": {"error_type": type(e).__name__}
            }
    
    async def execute_all_parallel(self) -> List[Dict[str, Any]]:
        """Execute all agents in parallel and collect results."""
        print(f"🎯 Task: '{self.task_prompt}'")
        print(f"🔄 Executing {len(self.agent_configs)} agents in parallel...")
        print("-" * 60)
        
        # Create tasks for parallel execution
        tasks = [
            self.execute_agent(config) 
            for config in self.agent_configs
        ]
        
        # Execute all tasks in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions that occurred
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Convert exception to error result
                config = self.agent_configs[i]
                processed_results.append({
                    "agent_name": config["name"],
                    "model": config["model"],
                    "provider": config["provider"],
                    "description": config["description"],
                    "success": False,
                    "result": None,
                    "error": str(result),
                    "execution_time": 0.0,
                    "response_length": 0,
                    "total_tokens": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "total_cost": 0.0,
                    "metadata": {"error_type": type(result).__name__}
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    def grade_performance(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Grade agent performance on multiple dimensions."""
        if not results:
            return results
        
        successful_results = [r for r in results if r["success"]]
        
        if not successful_results:
            # If no successful results, assign F grades to all
            for result in results:
                result.update({
                    "performance_grade": "F",
                    "speed_grade": "F",
                    "cost_grade": "F",
                    "overall_grade": "F"
                })
            return results
        
        # Performance grading (based on task completion and correctness)
        for result in results:
            if not result["success"]:
                result["performance_grade"] = "F"
            else:
                # For the simple math task "What is 2+2?", check if answer contains "4"
                response_text = result["result"].lower() if result["result"] else ""
                if "4" in response_text or "four" in response_text:
                    result["performance_grade"] = "S"  # Perfect answer
                else:
                    result["performance_grade"] = "C"  # Responded but incorrect
        
        # Speed grading (relative to other successful agents)
        if successful_results:
            execution_times = [r["execution_time"] for r in successful_results]
            min_time = min(execution_times)
            max_time = max(execution_times)
            time_range = max_time - min_time if max_time > min_time else 1
            
            for result in results:
                if not result["success"]:
                    result["speed_grade"] = "F"
                else:
                    # Relative speed scoring
                    relative_time = (result["execution_time"] - min_time) / time_range if time_range > 0 else 0
                    if relative_time <= 0.2:
                        result["speed_grade"] = "S"
                    elif relative_time <= 0.4:
                        result["speed_grade"] = "A"
                    elif relative_time <= 0.6:
                        result["speed_grade"] = "B"
                    elif relative_time <= 0.8:
                        result["speed_grade"] = "C"
                    else:
                        result["speed_grade"] = "D"
        
        # Cost grading (relative to other successful agents)
        if successful_results:
            costs = [r["total_cost"] for r in successful_results if r["total_cost"] > 0]
            if costs:
                min_cost = min(costs)
                max_cost = max(costs)
                cost_range = max_cost - min_cost if max_cost > min_cost else 0.0001
                
                for result in results:
                    if not result["success"] or result["total_cost"] == 0:
                        result["cost_grade"] = "F" if not result["success"] else "S"  # Free is best
                    else:
                        # Relative cost scoring (lower is better)
                        relative_cost = (result["total_cost"] - min_cost) / cost_range
                        if relative_cost <= 0.2:
                            result["cost_grade"] = "S"
                        elif relative_cost <= 0.4:
                            result["cost_grade"] = "A"
                        elif relative_cost <= 0.6:
                            result["cost_grade"] = "B"
                        elif relative_cost <= 0.8:
                            result["cost_grade"] = "C"
                        else:
                            result["cost_grade"] = "D"
            else:
                # No cost data available
                for result in results:
                    result["cost_grade"] = "S" if result["success"] else "F"
        
        # Overall grade (weighted: 40% performance, 30% speed, 30% cost)
        grade_values = {"S": 5, "A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
        grade_names = {5: "S", 4: "A", 3: "B", 2: "C", 1: "D", 0: "F"}
        
        for result in results:
            perf_val = grade_values[result["performance_grade"]]
            speed_val = grade_values[result["speed_grade"]]
            cost_val = grade_values[result["cost_grade"]]
            
            overall_val = round(0.4 * perf_val + 0.3 * speed_val + 0.3 * cost_val)
            result["overall_grade"] = grade_names[overall_val]
        
        return results
    
    def generate_report(self, results: List[Dict[str, Any]]) -> str:
        """Generate comprehensive comparison report."""
        report_lines = [
            "# Agent Orchestrator - Parallel Execution Report",
            f"\n**Task**: {self.task_prompt}",
            f"**Timestamp**: {datetime.now().isoformat()}",
            f"**Agents Tested**: {len(results)}",
            "\n## Agent Response Table\n"
        ]
        
        # Agent Response Table
        report_lines.append("| Agent | Model | Response Summary | Status |")
        report_lines.append("|-------|-------|------------------|--------|")
        
        for result in results:
            summary = ""
            if result["result"]:
                summary = result["result"][:100].replace("\n", " ").replace("|", "\\|")
                if len(result["result"]) > 100:
                    summary += "..."
            
            status = "✅" if result["success"] else "❌"
            report_lines.append(
                f"| {result['agent_name']} | {result['model']} | {summary} | {status} |"
            )
        
        # Performance Comparison Table
        report_lines.extend([
            "\n## Performance Comparison\n",
            "| Agent | Execution Time | Tokens | Cost | Quality Grade |",
            "|-------|---------------|--------|------|---------------|"
        ])
        
        for result in results:
            tokens = f"{result['total_tokens']}" if result['total_tokens'] > 0 else "N/A"
            cost = f"${result['total_cost']:.4f}" if result['total_cost'] > 0 else "Free"
            
            report_lines.append(
                f"| {result['agent_name']} | {result['execution_time']:.2f}s | "
                f"{tokens} | {cost} | {result['performance_grade']} |"
            )
        
        # Grading Summary
        report_lines.extend([
            "\n## Grading Summary\n",
            "| Agent | Performance | Speed | Cost | Overall |",
            "|-------|-------------|-------|------|---------|"
        ])
        
        for result in results:
            report_lines.append(
                f"| {result['agent_name']} | {result['performance_grade']} | "
                f"{result['speed_grade']} | {result['cost_grade']} | {result['overall_grade']} |"
            )
        
        # Final Ranking
        successful_results = [r for r in results if r["success"]]
        if successful_results:
            # Sort by overall grade (S=5, A=4, etc.) then by execution time
            grade_values = {"S": 5, "A": 4, "B": 3, "C": 2, "D": 1, "F": 0}
            ranked_results = sorted(
                successful_results,
                key=lambda x: (grade_values[x["overall_grade"]], -x["execution_time"]),
                reverse=True
            )
            
            report_lines.extend([
                "\n## Final Ranking\n"
            ])
            
            for i, result in enumerate(ranked_results[:3], 1):
                if i == 1:
                    title = "🥇 **Best Overall**"
                elif i == 2:
                    title = "🥈 **Runner Up**"
                else:
                    title = "🥉 **Third Place**"
                
                report_lines.append(
                    f"{i}. {title}: {result['agent_name']} (Grade: {result['overall_grade']}, "
                    f"{result['execution_time']:.2f}s, ${result['total_cost']:.4f})"
                )
        
        # Detailed Results (JSON format)
        report_lines.extend([
            "\n## Detailed Results (JSON)\n",
            "```json",
            json.dumps(results, indent=2, default=str),
            "```"
        ])
        
        return "\n".join(report_lines)
    
    async def run_orchestration(self) -> str:
        """Run the complete orchestration and return the report."""
        print("🎭 Claude Agent Orchestrator - Parallel Execution & Comparison")
        print("=" * 70)
        
        # Execute all agents in parallel
        results = await self.execute_all_parallel()
        
        print("\n📊 Grading performance...")
        
        # Grade the results
        graded_results = self.grade_performance(results)
        
        # Generate comprehensive report
        report = self.generate_report(graded_results)
        
        print("\n🎯 Orchestration complete!")
        return report


async def main():
    """Main entry point for the orchestrator."""
    orchestrator = AgentOrchestrator()
    
    try:
        report = await orchestrator.run_orchestration()
        
        # Save report to file
        report_path = Path("agent_orchestration_report.md")
        with open(report_path, "w") as f:
            f.write(report)
        
        print(f"\n📄 Report saved to: {report_path.absolute()}")
        print("\n" + "="*70)
        print("EXECUTIVE SUMMARY")
        print("="*70)
        print(report)
        
    except Exception as e:
        print(f"❌ Orchestration failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())