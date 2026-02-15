# Kiro CLI Quick Start Wizard

## Welcome
🚀 Welcome to the Kiro CLI Quick Start Wizard! This will help you set up your development environment with Kiro CLI by walking you through completing your project's steering documents and understanding all available features.

## Overview
This wizard will help you:
1. **Complete your steering documents** - Fill out the skeleton templates with your project details
2. **Understand your development workflow** - Learn about the available prompts and commands
3. **Explore advanced features** - Discover MCP servers, custom agents, hooks, and more

## Step 1: Complete Steering Documents

You already have skeleton steering documents in `.kiro/steering/`. Let's fill them out with your project details.

### Gather Project Information

**First: Analyze the codebase automatically**

1. Read package.json / pyproject.toml / go.mod / Cargo.toml / composer.json
2. Read README.md if exists
3. Scan directory structure
4. Identify frameworks and tech stack
5. Extract project name from config files

**Then: Ask ONLY for missing information**

Only ask questions if you cannot determine from code analysis:

1. **Project Name**: Ask only if not found in config files or README
2. **Project Description**: Ask only if README doesn't explain it clearly
3. **Target Users**: Ask only if not obvious from README or code
4. **Main Technology**: Skip - you already detected this

**If user doesn't answer or says "figure it out":**
- Use your best inference from code analysis
- Make intelligent assumptions based on what you found
- Proceed with confidence

### Update Steering Documents
After code analysis and any user responses, update the existing steering documents:

**Use this priority for information:**
1. Code analysis (highest priority - what actually exists)
2. User responses (if provided)
3. Intelligent defaults (based on tech stack)

#### Update `.kiro/steering/product.md`:

```markdown
# Product Overview

## Product Purpose
[From README.md or user description, or infer from code structure]

## Target Users
[From README.md or user input, or infer from project type]

## Key Features
[Extract from README.md features section, or infer from code modules]
- [Feature from code analysis]
- [Feature from code analysis]

## Business Objectives
[Infer from project type and structure]

## User Journey
[Create based on code structure and entry points]

## Success Criteria
[Define based on project type]
```

#### Update `.kiro/steering/tech.md`:

```markdown
# Technical Architecture

## Technology Stack
[DETECTED from package.json/pyproject.toml/go.mod/etc.]
- Primary: [Detected language and version]
- Framework: [Detected from dependencies]
- Database: [Detected from dependencies]
- Testing: [Detected from dev dependencies]
- Build tools: [Detected from scripts/config]

## Architecture Overview
[Infer from directory structure - src/, api/, components/, etc.]

## Development Environment
[Extract from package.json scripts, Makefile, etc.]

## Code Standards
[Detect from .eslintrc, .prettierrc, pyproject.toml, etc.]
- Formatting: [Detected formatter]
- Linting: [Detected linter]
- Type checking: [If TypeScript/mypy/etc. detected]

## Testing Strategy
[Detect from test files and dependencies]
- Framework: [Detected test framework]
- Coverage: [If coverage tool detected]

## Deployment Process
[Detect from .github/workflows, Dockerfile, etc.]

## Performance Requirements
[Reasonable defaults for detected tech stack]

## Security Considerations
[Standard practices for detected stack]
```

#### Update `.kiro/steering/structure.md`:

```markdown
# Project Structure

## Directory Layout
[ACTUAL structure from directory scan]
```
[ACTUAL PROJECT NAME]/
├── [actual directories found]
├── [actual directories found]
└── .kiro/
```

## File Naming Conventions
[Detect from actual files - analyze patterns in existing code]
- Components: [Detected pattern from actual files]
- Services: [Detected pattern from actual files]
- Tests: [Detected pattern from actual files]

## Module Organization
[Describe actual organization found in codebase]

## Configuration Files
[List actual config files found]

## Documentation Structure
[List actual docs found]

## Build Artifacts
[Detect from .gitignore and actual directories]

## Environment-Specific Files
[List actual .env files or config found]
```

## Step 2: Development Workflow Overview

Now that your steering documents are complete, let's review your development workflow. You have access to these powerful prompts:

### Core Development Loop
- **`@prime`** - Load project context and understand your codebase
- **`@plan-feature`** - Create comprehensive implementation plans for new features
- **`@execute`** - Execute development plans with systematic task management
- **`@create-prd`** - Generate Product Requirements Documents

### Quality Assurance & Validation
- **`@code-review`** - Perform technical code reviews for quality and bugs
- **`@code-review-fix`** - Fix issues found in code reviews
- **`@execution-report`** - Generate implementation reports for completed work
- **`@system-review`** - Analyze implementation vs plan for process improvements

### Issue Management
- **`@rca`** - Perform root cause analysis for issues
- **`@implement-fix`** - Implement fixes based on RCA documents

### Typical Workflow
1. **Start with `@prime`** to understand your project context
2. **Use `@plan-feature`** to plan new features or changes
3. **Execute with `@execute`** to implement the plan systematically
4. **Review with `@code-review`** to ensure quality
5. **Generate reports** with `@execution-report` for documentation

## Step 3: Advanced Kiro Features

Beyond the core prompts, Kiro CLI offers powerful advanced features to enhance your development workflow:

### 🔧 MCP Servers (Model Context Protocol)
Connect external tools and APIs to extend Kiro's capabilities (AWS docs, git operations, database management, custom integrations).

### 🤖 Custom Agents
Create specialized AI assistants for specific workflows (backend specialist, frontend expert, DevOps agent, security reviewer, API designer).

### ⚡ Hooks (Automation)
Automate workflows and processes at specific lifecycle points (pre-commit hooks, post-deployment hooks, agent spawn hooks, tool execution hooks).

### 📚 Context Management
Optimize how Kiro understands your project (agent resources, session context, knowledge bases, context optimization).

### 🧠 Knowledge Management (Experimental)
Advanced knowledge base features (semantic search, code indexing, documentation integration, pattern learning).

### 🔄 Tangent Mode (Experimental)
Explore side topics without disrupting main conversation (side explorations, what-if scenarios, learning mode, context switching).

### 📋 TODO Lists & Checkpointing (Experimental)
Advanced task and progress management (persistent TODO lists, progress checkpoints, task dependencies, progress visualization).

### 🔀 Subagents
Delegate complex tasks to specialized subagents (parallel processing, specialized expertise, independent context, task delegation).

**Would you like help with any of these advanced features?** For example, I can help you set up MCP servers, create custom agents for specialized workflows, configure automation hooks, or enable experimental features like knowledge management and tangent mode.

## Step 4: Next Steps and Recommendations

Based on your project setup, here are recommended next steps:

### Immediate Actions
1. **Test your setup**: Try `@prime` to load your project context
2. **Plan your first feature**: Use `@plan-feature` for your next development task
3. **Set up your preferred model**: Use `/model` to choose the best AI model for your needs

### Recommended Configurations
Based on your project type and tech stack, suggest specific configurations:
- **For web applications**: Recommend frontend/backend agents and deployment hooks
- **For APIs**: Suggest API design agents and testing automation
- **For data projects**: Recommend database MCP servers and analysis agents
- **For open source**: Suggest GitHub integration and community management tools

## Completion Summary

🎉 **Kiro CLI Quick Start Complete!**

### ✅ What You've Accomplished
- **Steering Documents**: Completed product.md, tech.md, and structure.md with your project details
- **Development Workflow**: Ready to use 11 powerful development prompts
- **Advanced Features**: Aware of MCP servers, custom agents, hooks, and experimental features

### 🚀 **Your Development Arsenal**
**Core Workflow**: @prime → @plan-feature → @execute → @code-review → @execution-report
**Quality Assurance**: @code-review, @code-review-fix, @system-review
**Issue Management**: @rca, @implement-fix
**Documentation**: @create-prd

### 🔧 **Available Advanced Features**
- MCP Servers for external tool integration
- Custom Agents for specialized workflows
- Hooks for workflow automation
- Context Management optimization
- Experimental features (Knowledge, Tangent Mode, TODO Lists, Subagents)

### 💡 **Getting Started**
1. **Right now**: Try `@prime` to understand your project
2. **Next**: Use `@plan-feature` to plan your next development task
3. **Then**: Explore the advanced features that interest you most

### 🆘 **Need Help?**
- Ask about any specific feature: "How do I set up MCP servers?"
- Request workflow guidance: "What's the best way to handle code reviews?"
- Get feature explanations: "Tell me more about custom agents"

**Let me know if you want help with any of these advanced features** - I can guide you through setting up MCP servers, creating custom agents, configuring automation hooks, or enabling experimental features!

**Welcome to supercharged development with Kiro CLI!** 🚀

## Instructions for Assistant

### Critical Requirements
1. **Analyze code FIRST** - Read config files, README, directory structure before asking anything
2. **Ask 0-3 questions maximum** - Only ask what you cannot determine from code
3. **Accept "figure it out" as answer** - Use code analysis and make intelligent inferences
4. **Prioritize detected information** - What exists in code > user input > defaults
5. **Update existing files** - Don't create new steering documents, update the templates
6. **Be confident** - If you can infer it from code, don't ask

### Analysis Checklist
Before asking ANY questions:
- [ ] Read package.json / pyproject.toml / go.mod / Cargo.toml / composer.json
- [ ] Read README.md and extract project description
- [ ] Scan directory structure (ls -la, find key directories)
- [ ] Identify all config files (.eslintrc, tsconfig.json, etc.)
- [ ] Detect testing setup from dependencies
- [ ] Find CI/CD configs (.github/workflows, .gitlab-ci.yml, etc.)
- [ ] Extract project name from configs
- [ ] Infer project purpose from README or code structure

### Quality Checklist
- [ ] Analyzed codebase before asking questions
- [ ] Asked 0-3 questions (only for truly missing info)
- [ ] All three steering documents updated with detected information
- [ ] Used actual code structure, not generic templates
- [ ] Workflow overview provided with specific prompt usage
- [ ] Advanced features mentioned with offer to help
- [ ] User feels confident without being overwhelmed

### Success Metrics
- Steering documents reflect ACTUAL project (not generic templates)
- User didn't need to answer obvious questions
- Tech stack completely detected from code
- Project structure matches reality
- User can immediately start using `@prime` and `@plan-feature`
