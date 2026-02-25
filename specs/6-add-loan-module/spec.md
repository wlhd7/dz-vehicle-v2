# Feature Specification: Inventory Loan Module

## Description
This feature adds a new sub-module named 'Loan' (借出) under the 'Inventory' (库存) module. The 'Loan' module will display a list of items that are currently borrowed, providing transparency on asset status and borrower information.

## Clarifications
### Session 2026-02-24
- Q: Should the 'Loan' module be strictly read-only for monitoring, or should it include administrative actions? → A: Read-only display for monitoring purposes.
- Q: Who should have access to view the 'Loan' module? → A: Publicly visible to all logged-in users.
- Q: What should be displayed in the 'Loan' module when the list is empty? → A: Hide the 'Loan' tab entirely if there are no active loans.
- Q: How should the 'Loan' module handle data updates to ensure accuracy? → A: Refresh data every time the 'Loan' tab is selected/clicked.
- Q: How should the system handle large lists of active loans? → A: Display all (approx. 10 items); only active loans, no history.

## User Scenarios

### Scenario 1: Viewing Loaned Items
**Actor**: Any Logged-in User
1. User navigates to the 'Inventory' (库存) module.
2. User selects the 'Loan' (借出) sub-module/tab.
3. User sees a list of all currently loaned items.
4. User confirms that the items are listed with 'Identifier', 'Type', and 'User'.
5. User observes that the most recently loaned items appear at the top of the list.

## Functional Requirements

### 1. Module Layout
- **1.1 Location**: The 'Loan' (借出) module must be a standalone section placed directly below the 'Inventory' (库存) module.
- **1.2 Visual Separation**: It should be visually distinct from the 'Inventory' module (e.g., its own header or container).
- **1.3 Visibility**: The 'Loan' module and its contents are visible to all logged-in users.
- **1.4 Conditional Display**: The 'Loan' section must only be visible when there is at least one active loan. If no items are loaned, the entire section must be hidden.

### 2. Loan List Display
- **2.1 Read-Only Constraint**: The list is for monitoring only; no interactive actions (like 'Return' or 'Edit') are required within this view.
- **2.2 Data Scope**: Only items currently in a 'borrowed' state are shown. Once an item is returned, it is immediately removed from this list.
- **2.3 Display Capacity**: As the total volume of assets is small (approx. 10), all active loans are displayed in a single view without pagination.
- **2.4 Data Refresh**: To ensure accuracy, the loan list data must be automatically refreshed every time the user selects/clicks the 'Loan' tab.
- **2.5 Column Layout**: The list must display exactly three columns:
    - **Identifier (标识符)**: The unique ID of the loaned asset.
    - **Type (类型)**: The category or type of the asset (e.g., Vehicle, Gas Card).
    - **User (使用者)**: The username of the individual who borrowed the item.
- **2.3 Sorting**: The records must be sorted by the time the loan was initiated.
    - **Order**: Descending (Newest records at the top, oldest at the bottom).

## Success Criteria
1. **Accessibility**: The 'Loan' module is clearly visible and accessible from the Inventory section.
2. **Data Accuracy**: Every item displayed in the 'Loan' module correctly reflects its 'Identifier', 'Type', and the 'User' who currently holds it.
3. **Correct Ordering**: The list correctly implements reverse-chronological sorting, verified by checking that the most recent loan action results in that item appearing at the top.
4. **Technology-Agnostic Display**: The UI correctly renders the table and column headers as specified, regardless of the underlying frontend framework.

## Key Entities
- **Asset**: The item being loaned (Vehicle, Gas Card, etc.).
- **User**: The borrower associated with the asset.
- **Loan Record**: The record linking an asset to a user and a timestamp.

## Assumptions
- **A1**: An 'Inventory' (库存) module already exists in the application.
- **A2**: Users have unique usernames that can be retrieved and displayed.
- **A3**: The system tracks the timestamp of when a loan occurs to support the required sorting.

## Constraints
- **C1**: The UI must maintain consistency with the existing 'Inventory' module's styling and layout.
- **C2**: Sorting must be handled efficiently to ensure fast load times as the number of loan records grows.
