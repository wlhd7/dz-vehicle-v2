# Feature Specification: Unattended Vehicle Asset Pickup

## Description
实现用户领取车钥匙或加油卡的无人值守系统。用户通过姓名和身份证后四位进行身份验证，验证通过后可自主领取或归还车辆钥匙及加油卡。系统通过提供由管理员预设的一次性临时密码来配合物理密码锁使用，并全程记录操作日志。

## Clarifications
### Session 2026-02-23
- Q: Are vehicle plates and gas cards bundled or independent? → A: Independent: Users select plate and gas card separately from available pools.
- Q: How to handle OTP pool exhaustion during pickup? → A: Block & Notify: Prevent pickup actions and show a "Contact Admin" message if the OTP pool is empty.
- Q: How does the return verification work? → A: Open Return: Users click return and are shown a code to open the locker (same as pickup).
- Q: How to handle two users trying to pick up the same asset? → A: First-to-Click: The first person to "Confirm Pickup" gets the asset; others see "Already Checked Out" immediately.
- Q: What notification method for low OTP levels? → A: Dual Notification: Dashboard alert (red badge) and email for OTP thresholds.

## User Scenarios

### Scenario 1: First-time User Pickup
**Actor**: Employee (User)
1. User accesses the system for the first time.
2. User enters their full name and the last 4 digits of their ID card.
3. System validates the input against the administrator-provided whitelist.
4. System authenticates the user and directs them to the pickup interface.
5. User selects a vehicle plate number and a gas card.
6. User clicks "Confirm Pickup".
7. System displays a one-time temporary password (OTP) and records the transaction.
8. User uses the OTP to open the physical key box/locker.

### Scenario 2: Returning an Asset
**Actor**: Employee (User)
1. User (previously authenticated) accesses the system.
2. System identifies the user (via session/cookie) and displays the currently held assets.
3. User clicks "One-click Return" for the vehicle key or gas card.
4. System displays a new one-time temporary password (OTP) to open the physical locker.
5. System records the return time and updates the asset status.
6. User uses the OTP to open the locker and return the asset.

### Scenario 3: Admin Asset Management
**Actor**: Administrator
1. Admin logs into the management dashboard.
2. Admin adds a new vehicle plate number and a corresponding gas card to the inventory.
3. Admin uploads a batch of temporary passwords to the OTP pool.
4. Admin updates the user whitelist with new employee names and ID digits.

## Functional Requirements

### 1. Identity Verification
- **1.1 First-time Login**: Users must provide Name and ID (Last 4 digits) for verification.
- **1.2 Whitelist Matching**: Authentication only succeeds if the combination exists in the admin-managed whitelist.
- **1.3 Persistent Session**: After successful verification, users should be able to access the pickup interface directly in subsequent visits (using standard web persistence).

### 2. Pickup & Return Workflow
- **2.1 Asset Selection**: Users can select one vehicle plate, one gas card, or both in a single transaction. These assets are managed independently and are not bundled.
- **2.2 OTP Distribution**: Every pickup and return action must trigger the generation of a unique temporary password from the pool.
- **2.3 OTP Consumption**: Once a password is displayed to a user, it must be marked as "used" or deleted from the pool to ensure it is one-time only.
- **2.4 Asset Status Tracking**: The system must track which assets are currently held by which users.
- **2.5 OTP Exhaustion Handling**: If the OTP pool is empty, the system must block the "Confirm Pickup/Return" action and display a "No passwords available, please contact Administrator" message.

### 3. Logging & Monitoring
- **3.1 Transaction Logs**: Every action (pickup/return) must record: User Name, Action Type, Asset Identifier, and Timestamp.
- **3.2 Low Password Alert**: When the number of available passwords in the OTP pool falls below 30, the system must notify the administrator via both a dashboard alert (red badge) and an email.

### 4. Administrative Controls
- **4.1 Asset CRUD**: Administrators can create, read, update, and delete vehicle plate numbers and gas card numbers.
- **4.2 OTP Pool Management**: Administrators can upload and manage the list of temporary passwords.
- **4.3 Whitelist Management**: Administrators can manage the authorized user list.

## Success Criteria
1. **Verification Accuracy**: 100% of unauthorized access attempts are blocked.
2. **OTP Reliability**: Every confirmed pickup or return action provides a valid, unique password from the pool.
3. **Log Integrity**: Every transaction is recorded with accurate user and timestamp data, viewable by admins.
4. **Alert Timeliness**: Admin notification for low OTP pool is triggered within 1 minute of reaching the threshold (<30).

## Key Entities
- **User**: Name, ID_Last4, Status (Active/Inactive)
- **Asset**: Type (Key/Card), Identifier (Plate#/Card#), Status (Available/Checked Out), Current Holder ID
- **OTP Pool**: Password String, Usage Status, Date Added
- **Log**: Timestamp, User_Ref, Action (Pickup/Return), Asset_Ref

## Assumptions
- **A1**: User identity persistence is handled via browser cookies or local storage for a reasonable duration (e.g., 30 days).
- **A2**: Physical security (the locker) is compatible with 4-6 digit numeric passwords provided by the system.
- **A3**: Administrator notifications will be delivered via a "Notification Center" in the admin dashboard and an optional system email.

## Constraints
- **C1**: One-time passwords cannot be reused.
- **C2**: Users cannot pick up assets that are already checked out by another user.
- **C3**: Concurrent access is handled via "First-to-Click": the first user to submit the pickup request for an asset secures it; subsequent concurrent requests for the same asset will fail with an "Already Checked Out" error.
