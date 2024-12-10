# Discount Management API
This project provides an API for managing discounts, user profiles, orders, and system logs. It is built with Django and Django REST Framework (DRF).

## Features
***User Profile Management:*** View and manage user profiles.<br>
***Cart Discount Calculation:*** Automatically calculate the best discounts for a user's cart.<br>
***Order History:*** Retrieve a user's order history.<br>
***System Logs:*** View actions performed in the system for audit and debugging purposes.<br>
***Order Management:*** Manage orders using a RESTful interface.<br>

## Usage

#### Clone the repository

```sh
git clone https://github.com/94R1K/cat_charity_fund.git
```

#### Go to the discount folder, install and run the virtual environment.

```sh
cd  discount
```

```
python -m venv venv
```

* If you are on Linux/MacOS

```
source venv/bin/activate
```

* If you are on windows

```
source venv/Scripts/activate
```
#### Install dependencies:

```
pip install -r requirements.txt
```
#### Run the apps on the local server
```
python manage.py runserver
```
## Swagger and Redoc Documentation
The API includes built-in documentation using Swagger and Redoc.<br>
 You can use the following endpoints to view the API specification:
 
```
GET /swagger.json
GET /swagger.yaml
```

```
GET /swagger/
```
Opens the Swagger UI, which allows you to test and view API endpoints.
```
GET /redoc/
```
Opens the Redoc user interface for easy reading of the API documentation.


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

