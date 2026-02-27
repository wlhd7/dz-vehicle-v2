# Quickstart: Admin OTP Management Panel

## Setup
1. Define the designated administrator name.
2. Add `VITE_OTP_ADMIN_NAME="管理员名字"` to your `docker/env.production` or local development environment.
3. Start the application:
   ```bash
   # Backend
   python main.py
   
   # Frontend
   npm run dev
   ```

## Development Workflow
1. Log in as the designated administrator.
2. Observe the "OTP管理" link in the Dashboard header (next to Logout).
3. Access the link to navigate to the OTP Panel.
4. Verify functionality:
   - "剩余可用 OTP" count updates correctly.
   - "添加单笔" field rejects non-8-digit input.
   - "批量上传" rejects files with invalid formats (e.g., 7-digit OTPs).

## Verification
- Run backend tests: `pytest tests/test_admin_otp.py`
- Run frontend tests: `npm test OTPManagement.spec.ts`
