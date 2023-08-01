## Product Endpoints Documentation

This section provides documentation for the endpoints related to products in the online shopping store's reward system.

### View All Products [GET]

View all products along with their images and category details.

**Endpoint:** `/products/view/all`

**Response (Success):**

```json
[
  {
    "id": 1,
    "name": "Product 1",
    "price": 1000.0,
    "description": "This is product 1",
    "category_id": 1,
    "images": [
      {
        "image_url": "image_url_1",
        "product_id": 1
      },
      {
        "image_url": "image_url_2",
        "product_id": 1
      }
    ]
  },
  {
    "id": 2,
    "name": "Product 2",
    "price": 500.0,
    "description": "This is product 2",
    "category_id": 2,
    "images": [
      {
        "image_url": "image_url_3",
        "product_id": 2
      }
    ]
  }
]
```

### View a Single Product [GET]

View details of a specific product by its ID.

**Endpoint:** `/products/view/<int:product_id>`

**Response (Success):**

```json
{
  "id": 1,
  "name": "Product 1",
  "price": 1000.0,
  "description": "This is product 1",
  "category_id": 1,
  "image": [
    {
      "image_url": "image_url_1",
      "product_id": 1
    },
    {
      "image_url": "image_url_2",
      "product_id": 1
    }
  ]
}
```

### Create a Product [POST]

Create a new product in the system.

**Endpoint:** `/products/add`

**Authorization:** Requires a valid JWT token with the "ADMIN" role.

**Request Payload:**

```json
{
  "name": "New Product",
  "price": 1500.0,
  "description": "This is the description of the new product",
  "category": "Electronics",
  "images": ["image_url_1", "image_url_2"]
}
```

| Field       | Type   | Description                             |
| ----------- | ------ | --------------------------------------- |
| name        | String | Name of the new product.                |
| price       | Number | Price of the new product.               |
| description | String | Description of the new product.         |
| category    | String | Category of the new product.            |
| images      | Array  | An array of image URLs for the product. |

**Response (Success):**

```json
{
  "status": true
}
```

### Update a Product [PUT]

Update details of a specific product by its ID. Only users with the "ADMIN" role can access this endpoint.

**Endpoint:** `/products/edit/<int:product_id>`

**Authorization:** Requires a valid JWT token with the "ADMIN" role.

**Request Payload:**

```json
{
  "name": "Updated Product Name",
  "price": 2000.0,
  "description": "Updated description of the product",
  "category": "Home & Kitchen",
  "images": ["updated_image_url_1", "updated_image_url_2"]
}
```

**Response (Success):**

```json
{
  "status": true
}
```

These endpoints allow the management of products in the online shopping store. Users with the "ADMIN" role can create new products, view all products, view a specific product, and update the details of a product. The responses include information about the product, its images, and its category.
