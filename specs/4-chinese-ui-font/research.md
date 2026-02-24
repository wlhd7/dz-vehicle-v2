# Research: Chinese UI Font and Localization

## Decision: Standard Font Stack
**Rationale**: Using a standard system font stack avoids the overhead of downloading web fonts while ensuring a high-quality display on all major operating systems.
**Stack**: `system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", "Source Han Sans SC", sans-serif`
- **iOS/macOS**: PingFang SC (Apple standard)
- **Windows**: Microsoft YaHei (Microsoft standard)
- **Linux/Generic**: Source Han Sans SC (Adobe/Google standard)

## Decision: Vue I18n Integration
**Rationale**: Although the user requested a permanent migration to Chinese, using `vue-i18n` is the industry standard for managing translations. It provides a structured way to extract strings from components and allows for future expansion if English needs to be restored.
**Alternatives considered**:
- **Hardcoded Strings**: Simple but difficult to maintain and audit.
- **Custom Translation Service**: Over-engineering when `vue-i18n` exists.

## Decision: Element Plus Localization
**Rationale**: Element Plus provides built-in localization for its components (date pickers, pagination, messages). We will use its `config-provider` to set the locale to Chinese (`zh-cn`).

## Decision: CSS-based Typography Adjustments
**Rationale**: Chinese characters often require more vertical space and slightly different letter spacing than Latin characters to remain legible. We will apply global CSS adjustments to `line-height` and `letter-spacing`.
