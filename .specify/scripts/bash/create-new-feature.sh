#!/bin/bash

# Parse arguments
NUMBER=""
SHORT_NAME=""
JSON_OUTPUT=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --number) NUMBER="$2"; shift ;;
        --short-name) SHORT_NAME="$2"; shift ;;
        --json) JSON_OUTPUT=true ;;
        *) DESCRIPTION="$1" ;;
    esac
    shift
done

if [[ -z "$NUMBER" || -z "$SHORT_NAME" ]]; then
    echo "Usage: $0 --number <N> --short-name <name> <description>"
    exit 1
fi

BRANCH_NAME="${NUMBER}-${SHORT_NAME}"
FEATURE_DIR="specs/${BRANCH_NAME}"
SPEC_FILE="${FEATURE_DIR}/spec.md"

# Create branch
git checkout -b "$BRANCH_NAME"

# Create directory structure
mkdir -p "${FEATURE_DIR}/checklists"

# Create empty spec file
touch "$SPEC_FILE"

if [ "$JSON_OUTPUT" = true ]; then
    echo "{"BRANCH_NAME": "$BRANCH_NAME", "FEATURE_DIR": "$FEATURE_DIR", "SPEC_FILE": "$SPEC_FILE"}"
else
    echo "Created branch $BRANCH_NAME and directory $FEATURE_DIR"
fi
