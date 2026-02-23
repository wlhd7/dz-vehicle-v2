#!/bin/bash
BRANCH_NAME=$(git branch --show-current)
FEATURE_DIR="specs/${BRANCH_NAME}"
FEATURE_SPEC="${FEATURE_DIR}/spec.md"
IMPL_PLAN="${FEATURE_DIR}/plan.md"

if [ ! -f "$IMPL_PLAN" ]; then
    cp .specify/templates/plan-template.md "$IMPL_PLAN" 2>/dev/null || touch "$IMPL_PLAN"
fi

if [ "$1" == "--json" ]; then
    echo "{"FEATURE_SPEC": "$FEATURE_SPEC", "IMPL_PLAN": "$IMPL_PLAN", "FEATURE_DIR": "$FEATURE_DIR", "BRANCH": "$BRANCH_NAME"}"
else
    echo "FEATURE_SPEC=$FEATURE_SPEC"
    echo "IMPL_PLAN=$IMPL_PLAN"
    echo "FEATURE_DIR=$FEATURE_DIR"
    echo "BRANCH=$BRANCH_NAME"
fi
