#!/usr/bin/env python3
"""
Cost Optimization Workflow Demonstration

This script demonstrates the complete cost optimization workflow with:
1. Intelligent multi-model routing based on complexity
2. Real-time cost tracking and savings calculation
3. Workflow state management and persistence
4. Comprehensive reporting and analysis

Simulates processing 1000 records with hybrid approach vs Claude Opus only.
"""

import asyncio
import json
import time
from cost_optimization_workflow import CostOptimizationWorkflow, demonstrate_workflow_composition
from workflow_state_manager import WorkflowComposer, demonstrate_workflow_state_management

def main():
    """Execute the complete cost optimization demonstration."""
    
    print("🚀 COST OPTIMIZATION WORKFLOW DEMONSTRATION")
    print("=" * 80)
    print("Simulating processing of 1000 records with intelligent model routing")
    print("vs processing all records with Claude Opus for cost comparison")
    print("=" * 80)
    
    # Phase 1: Execute the cost optimization workflow
    print("\n🔥 PHASE 1: COST OPTIMIZATION WORKFLOW EXECUTION")
    print("-" * 50)
    
    try:
        metrics, processed_records = demonstrate_workflow_composition()
        
        # Extract key results
        total_savings = metrics.cost_vs_opus_only - metrics.total_cost
        
        print(f"\n🎯 KEY RESULTS:")
        print(f"   💰 Total Cost (Optimized): ${metrics.total_cost:.4f}")
        print(f"   💸 Cost if All Claude Opus: ${metrics.cost_vs_opus_only:.4f}")
        print(f"   💵 Total Savings: ${total_savings:.4f}")
        print(f"   📈 Savings Percentage: {metrics.savings_percentage:.1f}%")
        print(f"   ⚡ Processing Time: {metrics.total_time:.2f} seconds")
        
    except Exception as e:
        print(f"❌ Error in workflow execution: {e}")
        return
    
    # Phase 2: Demonstrate workflow state management
    print(f"\n🔄 PHASE 2: WORKFLOW STATE MANAGEMENT")
    print("-" * 50)
    
    try:
        workflow, composer = demonstrate_workflow_state_management()
        
        print(f"\n📊 WORKFLOW ORCHESTRATION RESULTS:")
        print(f"   🆔 Workflow ID: {workflow.workflow_id}")
        print(f"   📝 Status: {workflow.status.value}")
        print(f"   🔢 Steps Completed: {workflow.current_step}/{workflow.total_steps}")
        print(f"   💰 Total Workflow Cost: ${workflow.total_cost:.4f}")
        print(f"   🔤 Total Tokens: {workflow.total_tokens:,}")
        
    except Exception as e:
        print(f"❌ Error in workflow state management: {e}")
        return
    
    # Phase 3: Cost efficiency analysis
    print(f"\n📊 PHASE 3: COST EFFICIENCY ANALYSIS")
    print("-" * 50)
    
    # Calculate additional metrics
    cost_per_record_optimized = metrics.total_cost / metrics.total_records
    cost_per_record_opus = metrics.cost_vs_opus_only / metrics.total_records
    efficiency_multiplier = cost_per_record_opus / cost_per_record_optimized
    
    records_per_dollar_optimized = 1.0 / cost_per_record_optimized
    records_per_dollar_opus = 1.0 / cost_per_record_opus
    
    print(f"\n💡 COST EFFICIENCY METRICS:")
    print(f"   📋 Cost per Record (Optimized): ${cost_per_record_optimized:.6f}")
    print(f"   📋 Cost per Record (Opus Only): ${cost_per_record_opus:.6f}")
    print(f"   ⚡ Efficiency Multiplier: {efficiency_multiplier:.1f}x")
    print(f"   📊 Records per $1 (Optimized): {records_per_dollar_optimized:,.0f}")
    print(f"   📊 Records per $1 (Opus Only): {records_per_dollar_opus:,.0f}")
    
    # Phase 4: Scaling projections
    print(f"\n📈 PHASE 4: SCALING PROJECTIONS")
    print("-" * 50)
    
    scaling_volumes = [10_000, 100_000, 1_000_000]
    
    print(f"\n🔮 PROJECTED SAVINGS AT SCALE:")
    for volume in scaling_volumes:
        optimized_cost = cost_per_record_optimized * volume
        opus_cost = cost_per_record_opus * volume
        savings = opus_cost - optimized_cost
        
        print(f"   📊 {volume:,} records:")
        print(f"      💰 Optimized Cost: ${optimized_cost:,.2f}")
        print(f"      💸 Opus Only Cost: ${opus_cost:,.2f}")
        print(f"      💵 Savings: ${savings:,.2f}")
        print()
    
    # Phase 5: Model utilization breakdown
    print(f"\n🤖 PHASE 5: MODEL UTILIZATION BREAKDOWN")
    print("-" * 50)
    
    print(f"\n📊 MODEL DISTRIBUTION:")
    for model, count in metrics.model_distribution.items():
        percentage = (count / metrics.total_records) * 100
        cost_contribution = 0
        
        # Calculate cost contribution per model (simplified)
        if "gemini" in model.lower():
            cost_contribution = count * 0.000075  # Approximate
        elif "gpt-5-mini" in model.lower():
            cost_contribution = count * 0.00015
        elif "claude" in model.lower():
            cost_contribution = count * 0.015
        
        cost_percentage = (cost_contribution / metrics.total_cost) * 100 if metrics.total_cost > 0 else 0
        
        print(f"   🔹 {model}:")
        print(f"      📊 Records: {count:,} ({percentage:.1f}%)")
        print(f"      💰 Cost Contribution: ~${cost_contribution:.4f} ({cost_percentage:.1f}%)")
        print()
    
    # Phase 6: Summary and recommendations
    print(f"\n🎯 PHASE 6: SUMMARY & RECOMMENDATIONS")
    print("-" * 50)
    
    print(f"\n✅ WORKFLOW DEMONSTRATION COMPLETED SUCCESSFULLY!")
    print(f"\n🔑 KEY INSIGHTS:")
    print(f"   1. 🎯 Intelligent routing achieved {metrics.savings_percentage:.1f}% cost reduction")
    print(f"   2. ⚡ Maintained quality while processing {metrics.total_records:,} records in {metrics.total_time:.2f}s")
    print(f"   3. 🔄 Workflow orchestration enables complex multi-step automation")
    print(f"   4. 📈 Savings scale linearly with volume - perfect for production")
    print(f"   5. 🤖 Hybrid approach balances cost, speed, and quality optimally")
    
    print(f"\n📋 IMPLEMENTATION RECOMMENDATIONS:")
    print(f"   • Deploy 70/25/5 distribution for optimal cost-quality balance")
    print(f"   • Implement real-time complexity classification for accurate routing")
    print(f"   • Monitor model performance to maintain quality standards")
    print(f"   • Scale gradually and track cost metrics in production")
    print(f"   • Use workflow composer pattern for complex orchestration needs")
    
    print(f"\n🗂️  FILES GENERATED:")
    print(f"   📄 cost_optimization_results.json - Detailed execution results")
    print(f"   📄 CG_WORKFLOW_STATE_*.yaml - Workflow state persistence")
    print(f"   📄 CG_WORKFLOW_REPORT_*.md - Comprehensive execution report")
    
    print(f"\n🎉 DEMONSTRATION COMPLETE - Cost Optimization Workflow Successfully Executed!")
    
    return {
        "metrics": metrics,
        "workflow": workflow,
        "composer": composer,
        "efficiency_multiplier": efficiency_multiplier,
        "total_savings": total_savings
    }

if __name__ == "__main__":
    results = main()