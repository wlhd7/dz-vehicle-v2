# Specification: Admin Vehicle Information Management

**Feature Name**: Admin Vehicle Information Management
**Status**: Draft
**Created**: 2026-02-25
**Branch**: `8-admin-vehicle-info`

## Description

Add a dedicated "Vehicle Information" (车辆信息) panel accessible from the login screen for administrators. This panel allows tracking of critical vehicle maintenance and compliance dates, including maintenance history, annual inspections, and insurance renewals. The system provides visual alerts for items requiring attention (e.g., overdue maintenance or upcoming inspections).

## Clarifications

### Session 2026-02-25
- Q: 如何通知管理员？ (How to notify administrators?) → A: 给管理员发邮件 (Send emails to administrators).
- Q: 管理员邮箱如何配置？ (How to configure admin email?) → A: 通过系统配置文件（.env）设置 (Configured via system .env file).
- Q: 邮件发送频率是多少？ (What is the email frequency?) → A: 每周发送一次，直到相关车辆信息被管理员更新 (Weekly, until the vehicle info is updated).

## User Scenarios & Testing

### Scenario 1: Accessing Vehicle Information
- **Given** an administrator is on the login screen
- **When** they click the "车辆信息" link next to "管理面板"
- **Then** they are prompted for the `ADMIN_SECRET` (if not already stored in the browser)
- **And** upon providing the correct secret, they see a list of all vehicles (AssetType.KEY)

### Scenario 2: Updating Vehicle Information
- **Given** an administrator is in the "Vehicle Information" panel
- **When** they select a vehicle and update its maintenance date, mileage, inspection date, or insurance date
- **Then** the information is persisted in the system
- **And** the list view updates to reflect the changes

### Scenario 3: Monitoring Vehicle Status (Alerts)
- **Given** a vehicle has a maintenance date older than 6 months
- **When** an administrator views the "Vehicle Information" panel
- **Then** the vehicle is highlighted with a warning indicating overdue maintenance
- **Given** a vehicle's annual inspection or insurance expires within one month
- **When** an administrator views the panel
- **Then** the vehicle is highlighted with a warning for the upcoming expiration

## Functional Requirements

### 1. UI Navigation
- Add "车辆信息" link to the login page, positioned to the left of "管理面板" (Admin Panel), separated by a vertical bar (`|`).
- Access to the "Vehicle Information" panel requires `ADMIN_SECRET` authorization.

### 2. Vehicle Information Tracking
- Each vehicle (Asset of type `KEY`) must support the following data fields:
  - **Maintenance Date** (上次保养日期)
  - **Maintenance Mileage** (上次保养公里数)
  - **Annual Inspection Date** (年审到期时间)
  - **Insurance Expiration Date** (车险到期时间)
- Administrators can edit these fields for any vehicle in the inventory.

### 3. Administrator Notifications (Alerts)
- **Visual Alerts**: The system must identify and highlight vehicles requiring attention in the UI:
  - **Maintenance Warning**: If the current date is more than 6 months after the recorded maintenance date.
  - **Inspection Warning**: If the current date is within 30 days of the annual inspection date.
  - **Insurance Warning**: If the current date is within 30 days of the insurance expiration date.
  - **Style**: Use row background color changes (e.g., orange) and a warning icon (⚠️) for highlighted vehicles.
- **Email Notifications**: The system must send email alerts to the administrator's registered email address when the above thresholds are met.
  - **Frequency**: Send once per week (e.g., every Monday) for all vehicles currently in a "Warning" state.
  - **Persistence**: Continue sending until the administrator updates the corresponding vehicle's maintenance or compliance records.
  - **Content**: The email must include an aggregated list of all warning vehicles, specifying for each:
    - Vehicle Identifier (License Plate)
    - Alert Type (Maintenance / Inspection / Insurance)
    - Relevant Date (Last maintenance date / Expiration date)
    - Current Status (e.g., "Overdue by 15 days" or "Expiring in 10 days")

### 4. Admin-Only Editing
- Only users with valid `ADMIN_SECRET` can modify vehicle information.
- Regular users cannot see or access this data.

## Success Criteria

- Administrators can successfully view and update maintenance/compliance dates for all vehicles.
- The login page correctly displays the "车辆信息 | 管理面板" navigation.
- Vehicles with overdue maintenance (> 6 months) or upcoming expirations (within 30 days) are clearly flagged in the UI with a distinct color and warning icon.
- **Email Delivery**: Automated email alerts are triggered and successfully delivered to administrators for all three alert types (Maintenance, Inspection, Insurance).
- All date calculations for alerts are accurate and relative to the current system date.

## Key Entities

### Asset (Updated)
- `maintenance_date`: DateTime (Optional)
- `maintenance_mileage`: Integer/Float (Optional)
- `inspection_date`: DateTime (Optional)
- `insurance_date`: DateTime (Optional)

## Assumptions
- `ADMIN_NOTIFICATION_EMAIL` environment variable will be used to store recipient address.
- "Notify administrator" refers to both visual indicators/alerts within the panel and email alerts.
- Maintenance alerts are strictly date-based (6 months) as specified, though mileage is recorded.
- The `ADMIN_SECRET` mechanism used for the existing Admin Panel is sufficient for securing this new panel.
