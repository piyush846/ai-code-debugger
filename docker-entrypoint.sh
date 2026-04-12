#!/bin/bash
echo "Waiting for Ollama to be ready..."
until curl -s http://ollama:11434 > /dev/null 2>&1; do
    sleep 2
done
echo "Ollama is ready."
echo "Pulling model: $AIDBG_MODEL"
curl -s -X POST http://ollama:11434/api/pull -d "{\"name\":\"$AIDBG_MODEL\"}" > /dev/null
echo "aidbg is ready."
exec "$@"