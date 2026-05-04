---
name: context-intelligence
description: Manage contextual memory and skills with Qdrant vector database. Use when you need to store memories about users/projects, search past context, register reusable skills, or manage persistent context for AI assistants. Covers memory storage across domains (identity, projects, code, general), skill registration and discovery, and semantic search capabilities.
---

# Context Intelligence CLI

Command-line tool for persistent context management with Qdrant vector database. Store memories, register skills, and perform semantic search across contextual data.

**CRITICAL WORKFLOW - Follow these steps in order:**

1. **Check initialization status** - Always verify system is initialized before operations:

   ```bash
   context-cli status
   ```

   - If "Not initialized" - Run `context-cli init` first
   - If "Qdrant: Not reachable" - Check Qdrant instance or reconfigure

2. **Initialize if needed** - For first-time setup or reconfiguration:

   ```bash
   context-cli init
   ```

   Options:
   - Use existing setup (no-op)
   - Reinitialize collections
   - Change configuration
   - Reset everything

3. **Store memories** - Save context with domain classification:

   ```bash
   context-cli memory add "content" <domain> [--type note|preference|fact|decision|goal]
   ```

   Domains: `identity`, `projects`, `code`, `general`

4. **Search memories** - Semantic search across stored context:

   ```bash
   context-cli memory search "query" <domain>
   ```

5. **Manage skills** - Register and discover reusable skills (future enhancement)

## How It Works

1. User or agent needs to store/retrieve contextual information
2. Check if system is initialized with `context-cli status`
3. If not initialized, run `context-cli init` (guides through Docker or cloud setup)
4. Store memories with automatic embedding and vector storage
5. Search memories using semantic similarity
6. All data persisted in Qdrant collections

## Commands Reference

### Status and Initialization

```bash
# Check current status
context-cli status

# Initialize or reconfigure
context-cli init
```

### Memory Operations

```bash
# Add memory (domain can be with or without 'memory_' prefix)
context-cli memory add "I prefer TypeScript" identity --type preference
context-cli memory add "Using FastAPI for the backend" projects

# Search memories
context-cli memory search "preferences" identity
context-cli memory search "backend framework" projects
```

### Configuration

```bash
# View current config (API key masked)
context-cli config show

# Update API key
context-cli config set-key "your-key"

# Update Qdrant URL
context-cli config set-url "http://localhost:6333"
```

## Memory Types

- `note` - General notes (default)
- `preference` - User preferences
- `fact` - Established facts
- `decision` - Decisions made
- `goal` - Goals and objectives

## Memory Domains

- `identity` - Personal preferences, user facts, identity-related context
- `projects` - Project details, decisions, goals
- `code` - Code patterns, conventions, technical preferences
- `general` - General-purpose context and notes

## Examples

### Store User Preference

```bash
context-cli memory add "User prefers dark mode in all applications" identity --type preference
```

### Search Project Context

```bash
context-cli memory search "authentication setup" projects
```

### Check System Health

```bash
context-cli status
```

Output:
```
Status: Initialized
Qdrant URL: http://localhost:6333
API Key: abcd...wxyz
Qdrant: Reachable
Collections:
  - memory_identity
  - memory_projects
  - memory_code
  - memory_general
  - skills
```

## When to Use This Tool

- **Before starting work**: Check `context-cli status` to ensure system is ready
- **Storing context**: After learning user preferences, project decisions, or important facts
- **Retrieving context**: When you need to recall past decisions, preferences, or project details
- **Registering skills**: When defining reusable workflows or procedures (skill commands)

## Error Handling

All commands check for initialization and show helpful messages:

- "System not initialized. Please run: context-cli init"
- "Qdrant not reachable. Please run: context-cli init"

## Configuration File

Located at `~/.context-cli/config.json`:

```json
{
  "url": "http://localhost:6333",
  "api_key": "your-api-key"
}
```

## Tips

- **Always check status first** - Run `context-cli status` before memory operations
- **Use appropriate domains** - Store in correct domain for better organization
- **Set memory type** - Use `--type` to classify memories (preference, fact, decision, goal)
- **API key is masked** - `context-cli config show` masks API keys for security
- **Reinitialize safely** - Use "Reinitialize collections" option in `init` to rebuild without losing config
