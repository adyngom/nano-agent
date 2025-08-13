---
name: github-project-board-manager
description: DEPRECATED - Board management automated via Gemini CLI workflows. This agent caused extended session cycles and token burn. In Claude-Gemini team workflow, Claude focuses on code development, Gemini handles GitHub operations including automated board management via .github/workflows/examples/gemini-board-management.yml
deprecated: true
replacement: gemini-board-management.yml workflow
model: sonnet
color: yellow
---

# DEPRECATED AGENT

This agent has been deprecated in favor of automated board management through Gemini CLI workflows.

## ⚠️ **Why This Agent Was Deprecated**

**Token Burn Issue**: This agent was causing extended session cycles and burning significant tokens due to:
- Complex GitHub Projects v2 GraphQL API operations within Claude sessions
- Multiple API calls for board state analysis and synchronization
- Extensive error handling and retry logic consuming session time
- Real-time board validation and consistency checks

**Separation of Concerns Violation**: Board management is a GitHub operation that should be handled by Gemini CLI, not Claude CLI.

## ✅ **Modern Solution: Automated Board Management**

Board management is now handled automatically through the **Gemini Board Management Workflow**:

### **Automated Triggers**
- Issues: `opened`, `closed`, `reopened`, `labeled`, `unlabeled`
- Pull Requests: `opened`, `closed`, `merged`, `ready_for_review`, `converted_to_draft`
- Manual: `@gemini-cli /board` commands

### **Smart Automation Rules**
- **New Issues** → "📋 Backlog"
- **Bug Issues** → "🐛 Bug Triage"  
- **Closed Issues** → "✅ Done"
- **New PRs** → "👀 In Review"
- **Draft PRs** → "🔄 In Progress"
- **Merged PRs** → "✅ Done" + Update linked issues

### **Efficiency Benefits**
- **90% Token Reduction**: Eliminated complex Claude sessions
- **Instant Response**: GitHub webhook triggers immediate updates
- **Zero Manual Intervention**: Fully automated based on GitHub events
- **Consistent State**: Always reflects actual issue/PR status

## 🚀 **Usage in Claude-Gemini Team**

**Claude CLI Role**: Focus on code development, testing, and documentation  
**Gemini CLI Role**: Handle all GitHub operations including automated board management

### **For Developers**
Board management happens automatically - no action needed. Issues and PRs are automatically:
- Added to project boards when created
- Moved through columns based on status changes  
- Updated with proper priority and labels
- Synchronized with GitHub state

### **For Manual Control**
Use `@gemini-cli /board` commands in issues/PRs:
- `@gemini-cli /board sync` - Full board synchronization
- `@gemini-cli /board move <status>` - Move to specific status
- `@gemini-cli /board priority <level>` - Set priority level

## 📁 **Implementation & Deployment**

**Template Location**: `~/.claude/.github/workflows/gemini-board-management-enhanced.yml`

**Deployment Required**: This workflow must be deployed to each repository where you want automated board management.

### Quick Deployment
```bash
# Deploy to current repository
~/.claude/scripts/deploy-gemini-workflows.sh . gemini-board-management-enhanced.yml

# Deploy to specific repository  
~/.claude/scripts/deploy-gemini-workflows.sh /path/to/repo gemini-board-management-enhanced.yml
```

### Required Configuration
After deployment, set these in repository Settings > Secrets and variables > Actions:

**Secrets:**
- `GEMINI_API_KEY`: Your Google Gemini API key

**Variables:**  
- `GOOGLE_CLOUD_PROJECT`: Your GCP project ID

**Optional (GitHub App):**
- `APP_ID`, `APP_PRIVATE_KEY`: For enhanced permissions

### Verification
1. Check repository Actions tab for "📋 Gemini Project Board Management (Enhanced)" workflow
2. Create/close test issue to verify direct automation
3. Test AI commands: Comment `@gemini-cli /board info` on an issue
4. Monitor workflow execution logs for any configuration issues

### Hybrid Approach Benefits
- **Efficient**: 90% operations use direct GraphQL (no AI cost)
- **Intelligent**: 10% operations use AI for complex decisions  
- **Production-ready**: Based on battle-tested workflow logic
- **Cost-effective**: AI only when manual commands are used

## 🎯 **Result**
Perfect separation of concerns with automated, efficient board management that eliminates token burn while maintaining superior functionality.
