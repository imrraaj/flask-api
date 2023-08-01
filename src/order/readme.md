## Order Endpoints Documentation

This section provides documentation for the endpoints related to orders in the online shopping store's reward system.

### Create Order [POST]

Create a new order in the system.

**Endpoint:** `/orders/create`

**Authorization:** Requires a valid JWT token.

**Request Payload:**

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 1
    }
  ],
  "reward_code": "REWARD8N"
}
```

| Field       | Type   | Description                             |
| ----------- | ------ | --------------------------------------- |
| items       | Array  | An array of product IDs and quantities. |
| reward_code | String | An optional 8-digit custom reward code. |

**Response (Success):**

```json
{
  "status": true,
  "total_amount": 1500.0,
  "reward": true,
  "reward_code": "REWARD8N",
  "net_payable_amount": 1350.0
}
```

**Response (Failure):**

```json
{
  "status": false,
  "error": "Product id: 1 doesn't exist"
}
```

### View All Orders [GET]

View all orders placed by the authenticated user.

**Endpoint:** `/orders/view/all`

**Authorization:** Requires a valid JWT token.

**Response (Success):**

```json
{
  "status": true,
  "orders": [
    {
      "id": 1,
      "order_date": "2023-07-10 15:30:00",
      "total_amount": 1500.0,
      "order_status": "ORDERED",
      "order_details": [
        {
          "product_id": 1,
          "quantity": 2,
          "price": 1000.0
        },
        {
          "product_id": 3,
          "quantity": 1,
          "price": 500.0
        }
      ]
    },
    {
      "id": 2,
      "order_date": "2023-07-10 16:45:00",
      "total_amount": 750.0,
      "order_status": "PAID",
      "order_details": [
        {
          "product_id": 2,
          "quantity": 3,
          "price": 750.0
        }
      ]
    }
  ]
}
```

### Change Order Status [GET]

Change the status of a specific order by its ID. Only users with the "ADMIN" role can access this endpoint.

**Endpoint:** `/orders/status/<int:id>`

**Authorization:** Requires a valid JWT token with the "ADMIN" role.

**Response (Success):**

```json
{
  "status": true
}
```

**Response (Failure):**

```json
{
  "status": false,
  "Message": "Order does not exist"
}
```

These endpoints enable the creation and management of orders in the online shopping store, including applying reward codes and viewing order details. The system also allows users with the "ADMIN" role to change the order status.
