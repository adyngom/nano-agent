#!/usr/bin/env python3
"""
Workflow State Manager - Meta-Agent Orchestration

This module implements the workflow composer pattern for managing complex
multi-step workflows with state persistence, error recovery, and conditional routing.
"""

import json
import time
import yaml
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

class AgentType(Enum):
    NANO_AGENT_GEMINI = "nano-agent-gemini"
    NANO_AGENT_GPT5_MINI = "nano-agent-gpt5-mini"
    NANO_AGENT_CLAUDE_OPUS = "nano-agent-claude-opus"
    NANO_AGENT_FACTORY = "nano-agent-factory"

@dataclass
class WorkflowStep:
    step_id: str
    agent_type: AgentType
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    status: WorkflowStatus = WorkflowStatus.PENDING
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    cost: float = 0.0
    tokens_used: int = 0
    error_message: Optional[str] = None

@dataclass
class WorkflowState:
    workflow_id: str
    workflow_name: str
    status: WorkflowStatus
    current_step: int
    total_steps: int
    steps: List[WorkflowStep]
    context: Dict[str, Any]
    artifacts: List[str]
    total_cost: float = 0.0
    total_tokens: int = 0
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    
class WorkflowComposer:
    """
    Implements the nano-agent workflow composer pattern for complex orchestration.
    Manages state, routing, error recovery, and cost optimization.
    """
    
    def __init__(self, workflow_dir: str = "/Users/zero2hero/Code/Liveprojects/nano-agent"):
        self.workflow_dir = Path(workflow_dir)
        self.current_workflows: Dict[str, WorkflowState] = {}
        
    def create_cost_optimization_workflow(self, workflow_id: str) -> WorkflowState:
        """Create the cost optimization workflow definition."""
        
        steps = [
            WorkflowStep(
                step_id="record_generation",
                agent_type=AgentType.NANO_AGENT_FACTORY,
                input_data={"task": "generate_test_records", "count": 1000}
            ),
            WorkflowStep(
                step_id="complexity_analysis",
                agent_type=AgentType.NANO_AGENT_GPT5_MINI,
                input_data={"task": "analyze_record_complexity", "batch_size": 100}
            ),
            WorkflowStep(
                step_id="simple_processing",
                agent_type=AgentType.NANO_AGENT_GEMINI,
                input_data={"task": "process_simple_records", "expected_count": 700}
            ),
            WorkflowStep(
                step_id="medium_processing", 
                agent_type=AgentType.NANO_AGENT_GPT5_MINI,
                input_data={"task": "process_medium_records", "expected_count": 250}
            ),
            WorkflowStep(
                step_id="complex_processing",
                agent_type=AgentType.NANO_AGENT_CLAUDE_OPUS,
                input_data={"task": "process_complex_records", "expected_count": 50}
            ),
            WorkflowStep(
                step_id="cost_analysis",
                agent_type=AgentType.NANO_AGENT_GPT5_MINI,
                input_data={"task": "calculate_cost_savings", "baseline": "claude_opus_only"}
            )
        ]
        
        workflow = WorkflowState(
            workflow_id=workflow_id,
            workflow_name="Cost Optimization Multi-Model Routing",
            status=WorkflowStatus.PENDING,
            current_step=0,
            total_steps=len(steps),
            steps=steps,
            context={
                "target_records": 1000,
                "distribution": {"simple": 0.70, "medium": 0.25, "complex": 0.05},
                "max_concurrent": 50,
                "cost_baseline": "claude_opus_only"
            },
            artifacts=[],
            start_time=time.time()
        )
        
        self.current_workflows[workflow_id] = workflow
        return workflow
    
    def save_workflow_state(self, workflow: WorkflowState) -> str:
        """Save workflow state to file for persistence."""
        
        state_file = self.workflow_dir / f"CG_WORKFLOW_STATE_{workflow.workflow_id}.yaml"
        
        # Convert to serializable format
        workflow_dict = {
            "workflow_metadata": {
                "workflow_id": workflow.workflow_id,
                "workflow_name": workflow.workflow_name,
                "status": workflow.status.value,
                "current_step": workflow.current_step,
                "total_steps": workflow.total_steps,
                "start_time": workflow.start_time,
                "end_time": workflow.end_time,
                "total_cost": workflow.total_cost,
                "total_tokens": workflow.total_tokens
            },
            "context": workflow.context,
            "artifacts": workflow.artifacts,
            "steps": []
        }
        
        # Add step details
        for step in workflow.steps:
            step_dict = {
                "step_id": step.step_id,
                "agent_type": step.agent_type.value,
                "status": step.status.value,
                "input_data": step.input_data,
                "output_data": step.output_data,
                "start_time": step.start_time,
                "end_time": step.end_time,
                "cost": step.cost,
                "tokens_used": step.tokens_used,
                "error_message": step.error_message
            }
            workflow_dict["steps"].append(step_dict)
        
        # Save as YAML for readability
        with open(state_file, 'w') as f:
            yaml.dump(workflow_dict, f, indent=2, default_flow_style=False)
        
        logger.info(f"Workflow state saved to: {state_file}")
        return str(state_file)
    
    def load_workflow_state(self, workflow_id: str) -> Optional[WorkflowState]:
        """Load workflow state from file."""
        
        state_file = self.workflow_dir / f"CG_WORKFLOW_STATE_{workflow_id}.yaml"
        
        if not state_file.exists():
            logger.warning(f"Workflow state file not found: {state_file}")
            return None
        
        with open(state_file, 'r') as f:
            workflow_dict = yaml.safe_load(f)
        
        # Reconstruct workflow state
        metadata = workflow_dict["workflow_metadata"]
        
        steps = []
        for step_dict in workflow_dict["steps"]:
            step = WorkflowStep(
                step_id=step_dict["step_id"],
                agent_type=AgentType(step_dict["agent_type"]),
                input_data=step_dict["input_data"],
                output_data=step_dict.get("output_data"),
                status=WorkflowStatus(step_dict["status"]),
                start_time=step_dict.get("start_time"),
                end_time=step_dict.get("end_time"),
                cost=step_dict.get("cost", 0.0),
                tokens_used=step_dict.get("tokens_used", 0),
                error_message=step_dict.get("error_message")
            )
            steps.append(step)
        
        workflow = WorkflowState(
            workflow_id=metadata["workflow_id"],
            workflow_name=metadata["workflow_name"],
            status=WorkflowStatus(metadata["status"]),
            current_step=metadata["current_step"],
            total_steps=metadata["total_steps"],
            steps=steps,
            context=workflow_dict["context"],
            artifacts=workflow_dict["artifacts"],
            total_cost=metadata.get("total_cost", 0.0),
            total_tokens=metadata.get("total_tokens", 0),
            start_time=metadata.get("start_time"),
            end_time=metadata.get("end_time")
        )
        
        self.current_workflows[workflow_id] = workflow
        return workflow
    
    def execute_step(self, workflow_id: str, step_index: int) -> bool:
        """Execute a single workflow step with error handling."""
        
        workflow = self.current_workflows.get(workflow_id)
        if not workflow:
            logger.error(f"Workflow {workflow_id} not found")
            return False
        
        if step_index >= len(workflow.steps):
            logger.error(f"Step index {step_index} out of range")
            return False
        
        step = workflow.steps[step_index]
        step.status = WorkflowStatus.RUNNING
        step.start_time = time.time()
        
        try:
            logger.info(f"Executing step: {step.step_id} with {step.agent_type.value}")
            
            # Simulate step execution based on agent type
            result = self.simulate_agent_execution(step)
            
            step.output_data = result
            step.status = WorkflowStatus.COMPLETED
            step.end_time = time.time()
            
            # Update workflow progress
            workflow.current_step = step_index + 1
            workflow.total_cost += step.cost
            workflow.total_tokens += step.tokens_used
            
            # Save state after each step
            self.save_workflow_state(workflow)
            
            logger.info(f"Step {step.step_id} completed successfully")
            return True
            
        except Exception as e:
            step.status = WorkflowStatus.FAILED
            step.error_message = str(e)
            step.end_time = time.time()
            
            logger.error(f"Step {step.step_id} failed: {e}")
            return False
    
    def simulate_agent_execution(self, step: WorkflowStep) -> Dict[str, Any]:
        """Simulate agent execution with realistic costs and timing."""
        
        # Simulate different processing characteristics per agent type
        if step.agent_type == AgentType.NANO_AGENT_GEMINI:
            step.cost = 0.01  # Low cost for simple processing
            step.tokens_used = 500
            return {
                "processed_records": step.input_data.get("expected_count", 100),
                "avg_processing_time": 0.2,
                "success_rate": 0.98
            }
            
        elif step.agent_type == AgentType.NANO_AGENT_GPT5_MINI:
            step.cost = 0.05  # Medium cost for balanced processing
            step.tokens_used = 1500
            return {
                "processed_records": step.input_data.get("expected_count", 100),
                "avg_processing_time": 0.5,
                "success_rate": 0.99
            }
            
        elif step.agent_type == AgentType.NANO_AGENT_CLAUDE_OPUS:
            step.cost = 0.25  # High cost for complex processing
            step.tokens_used = 3000
            return {
                "processed_records": step.input_data.get("expected_count", 50),
                "avg_processing_time": 1.2,
                "success_rate": 0.995
            }
            
        else:  # NANO_AGENT_FACTORY
            step.cost = 0.02  # Factory overhead
            step.tokens_used = 800
            return {
                "agent_created": "gemini-1.5-flash-agent",
                "configuration": step.input_data,
                "ready": True
            }
    
    def execute_workflow(self, workflow_id: str) -> bool:
        """Execute complete workflow with error recovery."""
        
        workflow = self.current_workflows.get(workflow_id)
        if not workflow:
            logger.error(f"Workflow {workflow_id} not found")
            return False
        
        workflow.status = WorkflowStatus.RUNNING
        
        for i in range(workflow.current_step, len(workflow.steps)):
            success = self.execute_step(workflow_id, i)
            
            if not success:
                workflow.status = WorkflowStatus.FAILED
                self.save_workflow_state(workflow)
                return False
        
        workflow.status = WorkflowStatus.COMPLETED
        workflow.end_time = time.time()
        self.save_workflow_state(workflow)
        
        logger.info(f"Workflow {workflow_id} completed successfully")
        return True
    
    def generate_execution_report(self, workflow_id: str) -> str:
        """Generate comprehensive workflow execution report."""
        
        workflow = self.current_workflows.get(workflow_id)
        if not workflow:
            return f"Workflow {workflow_id} not found"
        
        duration = (workflow.end_time or time.time()) - (workflow.start_time or 0)
        
        report = f"""# Workflow Execution Report

## Workflow: {workflow.workflow_name}
**ID**: {workflow.workflow_id}
**Status**: {workflow.status.value.upper()}
**Started**: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(workflow.start_time))}
**Duration**: {duration:.2f} seconds
**Total Cost**: ${workflow.total_cost:.4f}
**Total Tokens**: {workflow.total_tokens:,}

## Steps Executed
"""
        
        for i, step in enumerate(workflow.steps):
            status_emoji = {
                WorkflowStatus.COMPLETED: "✅",
                WorkflowStatus.FAILED: "❌", 
                WorkflowStatus.RUNNING: "🔄",
                WorkflowStatus.PENDING: "⏸️"
            }.get(step.status, "❓")
            
            step_duration = (step.end_time or 0) - (step.start_time or 0) if step.start_time else 0
            
            report += f"{i+1}. {status_emoji} **{step.step_id}** ({step.agent_type.value})\n"
            report += f"   - Duration: {step_duration:.2f}s | Cost: ${step.cost:.4f} | Tokens: {step.tokens_used:,}\n"
            
            if step.error_message:
                report += f"   - ❌ Error: {step.error_message}\n"
            
            if step.output_data:
                report += f"   - 📊 Output: {json.dumps(step.output_data, indent=4)}\n"
            
            report += "\n"
        
        report += f"""## Artifacts Created
{chr(10).join(f"- {artifact}" for artifact in workflow.artifacts)}

## Performance Metrics
- **Average Step Cost**: ${workflow.total_cost/len(workflow.steps):.4f}
- **Cost per Token**: ${workflow.total_cost/workflow.total_tokens:.6f}
- **Steps per Second**: {len(workflow.steps)/duration:.2f}

## Next Steps
"""
        
        if workflow.status == WorkflowStatus.COMPLETED:
            report += "- Workflow completed successfully\n- Review cost optimization results\n- Consider scaling to production"
        elif workflow.status == WorkflowStatus.FAILED:
            report += "- Investigate failed step\n- Implement error recovery\n- Retry from checkpoint"
        else:
            report += "- Continue execution from current step\n- Monitor resource usage\n- Adjust concurrency if needed"
            
        return report

def demonstrate_workflow_state_management():
    """Demonstrate the workflow composer with state management."""
    
    print("🔄 Workflow State Manager - Meta-Agent Orchestration")
    print("=" * 60)
    
    # Initialize composer
    composer = WorkflowComposer()
    
    # Create cost optimization workflow
    workflow_id = f"cost_opt_{int(time.time())}"
    workflow = composer.create_cost_optimization_workflow(workflow_id)
    
    print(f"\n📋 Created workflow: {workflow.workflow_name}")
    print(f"ID: {workflow_id}")
    print(f"Steps: {workflow.total_steps}")
    
    # Save initial state
    state_file = composer.save_workflow_state(workflow)
    print(f"📁 Initial state saved to: {state_file}")
    
    # Execute workflow
    print(f"\n⚡ Executing workflow...")
    success = composer.execute_workflow(workflow_id)
    
    if success:
        print("✅ Workflow completed successfully!")
    else:
        print("❌ Workflow failed")
    
    # Generate report
    report = composer.generate_execution_report(workflow_id)
    print("\n📊 Execution Report:")
    print(report)
    
    # Save final report
    report_file = composer.workflow_dir / f"CG_WORKFLOW_REPORT_{workflow_id}.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n📄 Full report saved to: {report_file}")
    
    return workflow, composer

if __name__ == "__main__":
    demonstrate_workflow_state_management()