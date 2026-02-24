# Feature Specification: UI Refactor & Borrowing/Returning Logic

## Description
This feature aims to simplify the user interface for the 'Using' (使用中) and 'Inventory' (库存) modules and update the business logic for borrowing and returning vehicles and gas cards to ensure a more streamlined and error-free user experience.

## Clarifications
- **Return Confirmation**: No confirmation dialog will be shown; clicking 'Return' triggers the process immediately.
- **Inventory Selection**: Clicking a new vehicle or gas card will automatically replace the previous selection in that category.
- **Module Visibility**: The 'Using' (使用中) module is only displayed when the user has active borrowings, so the 'Return' button's presence is tied to the module's visibility.

## User Scenarios

### Scenario 1: Returning Assets
**Actor**: User
1. User navigates to the 'Using' (使用中) module.
2. User sees their currently borrowed vehicle and/or gas card.
3. User clicks the 'Return' (归还) button in the bottom-right corner.
4. The system processes the return of all currently borrowed items (vehicle and/or gas card) simultaneously.
5. The assets are removed from the 'Using' module and returned to the 'Inventory' module.

### Scenario 2: Selecting Assets in Inventory
**Actor**: User
1. User navigates to the 'Inventory' (库存) module.
2. User sees two columns: 'Vehicle' (车辆) and 'Gas Card' (加油卡).
3. User clicks on a specific vehicle or gas card.
4. The background of the selected item turns light green, indicating it is selected.
5. User clicks the same item again to deselect it (background returns to normal).
6. User clicks a 'Borrow' button (assumed existing elsewhere or to be added) to finalize borrowing.

## Functional Requirements

### 1. 'Using' (使用中) Module UI
- **1.1 Remove 'Actions' List**: The existing list of individual actions for each item must be removed.
- **1.2 Return Button**: A single 'Return' (归还) button must be added to the bottom-right corner of the module.
- **1.3 Simultaneous Return Trigger**: Clicking the 'Return' button must trigger the simultaneous return (Requirement 3.2) of all items currently displayed in the 'Using' module.

### 2. 'Inventory' (库存) Module UI
- **2.1 Column Layout**: The module must display only two main columns: 'Vehicle' (车辆) and 'Gas Card' (加油卡).
- **2.2 Selection Mechanism**: 
    - Checkboxes must be removed.
    - Items are selected/deselected by clicking on the item text/row.
    - Selected items must have a light green background.
    - **Single Selection Logic**: If a vehicle is already selected, clicking another vehicle must deselect the first and select the new one. The same applies to gas cards.
- **2.3 Visual Feedback**: Selection must be visually distinct and toggleable.

### 3. Borrowing/Returning Logic
- **3.1 Borrowing Limits**: A user is restricted to borrowing a maximum of:
    - One vehicle AND one gas card OR
    - One vehicle OR
    - One gas card
- **3.2 Simultaneous Return**: If a user has borrowed multiple items (e.g., both a vehicle and a gas card), they must be returned together in a single action.

## Success Criteria
1. **Simplified Interaction**: Users can return all borrowed assets with a single click.
2. **Visual Clarity**: Selected items in the inventory are clearly highlighted with a light green background.
3. **Logic Enforcement**: The system prevents a user from borrowing more than one vehicle or one gas card at any given time.
4. **Data Integrity**: 100% of batch returns update the status of all involved assets atomically, with zero partial-update states recorded.

## Key Entities
- **Vehicle**: The vehicle asset being borrowed.
- **Gas Card**: The gas card asset being borrowed.
- **Borrowing Record**: The association between a user, a vehicle, and/or a gas card.

## Assumptions
- **A1**: A 'Borrow' button exists or will be implemented to finalize the selection made in the 'Inventory' module.
- **A2**: The 'Return' button will only be enabled/visible if the user has borrowed at least one item.
- **A3**: Standard confirmation patterns will be used for the 'Return' action unless specified otherwise.

## Constraints
- **C1**: UI changes must be consistent with the existing theme of the application.
- **C2**: Logic changes must be enforced at both the frontend and backend levels.
