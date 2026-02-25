# API Contract: Loan Records Panel

## Endpoint: GET /assets/loan-records

Retrieve the most recent 200 loan activities (pickup and return history).

### Request
- **Method**: GET
- **Path**: `/assets/loan-records`
- **Auth**: None (Publicly accessible)

### Response (200 OK)
Returns a list of `LoanRecord` objects.

```json
[
  {
    "identifier": "京A88888",
    "type": "KEY",
    "user_name": "张三",
    "loan_time": "2026-02-25T08:00:00Z",
    "return_time": "2026-02-25T17:00:00Z"
  },
  {
    "identifier": "GAS-001",
    "type": "GAS_CARD",
    "user_name": "李四",
    "loan_time": "2026-02-25T09:30:00Z",
    "return_time": null
  }
]
```

### Response Model (Pydantic)
```python
class LoanRecord(BaseModel):
    identifier: str
    type: AssetType
    user_name: str
    loan_time: datetime
    return_time: Optional[datetime]
```
