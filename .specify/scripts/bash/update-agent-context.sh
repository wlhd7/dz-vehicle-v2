#!/bin/bash
# Mock update-agent-context.sh
AGENT=$1
echo "Updating context for $AGENT..."
# In a real scenario, this would append to a .gemini/context or similar
mkdir -p .gemini
echo "Current Feature: Unattended Pickup" >> .gemini/context
echo "Tech Stack: Python, SQLite, Typer" >> .gemini/context
