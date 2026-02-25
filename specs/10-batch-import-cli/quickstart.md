# Quickstart: Batch Import CLI

## Installation
Ensure the CLI is installed in development mode:
```bash
pip install -e .
```

## Setup Admin Secret
Export the secret to authorize admin commands:
```bash
export ADMIN_SECRET="your-secret"
```

## Batch Add Users
Create a file `users.txt`:
```text
Alice,1234
Bob,5678,Charlie,9012
```

Run the import:
```bash
vehicle-asset admin batch-add-users users.txt
```

## Seed OTPs
Create a file `otps.txt`:
```text
12345678,87654321,11112222
33334444
```

Run the seed command:
```bash
vehicle-asset admin seed-otps --file otps.txt
```
