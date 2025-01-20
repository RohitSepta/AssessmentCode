# Dynamic Pricing & Discount System

This project provides an API for managing products, calculating dynamic prices based on quantity, and applying different discount strategies for seasonal and bulk products. The API supports standard CRUD operations and price calculations.

## Product Information 

### Features
- **Product List & Create**: View all products and create new products.
- **Product Detail**: Retrieve, update, or delete specific products.
- **Price Calculation**: Calculate the price of a product based on its quantity, applying any relevant discounts.
- **Seasonal Product**: Create products with seasonal discounts.
- **Bulk Product**: Create products with bulk purchase discounts.

## API Endpoints

### Product List & Create

- **GET** `product_info/products/`  
  Retrieves a list of all products.

- **POST** `product_info/products/`  
  Creates a new product.

- **GET** `product_info/products/<int:pk>/`
  Calculate price with quantity

#### Example Request for Creating a Product:
- **Request Body**:

```json
{
    "name": "Winter Jacket",
    "description": "Warm winter jacket",
    "base_price": "100.00",
    "product_type": "seasonal",
    "seasonal_details": {
        "season": "WINTER",
        "season_discount": "0.20",
        "off_season_discount": "0.05"
    }
}
