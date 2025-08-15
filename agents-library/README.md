# Agent Directory Structure

This directory contains specialized agents organized by domain and function for optimal discoverability and maintenance.

## Structure Overview

```
agents/
├── development/          # Code creation and modification
│   ├── backend/         # Python-specific development
│   ├── frontend/        # UI/design-focused agents  
│   └── fullstack/       # Component libraries & architecture
├── quality/             # Code quality, testing & review
│   ├── testing/         # QA and testing automation
│   ├── security/        # Security analysis & performance
│   ├── architecture/    # Architectural review
│   └── debugging/       # Error analysis & debugging
├── workflow/            # Process automation & version control
│   ├── git/            # Git workflow management
│   └── automation/     # Workflow automation tools
├── integration/         # External tool integrations
│   └── figma/          # Figma-to-code conversion
└── orchestration/       # High-level coordination
```

## Agent Categories

### Development (11 agents)
- **Backend**: Python-specific development and optimization
- **Frontend**: UI components, design tokens, asset management
- **Fullstack**: Component libraries, project structure, theming

### Quality (7 agents)  
- **Testing**: Test creation and strategy (claude-testing-specialist)
- **Security**: Security audits and performance reviews
- **Architecture**: Structural review and SOLID principles
- **Debugging**: Error analysis and troubleshooting

### Workflow (3 agents)
- **Git**: Local git operations for Claude development (claude-git-assistant)
- **Automation**: N8n workflow design and optimization

### ⚠️ Deprecated Agents (3 agents)
- **git-workflow-manager**: Use claude-git-assistant (GitHub ops → Gemini)
- **qa-testing-expert**: Use claude-testing-specialist (GitHub ops → Gemini)
- **github-project-board-manager**: Use .github/workflows/gemini-board-management.yml (Token burn → Gemini automation)

### Integration (4 agents)
- **Figma**: Design-to-code conversion and ShadCN mapping

### Orchestration (2 agents)
- High-level task coordination and context management

## Usage Notes

- Agents can be easily relocated as the project evolves
- Structure supports unlimited nesting levels
- Categories are based on primary function for intuitive discovery
- Cross-cutting concerns may reference multiple categories