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

## Discount Information 

### Features
- **Discount List & Create**: View all Discount and create new Discount.
- **Discount Detail**: Retrieve, update, or delete specific Discount.
- **Price Calculation**: Calculate the price of a product based on its quantity, applying any relevant discounts.
- **Seasonal Discount**: Create Discounts with seasonal discounts.
- **Bulk Discount**: Create Discounts with bulk purchase discounts.

## API Endpoints

### Discount List & Create

- **GET** `discount_info/discounts/`  
  Retrieves a list of all discounts.

- **POST** `discount_info/discounts/`  
  Creates a new product.

- **GET** `discount_info/discounts/<int:pk>/`
  Calculate price with quantity

#### Example Request for Creating a Discount:
- **Request Body**:

```json
{
    "name": "Summer Sale",
    "description": "20% off on all items",
    "discount_type": "percentage",
    "start_date": "2025-06-01T00:00:00Z",
    "end_date": "2025-08-31T23:59:59Z",
    "percentage_discount": {
        "percentage": 20.00,
        "min_purchase_amount": 50.00
    }
}