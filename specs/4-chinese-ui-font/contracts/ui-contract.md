# UI Contract: Localization and Typography

## Typography Contract
The application UI must adhere to the following CSS properties for Chinese rendering:

- **Font Family**: `system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", "Source Han Sans SC", sans-serif`
- **Base Line Height**: `1.5` (Increased from 1.2 to accommodate character height)
- **Base Font Size**: `14px` for body, `16px` for interactive elements.

## Localization Contract (I18n Structure)
Translations will be structured in a JSON format compatible with `vue-i18n`.

### Structure Example
```json
{
  "common": {
    "confirm": "确认",
    "cancel": "取消",
    "save": "保存"
  },
  "login": {
    "title": "车辆资产领取系统",
    "username": "姓名",
    "idDigits": "身份证后四位",
    "submit": "验证身份"
  }
}
```

## Component Contract (Element Plus)
- All Element Plus components must be wrapped in `<el-config-provider :locale="zhCn">`.
```
