# Research: Batch Import CLI

## Decision: Unified Delimiter Parsing
- **Chosen**: Regex split `re.split(r'[,
]+', content)`.
- **Rationale**: Cleanly handles mixed commas and newlines. It also allows for optional spaces if we strip each token.
- **Alternatives**: 
    - `csv` module: Overkill for simple comma/newline lists and less flexible with mixed newline/comma delimiters without specific dialect tuning.
    - String `.replace('
', ',').split(',')`: Simple, but regex is more robust for multiple consecutive delimiters.

## Decision: Atomic Validation Logic
- **Chosen**: "Pre-scan and Validate" pattern.
- **Rationale**: Before opening a transaction or adding any records, the entire list of tokens extracted from the file is validated.
    - Whitelist: Token count must be even. Each `ID_last4` must be exactly 4 characters (numeric check optional but recommended).
    - OTP: Every token must be exactly 8 digits.
- **Rationale**: Adheres to the "Atomic Processing" requirement from the spec.

## Decision: Duplicate Handling
- **Chosen**: Skip silently but report in summary.
- **Rationale**: Provides a smooth user experience where the system "reaches the desired state" without erroring out on partial overlap with existing data.
