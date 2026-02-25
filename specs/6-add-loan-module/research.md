# Research: Inventory Loan Module

## Decision 0.1: Backend Method for Active Loans
- **Decision**: Add a new method `AssetService.list_active_loans`.
- **Rationale**: `list_assets` is used for general inventory. `list_active_loans` requires a join with `TransactionLog` to get the latest pickup timestamp for sorting, and a join with `User` to get the username. Combining this into `list_assets` would overcomplicate the existing API.
- **Alternatives**: Extending `list_assets(status='CHECKED_OUT')`. Rejected because it wouldn't easily provide the sorting by loan time or the username without extra joins that might not be needed for simple status listing.

## Decision 0.2: Sorting Logic
- **Decision**: Sort by `TransactionLog.timestamp` descending where `action` is `PICKUP` for the currently held asset.
- **Rationale**: The requirement specifically asks for "the order in which they were borrowed" (按借出的先后顺序). Using the latest `PICKUP` log entry for each `CHECKED_OUT` asset is the most reliable way to determine this.

## Decision 0.3: Frontend Integration
- **Decision**: Add the 'Loan' tab in `Dashboard.vue` (or the relevant inventory view) with a `v-if` check on the fetched loan count.
- **Rationale**: To fulfill the "hide if empty" requirement, the parent component must fetch or check the loan status before rendering the tab.
- **Alternatives**: CSS-based hiding. Rejected because `v-if` is cleaner for conditional UI elements in Vue.
