#!/bin/bash

# Simple mock of check-prerequisites.sh for current context
BRANCH_NAME=$(git branch --show-current)
FEATURE_DIR="specs/${BRANCH_NAME}"
FEATURE_SPEC="${FEATURE_DIR}/spec.md"

if [ "$1" == "--json" ] || [ "$2" == "--json" ]; then
    echo "{"FEATURE_DIR": "$FEATURE_DIR", "FEATURE_SPEC": "$FEATURE_SPEC"}"
else
    echo "FEATURE_DIR=$FEATURE_DIR"
    echo "FEATURE_SPEC=$FEATURE_SPEC"
fi
