# Quickstart: Chinese Localization and Typography

## Prerequisites
- Node.js environment
- Access to the `frontend` directory

## Setup Instructions

### 1. Install Dependencies
Install `vue-i18n` to handle the localization layer.
```bash
cd frontend
npm install vue-i18n@9
```

### 2. Implementation Steps
1. **Initialize I18n**: Create `src/i18n/index.ts` and define the `zh-cn` messages.
2. **Update Main**: Inject `i18n` into the Vue app instance in `src/main.ts`.
3. **Configure Element Plus**: Wrap `App.vue` content with `el-config-provider` and set the locale to `zh-cn`.
4. **Global Styles**: Update `src/style.css` with the new font stack and line-height adjustments.
5. **Component Migration**: Replace hardcoded English text in `.vue` files with `$t('key')` references.

## Verification
- Run `npm run dev` and navigate to the login page.
- Verify that the font is clean and legible (no "tofu" characters).
- Verify that all buttons and labels are in Chinese.
- Check browser console for missing translation warnings.
