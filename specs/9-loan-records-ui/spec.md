# Specification: Loan Records Panel

**Feature Name**: Loan Records Panel
**Status**: Draft
**Created**: 2026-02-25
**Branch**: `9-loan-records-ui`

## Description

Add a "Loan Records" (领取记录) panel to the login screen to provide transparency into the usage history of vehicles and gas cards. This panel will display the most recent 200 loan activities, allowing users and administrators to track who is currently using an asset and review past usage. The feature includes filtering capabilities to quickly find records for specific vehicles or types of assets.

## Clarifications

### Session 2026-02-25
- Q: Empty State Handling: How should the UI behave when no records match the filters or if the list is empty? → A: Display "无记录" (No records).
- Q: UI Presentation: Should the loan records be shown in a modal or a separate route/view? → A: Separate Route/View (e.g., `/loan-records`).
- Q: Navigation Back: How should users return to the login screen from the Loan Records view? → A: "返回登录" (Back to Login) link/button.
- Q: Data Refresh Frequency: How often should the loan records data refresh? → A: Manual (Standard browser refresh).
- Q: Time Format: What format should be used for Loan Time and Return Time? → A: YY-MM-DD HH:mm.

## User Scenarios & Testing

### Scenario 1: Accessing Loan Records
- **Given** any user is on the login screen
- **When** they click the "领取记录" link next to "车辆信息"
- **Then** they see a panel displaying a table of recent loan activities
- **And** the list is sorted by loan time in descending order (most recent first)
- **And** the list is limited to the 200 most recent records

### Scenario 2: Filtering Records by Asset Type
- **Given** a user is viewing the "Loan Records" panel
- **When** they select "车辆" (Vehicle) from the "类型" (Type) filter
- **Then** only records for vehicles are displayed
- **When** they select "加油卡" (Gas Card) from the "类型" (Type) filter
- **Then** only records for gas cards are displayed

### Scenario 3: Filtering Records by Identifier
- **Given** a user is viewing the "Loan Records" panel
- **When** they select a specific license plate (e.g., "京A88888") from the "标识符" (Identifier) filter
- **Then** only records for that specific vehicle are displayed
- **When** they select a specific gas card identifier from the filter
- **Then** only records for that specific gas card are displayed

### Scenario 4: Identifying Active Loans
- **Given** an asset that has been picked up but not yet returned
- **When** a user views the "Loan Records" panel
- **Then** the "归还时间" (Return Time) for that record is blank
- **When** the asset is subsequently returned
- **Then** the record is updated to show the actual return time

## Functional Requirements

### 1. UI Navigation
- Add "领取记录" link to the login page.
- Position: To the left of "车辆信息" (Vehicle Information), separated by a vertical bar (`|`).
- Resulting layout: `领取记录 | 车辆信息 | 管理面板`.
- Unlike "车辆信息" and "管理面板", the "领取记录" view is publicly viewable and does not require `ADMIN_SECRET`.
- **Route**: Accessible via a dedicated route (e.g., `/loan-records`).
- **Navigation Back**: Include a "返回登录" (Back to Login) link or button to return to the root login view.

### 2. Loan Records Display
- **View Title**: 领取记录
- **Table Columns**:
  - **标识符 (Identifier)**: License plate or gas card ID. Supports Excel-style dropdown filtering within the header.
  - **类型 (Type)**: "车辆" or "加油卡". Supports Excel-style dropdown filtering within the header.
  - **领用者 (User)**: Name of the person who took the asset.
  - **领用时间 (Loan Time)**: Date and time when picked up (Format: YY-MM-DD HH:mm).
  - **归还时间 (Return Time)**: Date and time when returned (Format: YY-MM-DD HH:mm).
- **Record Limit**: Fetch the 200 most recent records from the backend.
- **Pagination**: Display 8 records per page.
- **Sorting**: Default sort by `Loan Time` descending.
- **Empty State**: If no records are found or match the filters, display "无记录" (No records) in place of the table body.
- **Data Refresh**: Data is fetched on initial view load. Subsequent updates (including the population of return times) are available in the backend immediately but require a manual page refresh to be reflected in the UI.

### 3. Filtering Capabilities (Integrated)
- Filtering is integrated directly into the column headers (Excel-style).
- **Identifier Filter**: A searchable dropdown within the "标识符" column header.
- **Type Filter**: A dropdown within the "类型" column header with options: "车辆" (Vehicle), "加油卡" (Gas Card).
- **UX Requirement**: The entire column header cell (including the title text and surrounding area) must be clickable to trigger the filter dropdown, providing a seamless Excel-like experience.
- **Filtering Logic**: Filtering is applied to the entire fetched set (up to 200 records).

### 4. Data Logic
- **Active Loans**: For items that have not been returned, the "归还时间" must be empty/blank in the UI.
- **Updates**: When an item is returned, the backend record must be updated immediately. The Loan Records view will display this update upon the next page load or manual refresh.

## Success Criteria

- The login page correctly displays the "领取记录 | 车辆信息 | 管理面板" navigation.
- Clicking "领取记录" opens a panel showing up to 200 recent records.
- The table correctly identifies active loans by leaving the return time blank.
- Filtering by type (Vehicle/Gas Card) accurately narrows the list.
- Filtering by identifier (specific plate/card) accurately narrows the list.
- All UI text is in Simplified Chinese as per project standards.

## Key Entities

### Loan Record (Derived from existing Loan/Asset data)
- `asset_identifier`: String (License plate or card ID)
- `asset_type`: Enum (Vehicle, Gas Card)
- `user_name`: String
- `loan_time`: DateTime
- `return_time`: DateTime (Nullable)

## Assumptions
- The "Identifier" filter dropdown should include both active assets and potentially deleted ones if they have historical records, though focusing on current inventory is the priority.
- The 200-record limit is a fixed requirement for this view to ensure performance and clarity.
- No authentication is required to view these records as they are intended for public transparency within the organization.
