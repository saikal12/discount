### Schema Design Documentation

### Entities and Their Purposes

**Users**:
Purpose: Represents the primary user entity for 
authentication, email verification, and account management.
-Fields:
"id": " Unique identifier for each user.",
"username": " User’s chosen display name.",
"email": "User’s email address.",
"password": "User’s password for authentication."
"is_email_verified" : "Indicates whether the user’s email address has been verified.",

**Profile**:
   - Purpose:  Dynamically calculate and store user-related
    metrics such as the number of orders, total spending, loyalty discounts, and tiers.
   - Fields:
    "user": " Foreign key linking to `Users`.",
    "orders_count": "counts user orders",
    "get_loyalty_discount": "get ",
    "loyalty_status": "decimal",
    "tier": "string",

**Order**:
 - Purpose:  Represent individual user transactions.
 - Fields: 
 "user_id" : "Foreign key linking to `Users`.",
 "subtotal": "price before discounts",
 "status": "status of order",
 "discount_amount": "amount of discount ",
 "final_amount":"amount after discount",
 "created_date": "created date of order"
 
**OrderItem**:

Purpose: Represent individual items in an order.
 - Fields: 
"order_id" = "Foreign key linking to `Order`.",
"product_text" = "product name",
"quantity" = "quantity  of product",
"price" = "price of product"

**DiscountRule**:

Purpose: Define configurable rules for applying discounts to orders.
 - Fields: 
"description": "description for discount rules",
"discount_type": "The type of discount, either percentage or fixed amount.",
"maximum_discount": "The upper limit for the discount.",
"discount_value" : "discount value",
"min_order_value": The minimum order value required to apply the discount.


**LoyaltyDiscount**:

Purpose: Define loyalty levels and associated discounts based on the number of orders.
 - Fields: 
"level_name" = "Name of the loyalty level".
"min_order" = "Range of orders needed to qualify for the level",
"max_order" = " Range of orders needed to qualify for the level",
"discount_percentage" = "Percentage discount associated with the level"

**SystemLog**:

Purpose: Record user actions (e.g., login, logout, create, update, delete) for auditing and troubleshooting.
 - Fields: 
"user_id" = "Foreign key linking to `Users`.",
"action_type": "Specifies the type of user action.",
"details": "JSON data with relevant information about the action."

### Relationships Between Entities
**User & Profile**
Type: One-to-One.
Purpose: Each user has a single profile.

**User & Order**
Type: One-to-Many.
Purpose: A user can place multiple orders.

**Order & OrderItem**
Type: One-to-Many.
Purpose: Each order can contain multiple items.

**User & SystemLog**
Type: One-to-Many.
Purpose: Each user can have multiple log entries for their activities.

**LoyaltyDiscount & Profile**
Type: Logical association.
Purpose: The user's loyalty status is dynamically calculated based on their order count.


### Explain Chosen Data Types
**CharField (String Fields):**
status, discount_type, level_name, product_text: Used to store short strings or enumerations (e.g., status could be pending, completed).

**IntegerField:**
quantity: To store integer values for the quantity of items.

**DecimalField:**
subtotal, discount_amount, final_amount, price: Used to store fixed-point numbers for financial values with high precision. Set to max_digits=10, decimal_places=2 to ensure that values are stored with up to two decimal places.

**DateTimeField:**
created_date, created_at: To store timestamps of when the records were created.

**ForeignKey:**
user_id: To associate Order, OrderItem, and SystemLog models with the User model.

**JSONField:**
details: Allows flexible storage of non-relational data (e.g., system log details, dynamic data for actions).

**IntegerField (min_order, max_order):**
For loyalty discount tiers, min_order and max_order store the boundaries for the number of orders.