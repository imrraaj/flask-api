To run the server

```bash
flask --app src\main\app.py run --debug
```

Here's an overview of each feature:

1. **User Management:**

   - User Login: Authenticate users with their credentials.
   - User Registration: Allow new users to create accounts.
   - Change Password: Enable users to update their passwords.
   - Grant Admin Rights: Give administrative privileges to a user.
   - Revoke Admin Rights: Remove administrative privileges from a user.

2. **Admin Management:**

   - Admin Login: Allow administrators to access the admin dashboard.

3. **Product Management:**

   - Product Creation: Create new products with details like name, price, description, etc.
   - Product Update: Modify product details such as name, price, and description.
   - Product Get All: Retrieve a list of all products along with their information.

4. **Category Management:**

   - Category Creation: Create new product categories.
   - Category Get All: Retrieve a list of all product categories.

5. **Order Management:**

   - Order Creation: Allow users to place orders with multiple products and quantities.
   - Order Get for Specific User: Retrieve orders made by a specific user, along with order details.

6. **Reward Management:**
   - Reward Creation: Create new rewards with details like name, description, discount, and expiry date.
   - Reward Distribution: Distribute rewards to users based on specific conditions.
   - Mail for Rewards: Send email notifications to users upon receiving rewards.
   - Mail for Birthdays: Automatically send birthday discount rewards to users.

With these features, your API provides a complete solution for managing user accounts, products, categories, orders, and rewards. It allows users to interact with the platform, make purchases, and receive special offers such as discounts and rewards. The admin functionality ensures that administrators have the necessary tools to manage products, categories, and user privileges effectively.

This API offers a comprehensive and user-friendly experience for both customers and administrators, making it a versatile tool for an online shopping platform with advanced features and capabilities.
