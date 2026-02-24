export interface Asset {
  id: string;
  type: string;
  identifier: string;
  status: string;
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
}
