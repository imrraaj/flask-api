# Database Schema Documentation

This document provides an overview of the database schema for the online shopping store's reward system. The schema is implemented using Flask-SQLAlchemy, a powerful ORM tool for managing databases in Flask applications.

## User Model

The `User` model represents the users of the online shopping store. It stores information such as the user's name, username, password, email, avatar, birth date, and role. Each user can have multiple rewards associated with them.

| Column     | Type         | Description                            |
| ---------- | ------------ | -------------------------------------- |
| id         | Integer (PK) | Unique identifier for the user.        |
| name       | String(50)   | User's full name.                      |
| username   | String(20)   | Unique username for the user.          |
| password   | String(200)  | Encrypted password for the user.       |
| email      | String(80)   | Unique email address of the user.      |
| avatar     | String(100)  | URL to the user's avatar image.        |
| birth_date | Date         | User's birth date (optional).          |
| role       | Enum         | Role of the user (ADMIN, USER, GUEST). |
| created_at | DateTime     | Timestamp of user registration.        |

## Product Model

The `Product` model represents the products available in the online shopping store. It stores information such as the product's name, price, description, category, and images associated with the product.

| Column      | Type         | Description                             |
| ----------- | ------------ | --------------------------------------- |
| id          | Integer (PK) | Unique identifier for the product.      |
| name        | String(200)  | Name of the product.                    |
| price       | Float        | Price of the product.                   |
| description | Text         | Description of the product (optional).  |
| category_id | Integer (FK) | Foreign key referencing Category model. |

## ProductImage Model

The `ProductImage` model represents the images associated with each product. It stores information about the image URL and the product it belongs to.

| Column     | Type         | Description                            |
| ---------- | ------------ | -------------------------------------- |
| id         | Integer (PK) | Unique identifier for the image.       |
| url        | String(100)  | URL to the product image.              |
| product_id | Integer (FK) | Foreign key referencing Product model. |

## Category Model

The `Category` model represents the categories to which products belong. Each product can be associated with only one category.

| Column | Type         | Description                         |
| ------ | ------------ | ----------------------------------- |
| id     | Integer (PK) | Unique identifier for the category. |
| name   | String(100)  | Name of the category.               |

## Order Model

The `Order` model represents the orders placed by users. It stores information about the user who placed the order, the order date, total amount, status, and order details.

| Column       | Type         | Description                                               |
| ------------ | ------------ | --------------------------------------------------------- |
| id           | Integer (PK) | Unique identifier for the order.                          |
| user_id      | Integer (FK) | Foreign key referencing User model.                       |
| order_date   | DateTime     | Timestamp of the order placement.                         |
| total_amount | Float        | Total amount of the order.                                |
| status       | Enum         | Status of the order (ORDERED, CANCELLED, PAID, DELIVERY). |

## OrderDetail Model

The `OrderDetail` model represents the details of each order. It stores information about the product ordered, the quantity, and the price at the time of ordering.

| Column     | Type         | Description                                |
| ---------- | ------------ | ------------------------------------------ |
| id         | Integer (PK) | Unique identifier for the order detail.    |
| order_id   | Integer (FK) | Foreign key referencing Order model.       |
| product_id | Integer (FK) | Foreign key referencing Product model.     |
| quantity   | Integer      | Quantity of the product ordered.           |
| price      | Float        | Price of the product at the time of order. |

## Reward Model

The `Reward` model represents the reward types available for users. It stores information about the reward's name, description, discount percentage, expiry date, custom code, user ID, and status.

| Column              | Type         | Description                                             |
| ------------------- | ------------ | ------------------------------------------------------- |
| id                  | Integer (PK) | Unique identifier for the reward.                       |
| name                | String(100)  | Name of the reward.                                     |
| description         | Text         | Description of the reward (optional).                   |
| discount_percentage | Float        | Discount percentage for the reward.                     |
| expiry_date         | Date         | Expiry date of the reward.                              |
| custom_code         | String(8)    | Custom 8-digit code for the reward.                     |
| user_id             | Integer (FK) | Foreign key referencing User model.                     |
| status              | Enum         | Status of the reward (NOT_REDEEMED, REDEEMED, EXPIRED). |

The database schema is designed to handle the core functionalities of the reward system efficiently. The relationships between models allow easy retrieval and management of user data, product details, and reward information. The use of enumerations (enums) for roles, order status, reward status, and reward types ensures data consistency and integrity.
