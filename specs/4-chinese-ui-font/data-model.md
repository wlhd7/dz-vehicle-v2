# Data Model: UI Localization

## Entities

### 1. Localization Message (I18n Store)
Represents the key-value mapping for UI strings.

| Field | Type | Description |
| :--- | :--- | :--- |
| `key` | String | Unique dot-notated identifier (e.g., `login.title`) |
| `value` | String | The Chinese translation string |

### 2. Configuration State
Represents the global UI configuration.

| Field | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| `locale` | Enum | Current application language | `zh-cn` |
| `fontFamily` | String | CSS font stack | `system-ui, ...` |

## Validation Rules
- All user-facing strings MUST have a corresponding key in the `zh-cn` locale file.
- Keys must follow a hierarchical naming convention (e.g., `view.component.element`).
- Placeholders in strings (e.g., `{name}`) must be preserved in translations.
