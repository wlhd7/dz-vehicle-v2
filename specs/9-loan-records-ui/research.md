# Research: Loan Records Panel

## Decision 0.1: Backend Implementation for Loan Records
- **Decision**: Add `AssetService.list_loan_records` using a correlated subquery to find the return time for each pickup.
- **Rationale**: The `TransactionLog` table stores discrete events. To present a unified "loan activity" (pickup + return), we must link the `PICKUP` action with its corresponding `RETURN`. Since assets are checked out sequentially, the earliest `RETURN` after a `PICKUP` for the same asset is the correct pairing.
- **Query Structure**:
  ```sql
  SELECT 
      t1.id, 
      a.identifier, 
      a.type, 
      u.name as user_name, 
      t1.timestamp as loan_time,
      (SELECT MIN(t2.timestamp) 
       FROM transaction_logs t2 
       WHERE t2.asset_id = t1.asset_id 
         AND t2.action = 'RETURN' 
         AND t2.timestamp > t1.timestamp) as return_time
  FROM transaction_logs t1
  JOIN assets a ON t1.asset_id = a.id
  JOIN users u ON t1.user_id = u.id
  WHERE t1.action = 'PICKUP'
  ORDER BY t1.timestamp DESC
  LIMIT 200
  ```
- **Alternatives**: Storing `loan_id` in `TransactionLog`. Rejected as it would require schema changes. The subquery approach works with the current model.

## Decision 0.2: Frontend Route and View
- **Decision**: Add a new route `/loan-records` and a dedicated `LoanRecords.vue` view.
- **Rationale**: Following the project's pattern for `Admin.vue` and `VehicleInfo.vue`, a separate route ensures the login page remains clean and provides a focused space for history and filtering.
- **Filtering**: Implementation will be frontend-side filtering for the 200 records to minimize backend complexity and provide instant UI feedback.

## Decision 0.3: Public Accessibility
- **Decision**: The `/loan-records` route will be publicly accessible (no `ADMIN_SECRET` or login required).
- **Rationale**: As per the specification, this feature is for transparency and does not contain sensitive data that requires authorization, unlike the admin panel.

## Decision 0.4: Date Formatting
- **Decision**: Use `dayjs` or native `Intl.DateTimeFormat` to format dates as `YY-MM-DD HH:mm`.
- **Rationale**: Aligning with the clarified requirement in the spec.
