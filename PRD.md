# Product Requirements Document (PRD) - dz-vehicle-v2

## 1. Project Overview
`dz-vehicle-v2` is an unattended vehicle asset management system designed to facilitate the borrowing and returning of vehicles and gas cards. The system focuses on simplicity, security, and a localized experience for Chinese-speaking users.

## 2. Target Audience
- **Employees**: Users who need to pick up and return vehicles and gas cards for work.
- **Administrators**: Users responsible for managing the asset inventory, user whitelist, and system security.

## 3. Core Features

### 3.1 Unattended Pickup & Return
- **Asset Categorization**: Assets are divided into "Vehicles" (represented by keys) and "Gas Cards".
- **Simplified Selection**: Users select one vehicle and/or one gas card from the inventory.
- **Bulk Return**: Users can return all held assets with a single action.
- **Workflow Enforcement**: Users are limited to borrowing one vehicle and one gas card at a time.
- **Persistent OTP Display**: Codes for opening lockers are displayed directly in the UI with a green border, replacing intrusive popups.
- **Auto-Expiration**: OTP displays automatically disappear after 2 hours to maintain UI cleanliness and security.
- **Refresh Persistence**: Displayed codes survive page refreshes and browser restarts until they expire.

### 3.2 Administrative Management
- **User Whitelist**: Manage users who are authorized to use the system.
- **Asset Inventory**: Add, update, and delete vehicles and gas cards.
- **OTP Pool**: Generate One-Time Passwords for secure operations.
- **Loan Monitoring**: View active loans and their current holders via CLI and Dashboard.
- **CLI & API Access**: Full administrative control via command line and REST API.

### 3.3 Security Validation
- **Admin Secret**: Administrative operations are protected by a mandatory secret (`ADMIN_SECRET`).
- **Environment Configuration**: Support for `.env` files to manage secrets securely.

### 3.4 Chinese Localization
- **Localized UI**: Complete frontend localization in Simplified Chinese.
- **Modern Typography**: High-quality Chinese font stack for better legibility.

### 3.5 Vehicle Maintenance & Compliance Tracking
- **Maintenance Records**: Track the date and mileage of the last vehicle maintenance.
- **Compliance Monitoring**: Manage annual inspection and insurance expiration dates.
- **Visual Alerts**: Highlight vehicles in the management UI (orange background + ⚠️ icon) when maintenance is overdue (>6 months) or compliance is expiring within 30 days.
- **Automated Notifications**: Weekly email reports sent to administrators summarizing all active vehicle warnings.
- **Management Panel**: Dedicated "Vehicle Information" (车辆信息) panel for administrators to update these records securely.

## 4. Technical Stack
- **Backend**:
  - Language: Python 3.x
  - Framework: FastAPI (API), Typer (CLI)
  - Database: SQLite
  - Testing: Pytest (Strict TDD)
- **Frontend**:
  - Framework: Vue 3 + TypeScript
  - UI Library: Element Plus
  - Localization: Vue-i18n
  - Build Tool: Vite

## 5. Success Criteria
- **User Efficiency**: Reduction in time taken to pick up/return assets through the simplified UI.
- **System Integrity**: 100% atomic updates for asset status changes.
- **Security**: No unauthorized access to administrative endpoints.
- **User Satisfaction**: Positive feedback on the localized Chinese interface.
