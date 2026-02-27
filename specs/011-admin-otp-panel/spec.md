# Feature Specification: Admin OTP Management Panel

**Feature Branch**: `011-admin-otp-panel`  
**Created**: 2026-02-27  
**Status**: Draft  
**Input**: User description: "新增 otp管理 panel - 不需要添加导航链接 - 指定一个管理员 - 管理员 dashboard panel 登出按钮左边添加一个 otp panel 链接 <otp panel 功能>: - 显示剩余 otp - 添加单个 otp - 批量添加 otp （输入文件与 cli 的批量添加一致）"

## Clarifications

### Session 2026-02-27
- Q: 是否记录审计日志？ → A: 不记录任何专门的审计信息。
- Q: 批量上传出错时是否显示详细错误？ → A: 仅显示一般错误消息（例如：“文件中包含无效的 OTP 格式”）。
- Q: 是否实施频率限制？ → A: 不实施频率限制（信任管理员）。
- Q: 批量导入中如何处理重复项？ → A: 不考虑重复项处理。
- Q: 批量导入成功后的反馈内容？ → A: 显示“成功导入 [数量] 个 OTP，当前池总数为 [总数]”。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - OTP Pool Oversight (Priority: P1)

As the designated Administrator (identified by a specific user name, e.g., `admin01`), I want to see how many unused OTPs are left in the pool so that I can decide when to add more before the pool is exhausted.

**Why this priority**: Crucial for system availability. If the OTP pool is empty, users cannot pick up or return vehicles.

**Independent Test**: Log in as the specific designated Admin, navigate to the OTP Panel (independent sub-page) via the new link, and verify that the "Remaining OTPs" count matches the database state.

**Acceptance Scenarios**:

1. **Given** the Admin is on the Admin Dashboard, **When** they look at the header area, **Then** they see an "OTP管理" (or icon) link to the left of the "Logout" button.
2. **Given** the Admin clicks the OTP link, **When** the OTP Panel opens, **Then** it displays the current count of unused OTPs (e.g., "剩余可用 OTP: 145").

---

### User Story 2 - Manual OTP Injection (Priority: P2)

As an Administrator, I want to add a single specific OTP to the pool manually for testing or emergency replenishment.

**Why this priority**: Provides a quick way to resolve immediate exhaustion without creating a file.

**Independent Test**: Enter an 8-digit code in the "Add Single OTP" field and verify it appears in the pool (count increments).

**Acceptance Scenarios**:

1. **Given** the Admin is in the OTP Panel, **When** they enter a valid 8-digit numeric code and click "添加", **Then** the code is added to the database and the remaining count updates.
2. **Given** the Admin enters an invalid code (e.g., 7 digits or non-numeric), **When** they click "添加", **Then** the system shows a validation error and does not add the record.

---

### User Story 3 - Batch OTP Import (Priority: P1)

As an Administrator, I want to upload a file containing many OTPs to seed the pool efficiently, using the same format I use for the CLI tool.

**Why this priority**: Necessary for initial setup and large-scale replenishment.

**Independent Test**: Upload a text file with 10 valid 8-digit OTPs and verify the pool count increases by 10.

**Acceptance Scenarios**:

1. **Given** the Admin selects a `.txt` or `.csv` file, **When** they click "批量上传", **Then** the system parses the file (newline or comma-separated), adds all valid 8-digit codes, and displays a success message: "成功导入 [数量] 个 OTP，当前池总数为 [总数]".
2. **Given** the upload file contains an invalid entry (e.g., "abc" or "1234"), **When** the Admin uploads it, **Then** the entire operation fails (atomic), and an error message identifies the invalid format.

---

### Edge Cases

- **Duplicate OTPs**: If an Admin tries to add an OTP that already exists and is unused, the system should skip it or notify the user without creating duplicates.
- **Empty File**: Uploading an empty file should return a friendly "No data found" message.
- **Unauthorized Access**: If a non-designated user tries to access the OTP Panel URL directly, they should be redirected to the Dashboard.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a link to the OTP Management Panel in the Admin Dashboard header, positioned immediately to the left of the "Logout" (登出) button.
- **FR-002**: System MUST NOT add any links to the main sidebar or global navigation menu for this feature.
- **FR-003**: Access to the OTP Management Panel MUST be restricted to the user whose name matches the `VITE_OTP_ADMIN_NAME` configuration.
- **FR-004**: The OTP Panel MUST display the real-time count of `is_used = False` records in the `OTPPool`.
- **FR-005**: The Panel MUST allow manual entry of a single 8-digit numeric OTP.
- **FR-006**: The Panel MUST support file uploads for batch adding OTPs.
- **FR-007**: Batch import MUST support newline-separated and comma-separated 8-digit numeric tokens, consistent with the CLI `seed-otps` command.
- **FR-008**: Batch import MUST be atomic; if any token in the file is invalid (not exactly 8 digits), the entire upload MUST be rejected.
- **FR-009**: System MUST prevent duplicate unused OTPs in the pool.

### Key Entities

- **OTPPool**: Represents the pool of pre-generated passwords.
    - `password`: 8-digit string (unique among unused).
    - `is_used`: Boolean flag.
    - `created_at`: Timestamp.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Admin can reach the OTP Management Panel from the Dashboard in a single click.
- **SC-002**: Batch import of 500 OTPs via the UI completes in under 3 seconds.
- **SC-003**: 100% of invalid OTP formats (non-8-digit) are blocked during entry or upload.
- **SC-004**: Zero duplicate active OTPs are present in the pool after any management action.
