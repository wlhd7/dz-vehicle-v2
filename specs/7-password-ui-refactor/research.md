# Research: Persistent Password UI

## Decision: Frontend Persistence
- **Choice**: `localStorage`
- **Rationale**: The requirement "Persistence Across Refresh" and "Current user session" is best served by `localStorage` for simple data like an OTP and its expiry. It survives page reloads and browser restarts.
- **Alternatives considered**: 
  - `sessionStorage`: Would be lost on tab close, which might not satisfy "Persistence Across Refresh" if the user reopens the tab.
  - Backend state: Overkill for this specific UI requirement, as the OTP is already provided in the operation response.

## Decision: Expiration Mechanism
- **Choice**: Frontend-only timer with `localStorage` fallback.
- **Rationale**: A `setInterval` in the main dashboard component can check the `expires_at` timestamp every minute. On mount, it checks if the saved password is still valid.
- **Alternatives considered**:
  - `setTimeout`: Risk of being cleared if the component unmounts or page reloads. `setInterval` is more robust for periodic checks.

## Decision: Visual Styling
- **Choice**: Custom CSS border with Element Plus variables.
- **Rationale**: Ensures consistency with the existing design system while meeting the "green border" requirement.
