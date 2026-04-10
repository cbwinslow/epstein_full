# Documentation

This directory contains comprehensive documentation for the Epstein Research System.

## Structure

```
docs/
├── agents/                    # Agent documentation
│   ├── README.md             # Agent overview
│   ├── discovery/            # Discovery agents
│   │   └── news.md           # News discovery agent
│   ├── collection/            # Collection agents
│   │   └── news.md           # News collection agent
│   └── processing/            # Processing agents
│       └── embeddings.md      # Embeddings processing
├── architecture/             # System architecture
│   └── README.md             # Architecture overview
├── api/                      # API documentation
│   └── embeddings.md         # Embeddings API
└── guides/                   # User guides
```

## Quick Links

### Getting Started
- [System Architecture](architecture/README.md) - Overview of system components
- [News Discovery Agent](agents/discovery/news.md) - How news articles are discovered
- [Embeddings Processing](agents/processing/embeddings.md) - Vector embeddings setup

### API Documentation
- [Embeddings API](api/embeddings.md) - Windows GPU embeddings endpoint

### Agent Documentation
- [Agent Overview](agents/README.md) - All agents and their roles
- [Discovery Agents](agents/discovery/) - Content discovery
- [Collection Agents](agents/collection/) - Content download
- [Processing Agents](agents/processing/) - Content analysis

## Documentation Standards

This documentation follows industry standards:
- **Markdown** for all documentation
- **Diagrams** using ASCII art for architecture
- **Code blocks** with syntax highlighting
- **API docs** following OpenAPI specification style
- **Troubleshooting** sections in each document
- **Performance metrics** where applicable

## Contributing

When adding new documentation:
1. Create appropriate subdirectory structure
2. Use markdown with proper formatting
3. Include code examples
4. Add troubleshooting section
5. Update this README with link

## Related Documentation

- [AGENTS.md](../../AGENTS.md) - Original agent documentation (legacy)
- [PROJECT.md](../../PROJECT.md) - Project overview
- [README.md](../../README.md) - Main project README
