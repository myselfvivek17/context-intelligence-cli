# Context Intelligence CLI

Model-agnostic middleware that gives any LLM persistent memory and reusable skills via Qdrant vector DB and FastEmbed. Built to reduce context pollution by offloading memories to a vector store instead of bloating your prompt. Works across Claude Desktop, Claude Code, Codex, and any MCP-compatible client. Switch models, keep your memory.

Companion to [context-mcp](https://github.com/myselfvivek17/context-intelligence) which provides the MCP server interface.

```bash
pip install git+https://github.com/myselfvivek17/context-intelligence.git
```

Reduce context pollution - store memories externally instead of stuffing prompts. Persistent across sessions. Semantic search. Skill management. Model-agnostic.

```bash
context-cli init          # Setup with Docker or cloud Qdrant
context-cli status        # Check system health
context-cli memory add "I prefer Python" identity
context-cli memory search "preferences" identity
```

Memory Domains: `identity` | `projects` | `code` | `general`

Requirements: Python 3.10+, Qdrant (Docker or cloud), FastEmbed

MIT License
