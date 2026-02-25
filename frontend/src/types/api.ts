export interface Asset {
  id: string;
  type: string;
  identifier: string;
  status: string;
  maintenance_date?: string;
  maintenance_mileage?: number;
  inspection_date?: string;
  insurance_date?: string;
}

export interface VerifyResponse {
  success: boolean;
  user_id: string;
  message: string;
}

export interface PickupResponse {
  success: boolean;
  otp: string;
  assets: string[];
  expires_at: string;
}

export interface ReturnResponse {
  success: boolean;
  otp: string;
  message: string;
  expires_at: string;
}

export interface ActiveLoan {
  identifier: string;
  type: string;
  user: string;
  timestamp: string;
}

export interface LoanHistoryRecord {
  identifier: string;
  type: string;
  user_name: string;
  loan_time: string;
  return_time?: string;
}
