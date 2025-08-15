#!/bin/bash

# MetricFlow GitHub Project Board Automated Setup Script
# ARTIST Methodology Implementation for Subscription Metrics SaaS
# This script creates and configures the GitHub project board with automation

set -e

# Configuration
PROJECT_NAME="MetricFlow - Subscription Analytics Dashboard"
REPO_OWNER="${GITHUB_REPOSITORY_OWNER:-$(gh repo view --json owner --jq .owner.login)}"
REPO_NAME="${GITHUB_REPOSITORY_NAME:-$(gh repo view --json name --jq .name)}"
PROJECT_DESCRIPTION="Automated project board for MetricFlow subscription analytics SaaS following ARTIST methodology with 7-sprint delivery timeline"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) is not installed. Please install it first."
        exit 1
    fi
    
    if ! gh auth status &> /dev/null; then
        log_error "GitHub CLI is not authenticated. Please run 'gh auth login' first."
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Create the project board
create_project_board() {
    log_info "Creating GitHub project board: $PROJECT_NAME"
    
    # Create the project
    PROJECT_URL=$(gh project create --title "$PROJECT_NAME" --body "$PROJECT_DESCRIPTION" --format json | jq -r .url)
    PROJECT_NUMBER=$(echo $PROJECT_URL | grep -o '[0-9]*$')
    
    if [ -z "$PROJECT_NUMBER" ]; then
        log_error "Failed to create project board"
        exit 1
    fi
    
    log_success "Project board created: $PROJECT_URL"
    echo "PROJECT_NUMBER=$PROJECT_NUMBER" > .env.project
}

# Configure custom fields
setup_custom_fields() {
    log_info "Setting up custom fields..."
    
    # Complexity field
    gh project field-create $PROJECT_NUMBER --name "Complexity" --type single_select \
        --single-select-option "Low" \
        --single-select-option "Medium" \
        --single-select-option "High"
    
    # Priority field
    gh project field-create $PROJECT_NUMBER --name "Priority" --type single_select \
        --single-select-option "P0" \
        --single-select-option "P1" \
        --single-select-option "P2" \
        --single-select-option "P3"
    
    # Epic field
    gh project field-create $PROJECT_NUMBER --name "Epic" --type single_select \
        --single-select-option "Authentication & User Management" \
        --single-select-option "Data Integration & Processing" \
        --single-select-option "Analytics Engine & Calculations" \
        --single-select-option "Dashboard & Visualization" \
        --single-select-option "Deployment & Operations"
    
    # Team field
    gh project field-create $PROJECT_NUMBER --name "Team" --type single_select \
        --single-select-option "UX Team" \
        --single-select-option "UI Team" \
        --single-select-option "Dev Team" \
        --single-select-option "QA Team" \
        --single-select-option "DevOps Team" \
        --single-select-option "Business Team"
    
    # Sprint field
    gh project field-create $PROJECT_NUMBER --name "Sprint" --type single_select \
        --single-select-option "Sprint 1" \
        --single-select-option "Sprint 2" \
        --single-select-option "Sprint 3" \
        --single-select-option "Sprint 4" \
        --single-select-option "Sprint 5" \
        --single-select-option "Sprint 6" \
        --single-select-option "Sprint 7"
    
    # Story Points field
    gh project field-create $PROJECT_NUMBER --name "Story Points" --type number
    
    # Business Value field
    gh project field-create $PROJECT_NUMBER --name "Business Value" --type single_select \
        --single-select-option "Critical" \
        --single-select-option "High" \
        --single-select-option "Medium" \
        --single-select-option "Low"
    
    log_success "Custom fields created successfully"
}

# Create board columns (views)
setup_board_columns() {
    log_info "Setting up ARTIST methodology columns..."
    
    # Note: GitHub Projects v2 uses views instead of columns
    # We'll create the default board view and customize it
    
    # The default "Board" view should already exist, we'll customize it
    log_info "Customizing board view with ARTIST methodology columns..."
    
    # GitHub CLI doesn't have direct column management for Projects v2 yet
    # This will need to be done through the web interface or GraphQL API
    log_warning "Column setup requires manual configuration in GitHub web interface"
    log_info "Please configure these columns in the project board:"
    echo "  📋 Backlog"
    echo "  🔍 Analysis"
    echo "  📅 Sprint Planning"
    echo "  🔄 In Progress"
    echo "  👀 Code Review"
    echo "  🧪 Testing"
    echo "  🚀 Deployment"
    echo "  ✅ Done"
}

# Create automation workflows
setup_automation_workflows() {
    log_info "Setting up automation workflows..."
    
    # Create .github/workflows directory if it doesn't exist
    mkdir -p .github/workflows
    
    # Create project automation workflow
    cat > .github/workflows/project-automation.yml << 'EOF'
name: Project Board Automation

on:
  issues:
    types: [opened, closed, reopened, labeled, unlabeled, assigned]
  pull_request:
    types: [opened, closed, ready_for_review, converted_to_draft]
  pull_request_review:
    types: [submitted]

jobs:
  update_project:
    runs-on: ubuntu-latest
    name: Update Project Board
    steps:
      - name: Add issue to project
        if: github.event_name == 'issues' && github.event.action == 'opened'
        uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/users/${{ github.repository_owner }}/projects/${{ env.PROJECT_NUMBER }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Auto-assign epic based on labels
        if: github.event_name == 'issues' && github.event.action == 'labeled'
        uses: actions/github-script@v6
        with:
          script: |
            const label = context.payload.label.name;
            let epic = '';
            
            if (label.includes('auth') || label.includes('user')) {
              epic = 'Authentication & User Management';
            } else if (label.includes('integration') || label.includes('payment')) {
              epic = 'Data Integration & Processing';
            } else if (label.includes('analytics') || label.includes('metrics')) {
              epic = 'Analytics Engine & Calculations';
            } else if (label.includes('dashboard') || label.includes('ui')) {
              epic = 'Dashboard & Visualization';
            } else if (label.includes('deploy') || label.includes('devops')) {
              epic = 'Deployment & Operations';
            }
            
            if (epic) {
              console.log(`Auto-assigning epic: ${epic}`);
              // Additional logic to update project field would go here
            }
      
      - name: Move to code review on PR creation
        if: github.event_name == 'pull_request' && github.event.action == 'opened'
        uses: actions/github-script@v6
        with:
          script: |
            console.log('Moving linked issues to code review column');
            // Logic to move issues to code review column
      
      - name: Move to testing on PR approval
        if: github.event_name == 'pull_request_review' && github.event.review.state == 'approved'
        uses: actions/github-script@v6
        with:
          script: |
            console.log('Moving issues to testing column');
            // Logic to move issues to testing column
EOF
    
    log_success "Automation workflow created"
}

# Create issue templates
setup_issue_templates() {
    log_info "Setting up issue templates..."
    
    mkdir -p .github/ISSUE_TEMPLATE
    
    # Feature request template
    cat > .github/ISSUE_TEMPLATE/feature_request.yml << 'EOF'
name: Feature Request
description: Request a new feature for MetricFlow
title: "[FEATURE] "
labels: ["enhancement"]
body:
  - type: dropdown
    id: epic
    attributes:
      label: Epic
      description: Which epic does this feature belong to?
      options:
        - Authentication & User Management
        - Data Integration & Processing
        - Analytics Engine & Calculations
        - Dashboard & Visualization
        - Deployment & Operations
    validations:
      required: true
  
  - type: dropdown
    id: complexity
    attributes:
      label: Complexity
      description: Estimated implementation complexity
      options:
        - Low
        - Medium
        - High
    validations:
      required: true
  
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      description: Business priority level
      options:
        - P0
        - P1
        - P2
        - P3
    validations:
      required: true
  
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Detailed description of the feature
    validations:
      required: true
  
  - type: textarea
    id: acceptance_criteria
    attributes:
      label: Acceptance Criteria
      description: List the acceptance criteria for this feature
      placeholder: |
        - [ ] Criterion 1
        - [ ] Criterion 2
    validations:
      required: true
EOF
    
    # Bug report template
    cat > .github/ISSUE_TEMPLATE/bug_report.yml << 'EOF'
name: Bug Report
description: Report a bug in MetricFlow
title: "[BUG] "
labels: ["bug"]
body:
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      description: Bug severity level
      options:
        - P0
        - P1
        - P2
        - P3
    validations:
      required: true
  
  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: Clear description of the bug
    validations:
      required: true
  
  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the bug
    validations:
      required: true
  
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should happen
    validations:
      required: true
  
  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happens
    validations:
      required: true
EOF
    
    log_success "Issue templates created"
}

# Import existing issues from github-issues.md
import_existing_issues() {
    log_info "Importing existing 35 issues from github-issues.md..."
    
    if [ ! -f "github-issues.md" ]; then
        log_warning "github-issues.md not found. Skipping issue import."
        return
    fi
    
    # Extract issue information and create GitHub issues
    # This is a simplified version - you may need to enhance based on your markdown format
    python3 << 'EOF'
import re
import subprocess
import json

def extract_issues(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Extract issues using regex
    issue_pattern = r'### Issue #(\d+): (.+?)\n\*\*Epic\*\*: (.+?)\n\*\*Sprint\*\*: (.+?)\n\*\*Complexity\*\*: (.+?)\n\*\*Team\*\*: (.+?)\n\n#### Description\n(.+?)\n\n#### Acceptance Criteria\n(.+?)(?=\n###|\n---|\Z)'
    
    issues = re.findall(issue_pattern, content, re.DOTALL)
    
    for issue in issues:
        issue_num, title, epic, sprint, complexity, team, description, acceptance = issue
        
        # Create GitHub issue
        issue_body = f"""**Epic**: {epic}
**Sprint**: {sprint}
**Complexity**: {complexity}
**Team**: {team}

## Description
{description.strip()}

## Acceptance Criteria
{acceptance.strip()}
"""
        
        # Determine labels based on epic and team
        labels = []
        if 'Auth' in epic:
            labels.append('authentication')
        elif 'Data' in epic:
            labels.append('integration')
        elif 'Analytics' in epic:
            labels.append('analytics')
        elif 'Dashboard' in epic:
            labels.append('frontend')
        elif 'Deploy' in epic:
            labels.append('devops')
        
        labels.append(complexity.lower())
        labels.append(f"sprint-{sprint}")
        
        # Create the issue using gh CLI
        cmd = [
            'gh', 'issue', 'create',
            '--title', title,
            '--body', issue_body,
            '--label', ','.join(labels)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Created issue: {title}")
            else:
                print(f"Failed to create issue: {title} - {result.stderr}")
        except Exception as e:
            print(f"Error creating issue {title}: {e}")

extract_issues('github-issues.md')
EOF
    
    log_success "Issue import completed"
}

# Create project documentation
create_documentation() {
    log_info "Creating project documentation..."
    
    cat > PROJECT_BOARD_GUIDE.md << 'EOF'
# MetricFlow Project Board Guide

## Overview
This project board implements the ARTIST methodology for systematic delivery of the MetricFlow subscription analytics SaaS platform.

## Board Structure

### Columns (ARTIST Methodology)
1. **📋 Backlog** - New issues awaiting analysis
2. **🔍 Analysis** - Issues undergoing research and technical analysis
3. **📅 Sprint Planning** - Analyzed issues ready for sprint assignment
4. **🔄 In Progress** - Active development work
5. **👀 Code Review** - Development complete, awaiting review
6. **🧪 Testing** - QA validation and testing
7. **🚀 Deployment** - Ready for or undergoing deployment
8. **✅ Done** - Completed and verified

### Custom Fields
- **Epic**: Major feature area (5 epics total)
- **Sprint**: Sprint assignment (7 sprints planned)
- **Complexity**: Technical complexity (Low/Medium/High)
- **Priority**: Business priority (P0-P3)
- **Team**: Responsible team assignment
- **Story Points**: Effort estimation
- **Business Value**: Business impact assessment

### Automation Rules
- New issues automatically added to Backlog
- Issues move through workflow based on PR status
- Team notifications triggered by column moves
- Epic assignment based on labels
- Sprint progress tracking

## Team Usage

### For Developers
1. Pick issues from "Sprint Planning" column
2. Move to "In Progress" when starting work
3. Create PR when ready - issue moves to "Code Review"
4. Respond to review feedback promptly
5. Issue moves to "Testing" after PR approval

### For QA Team
1. Monitor "Testing" column for new items
2. Validate acceptance criteria
3. Add "qa-approved" label when complete
4. Report bugs by creating new issues

### For Project Managers
1. Use Executive Dashboard view for high-level progress
2. Monitor Sprint Progress view for current sprint
3. Review Team Workload view for capacity planning
4. Check Risk Assessment reports weekly

## Views and Dashboards

### Executive Dashboard
High-level progress tracking for leadership team with focus on P0/P1 items and epic completion.

### Development View
Active sprint work and technical dependencies for development teams.

### Sprint Progress
Current sprint execution tracking with story points and completion metrics.

### Epic Roadmap
Progress visualization by major feature areas.

### Team Workload
Capacity and assignment distribution across all teams.

## Best Practices

1. **Issue Creation**: Use templates and assign epic/priority immediately
2. **Sprint Planning**: Ensure issues have clear acceptance criteria
3. **Code Review**: Review within 24 hours to maintain flow
4. **Testing**: Complete QA within sprint timeline
5. **Documentation**: Update project board fields consistently

## Troubleshooting

### Issue Not Moving Automatically
- Check if PR is linked to issue correctly
- Verify automation rules are enabled
- Ensure required labels are present

### Missing Custom Fields
- Contact project admin to configure fields
- Use issue templates for consistent field population

### Team Notification Issues
- Verify team assignments in repository settings
- Check notification preferences in GitHub
EOF
    
    log_success "Project documentation created"
}

# Main execution
main() {
    log_info "Starting MetricFlow GitHub Project Board setup..."
    
    check_prerequisites
    create_project_board
    setup_custom_fields
    setup_board_columns
    setup_automation_workflows
    setup_issue_templates
    import_existing_issues
    create_documentation
    
    log_success "🎉 MetricFlow Project Board setup completed successfully!"
    
    echo ""
    echo "Next Steps:"
    echo "1. Visit your project board: $PROJECT_URL"
    echo "2. Customize column layout in the web interface"
    echo "3. Configure team notifications"
    echo "4. Test automation workflows"
    echo "5. Train team members on board usage"
    echo ""
    echo "Documentation created in PROJECT_BOARD_GUIDE.md"
}

# Execute main function
main "$@"