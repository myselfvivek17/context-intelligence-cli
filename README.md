# Context Intelligence CLI

Model-agnostic middleware that gives any LLM persistent memory and reusable skills via Qdrant vector DB and FastEmbed. Built to reduce context pollution by offloading memories to a vector store instead of bloating your prompt. Works across Claude Desktop, Claude Code, Codex, and any MCP-compatible client. Switch models, keep your memory.

**Companion to [context-mcp](https://github.com/myselfvivek17/context-intelligence) - the MCP server interface for seamless LLM integration.**

## Features

- **Reduce Context Pollution** - Store memories externally instead of stuffing prompts with context
- **Memory Management** - Store and search contextual memories across different domains (identity, projects, code, general)
- **Skill Storage** - Register and discover reusable skills with semantic search
- **Qdrant Integration** - Uses Qdrant vector database with fastembed for embeddings
- **Interactive Setup** - Guided initialization with Docker or cloud Qdrant support
- **Smart Initialization** - Detects existing setup and offers reconfiguration options
- **Model-Agnostic** - Works across Claude, Codex, and any MCP-compatible client

## Installation

```bash
cd context-intelligence-cli
pip install -e .
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/myselfvivek17/context-intelligence-cli.git
```

## Quick Start

### 1. Initialize the System

```bash
context-cli init
```

Choose from:
- Use existing Qdrant instance
- Docker setup (automatic)
- Cloud Qdrant configuration

### 2. Check Status

```bash
context-cli status
```

### 3. Store a Memory

```bash
context-cli memory add "I prefer Python over JavaScript" --domain identity
```

### 4. Search Memories

```bash
context-cli memory search "preferences" --domain identity
```

## Commands

### Initialization
- `context-cli init` - Initialize or reconfigure the system
- `context-cli status` - Show current status and configuration

### Memory Management
- `context-cli memory add <content> <domain> [--type]` - Store a memory
- `context-cli memory search <query> <domain>` - Search memories

### Configuration
- `context-cli config show` - Show current configuration (API key masked)
- `context-cli config set-key <key>` - Update API key
- `context-cli config set-url <url>` - Update Qdrant URL

## Memory Domains

- `identity` - Personal preferences, facts about the user
- `projects` - Project-related context and decisions
- `code` - Code patterns, conventions, preferences
- `general` - General-purpose context

## Memory Types

- `note` - General notes (default)
- `preference` - User preferences
- `fact` - Established facts
- `decision` - Decisions made
- `goal` - Goals and objectives

## Configuration

Configuration is stored at `~/.context-cli/config.json`:

```json
{
  "url": "http://localhost:6333",
  "api_key": "your-api-key"
}
```

## Requirements

- Python 3.10+
- Qdrant (local via Docker or cloud instance)
- pip packages: typer, questionary, qdrant-client[fastembed], pydantic, fastembed

## Development

```bash
# Install in editable mode
pip install -e .

# Run CLI
context-cli --help
```

## Why Context Intelligence CLI?

Large language models suffer from context pollution - prompts get bloated with accumulated context, slowing down inference and increasing costs. Context Intelligence CLI solves this by:

- **Externalizing context** - Store memories in a vector database instead of prompts
- **Semantic retrieval** - Fetch only relevant context when needed
- **Persistence** - Memories persist across sessions and model switches
- **Model independence** - Switch between Claude, GPT, or any LLM without losing context

## License

MIT
