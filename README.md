# Elasticsearch 9.2.1 AI Demo

## Ports
- **Elasticsearch**: http://localhost:9201
- **Kibana**: http://localhost:5602

## Credentials
- **Username**: elastic
- **Password**: elastic123

## Quick Start

```bash
# Start services
docker-compose up -d

# Wait 30 seconds, then generate logs
python3 generate_scenario.py
```

## Setup AI Assistant

1. Open Kibana: http://localhost:5602
2. Login with credentials above
3. Go to **Management** → **Stack Management** → **Connectors**
4. Create OpenAI connector with `gpt-4o`
5. Click AI Assistant icon (✨) and select your connector
6. Create data view: `logs-app` or `logs-*`

## Test Scenario

The logs contain a cascading failure:
1. auth-service slow database queries
2. Connection pool exhaustion
3. API gateway timeouts
4. Circuit breakers open in payment/notification services

Ask the AI to discover the root cause!
