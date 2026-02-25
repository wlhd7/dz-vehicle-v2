# Quickstart: Persistent Password UI

## Project Overview
Refactor the temporary password display to be a persistent, embedded UI element instead of a popup, with a 2-hour expiration timer.

## Verification Steps

### Pickup Flow
1. Select an asset and click "Pickup Selected".
2. **Verify**: No dialog pops up.
3. **Verify**: A new section appears below the dashboard title with "领取密码：xxxx" inside a green border.
4. Refresh the page.
5. **Verify**: The password remains visible.

### Return Flow
1. Click "Return Assets".
2. **Verify**: No alert/dialog pops up.
3. **Verify**: The section below the title updates to "归还密码：yyyy" inside a green border.
4. Wait 2 hours (or mock the clock).
5. **Verify**: The section disappears automatically.

### Manual Verification
- Logout and log back in: The password should be cleared (session-based logic).
- Close the browser and reopen: The password should persist (localStorage logic).

## Resilience Verification
1. Open the dashboard with an active password displayed.
2. Toggle "Offline" mode in browser DevTools.
3. Toggle "Online" mode or switch networks.
4. **Verify**: The password remains visible and the green border is intact without requiring a manual page refresh.

## Technical Implementation Details
- **Component**: `frontend/src/views/Dashboard.vue`
- **State Key**: `active_otp` in `localStorage`
- **Timer Frequency**: 60 seconds (check `expiresAt < now`).
