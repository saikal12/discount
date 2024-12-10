# Discount Management API
This project provides an API for managing discounts, user profiles, orders, and system logs. It is built with Django and Django REST Framework (DRF).

## Features
***User Profile Management:*** View and manage user profiles.<br>
***Cart Discount Calculation:*** Automatically calculate the best discounts for a user's cart.<br>
***Order History:*** Retrieve a user's order history.<br>
***System Logs:*** View actions performed in the system for audit and debugging purposes.<br>
***Order Management:*** Manage orders using a RESTful interface.<br>

## API Endpoints
### User Profile
GET /api/v1/users/{user_id}/<br>
Response:
```
{
    "user_id": "string",
    "email": "string",
    "created_at": "datetime",
    "orders_count": "integer",
    "total_spent": "decimal",
    "loyalty_status": "string",
    "tier": "string"
}
```
### Orders Management
GET /api/v1/orders/<br> Response:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "user_id": 0,
      "items": [
        {
          "product_text": "string",
          "quantity": 0,
          "price": "string"
        }
      ],
      "subtotal": "string",
      "discount_amount": "string",
      "final_amount": "string",
      "status": "pending"
    }
  ]
}
```
POST /api/v1/orders/ <br> Request:
```
{
  "user_id": 0,
  "items": [
    {
      "product_text": "string",
      "quantity": 0,
      "price": "string"
    }
  ],
}
```
<br> Response:
```
{
  "user_id": 0,
  "items": [
    {
      "product_text": "string",
      "quantity": 0,
      "price": "string"
    }
  ],
  "subtotal": "string",
  "discount_amount": "string",
  "final_amount": "string",
  "status": "pending"
}
```

GET /api/v1/orders/{order_id}/<br> Response:
```
{
  "user_id": 0,
  "items": [
    {
      "product_text": "string",
      "quantity": 0,
      "price": "string"
    }
  ],
  "subtotal": "string",
  "discount_amount": "string",
  "final_amount": "string",
  "status": "pending"
}
```
PUT /api/v1/orders/{order_id}/<br> Response:
```
{
  "user_id": 0,
  "items": [
    {
      "product_text": "string",
      "quantity": 0,
      "price": "string"
    }
  ],
  "subtotal": "string",
  "discount_amount": "string",
  "final_amount": "string",
  "status": "pending"
}
```
DELETE /api/v1/orders/{order_id}/ <br> Response:
``` Code	Description
204
```
### User Orders History
GET /api/v1/users/{user_id}/orders/<br> Response:

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "order_id": 0,
      "created_at": "2024-12-10T04:59:24.027Z",
      "subtotal": "string",
      "discount_amount": "string",
      "final_amount": "string"
    }
  ]
}
```
### Discount Calculation
POST /api/v1/cart/calculate-discount/ <br> Request:
```
{
    "user_id": "string",
    "items": [
        {
            "product_text": "string",
            "quantity": "integer",
            "price": "decimal"
} ]
}
```
<br> Response:
```
{
    "subtotal": "decimal",
    "discounts": [
        {
            "type": "string",
            "amount": "decimal"
} ],
    "total_discount": "decimal",
    "final_amount": "decimal"
}
```
### System Logs

GET /api/v1/logs/ <br> Response:
```
Query Parameters:
- user_id: string
- action_type: string
- from_date: datetime
- to_date: datetime
- page: integer
- limit: integer
```

```
{
"logs": [ {
            "log_id": "string",
            "user_id": "string",
            "action_type": "string",
            "details": "json",
            "created_at": "datetime"
} ],
    "total": "integer",
    "page": "integer"
}
```

