# Context Intelligence CLI

A command-line tool for managing contextual memory and skills with Qdrant vector database. Enables persistent context storage and retrieval for AI assistants and agents.

## Features

- **Memory Management**: Store and search contextual memories across different domains (identity, projects, code, general)
- **Skill Storage**: Register and discover reusable skills with semantic search
- **Qdrant Integration**: Uses Qdrant vector database with fastembed for embeddings
- **Interactive Setup**: Guided initialization with Docker or cloud Qdrant support
- **Smart Initialization**: Detects existing setup and offers reconfiguration options

## Installation

```bash
cd context-intelligence-cli
pip install -e .
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

## License

MIT
