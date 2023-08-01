## Reward Endpoints Documentation

This section provides documentation for the endpoints related to rewards in the online shopping store's reward system.

### View All Rewards [GET]

View all rewards associated with the authenticated user.

**Endpoint:** `/rewards/view/all`

**Authorization:** Requires a valid JWT token.

**Response (Success):**

```json
[
  {
    "name": "Birthday Discount",
    "description": "A gift for your birthday from us",
    "custom_code": "ABC12345",
    "expiry_date": "2023-07-31",
    "discount_percentage": 25.0,
    "status": "NOT_REDEEMED",
    "used_on": null
  },
  {
    "name": "Special Deal Discount",
    "description": "Special discount for loyal customers",
    "custom_code": "XYZ98765",
    "expiry_date": "2023-08-15",
    "discount_percentage": 15.0,
    "status": "REDEEMED",
    "used_on": "2023-07-05 09:30:00"
  }
]
```

### Send Birthday Discount [GET]

Send birthday discounts to users who have their birthdays today.

**Endpoint:** `/rewards/send-birthday-discount`

**Response (Success):**

```json
{}
```

These endpoints allow the management of rewards in the online shopping store. Users can view all their rewards, including their details like name, description, custom code, expiry date, discount percentage, status (redeemed or not), and the date when the reward was used (if redeemed). Users with the "ADMIN" role can send birthday discounts to users whose birthdays are today.
