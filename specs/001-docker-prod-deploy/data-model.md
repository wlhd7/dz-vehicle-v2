# Data Model: Production Container Startup

## Entities

### Deployment Package
- **Purpose**: Represents the production-ready bundle used to start the service.
- **Key Fields**:
  - **Package Identifier**: Human-readable name or tag for the bundle.
  - **Build Timestamp**: When the package was produced.
  - **Target Service**: The service the package runs.

### Runtime Configuration
- **Purpose**: Environment-specific values required for production startup.
- **Key Fields**:
  - **Configuration Name**: Friendly label for the environment.
  - **Environment Values**: Key-value pairs required at runtime.
  - **Validation Status**: Whether required values are present.

### Access Endpoint
- **Purpose**: The public address used to reach the running service.
- **Key Fields**:
  - **Public IP**: `124.70.179.238`.
  - **Port**: `8081`.
  - **Primary Path**: `/`.

## Relationships

- A **Deployment Package** uses a **Runtime Configuration** during startup.
- A running **Deployment Package** exposes an **Access Endpoint**.

## State Transitions

- **Deployment Package**: Draft → Built → Available.
- **Runtime Configuration**: Defined → Validated → Active.
