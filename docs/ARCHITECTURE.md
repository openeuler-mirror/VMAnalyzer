# VMAnalyzer Architecture

## System Design

### Data Flow
1. Collection (libvirt → VMStatsCollector)
2. Storage (Redis/InfluxDB)
3. Analysis (VMStatsAnalyzer)
4. Reporting (Console/File/API)

### Components
- **Agent**: Core collection and analysis
- **Gather**: Individual metric collectors
- **Utils**: Shared utilities
