# Vendor Management System with Performance Metrics

## Overview

This project implements a Vendor Management System with performance metrics using Django and Django REST Framework. The system allows users to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

This project is deployed at `https://vms.pythonanywhere.com/`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Naman-0206/vendor_management_system.git
   ```
2. Navigate to the project directory

   ```bash
   cd vendor_management_system
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Navigate to the project root directory

   ```bash
   cd vendor_management_system
   ```

5. Apply database migrations
   ```bash
   python manage.py migrate
   ```

## How to Run the Project

Start the server using `python manage.py runserver`.
Access the application at `http://localhost:8000`

## How to Test the Project

1. Run the test suite:
   ```bash
   python manage.py test
   ```
2. Alternatively, you can run tests for specific apps:
   ```bash
   python manage.py test vendors
   python manage.py test purchase_orders
   python manage.py test auth
   ```

## API Documentation

- API schema: `/api/schema/`
- Swagger UI: `/api/schema/swagger-ui/`
- ReDoc: `/api/schema/redoc/`

You can use these endpoints to view the API documentation in different formats.

Comprehensive API documentation with live testing is available at the following endpoints:

- [Swagger UI](https://vms.pythonanywhere.com/api/schema/swagger-ui/#/)
- [ReDoc](https://vms.pythonanywhere.com/api/schema/redoc/)
- [Download Schema](https://vms.pythonanywhere.com/api/schema/)

These endpoints provide detailed information about all API endpoints, request parameters, and responses.

## API Guide

### Endpoints

#### Vendor Profile Management:

- `POST /api/vendors/` Create a new vendor.
- `GET /api/vendors/` List all vendors.
- `GET /api/vendors/{vendor_id}/` Retrieve a specific vendor's details.
- `PUT /api/vendors/{vendor_id}/` Update a vendor's details.
- `DELETE /api/vendors/{vendor_id}/` Delete a vendor.

#### Purchase Order Tracking:

- `POST /api/purchase_orders/` Create a purchase order.
- `GET /api/purchase_orders/` List all purchase orders with an option to filter by vendor.
- `GET /api/purchase_orders/{po_id}/` Retrieve details of a specific purchase order.
- `PUT /api/purchase_orders/{po_id}/` Update a purchase order.
- `DELETE /api/purchase_orders/{po_id}/` Delete a purchase order.

#### Vendor Performance Evaluation:

- `GET /api/vendors/{vendor_id}/performance/` Retrieve a vendor's performance metrics.

#### Additional Endpoints:

- `POST /api/purchase_orders/{po_id}/acknowledge/` Acknowledge a purchase order.

#### User Authentication:

- `POST /api/token/`: Obtain authentication token.
- `POST /api/register/`: Register a new user.

### API Authentication

All API endpoints are protected and require authentication using a token. Follow these steps to authenticate:

#### Register a new user:

`POST /api/register/`
This endpoint creates a new user. Provide a username and password in the request body.

Obtain an authentication token:
`POST /api/token/`
Use the credentials of the registered user to obtain an authentication token. Provide the username and password in the request body. This endpoint will return a token.

Use the token for accessing protected endpoints:
Include the obtained token in the Authorization header of subsequent requests. The header should be in the format:
`Authorization: Token <your-token>`

With the authentication token, you can access all protected endpoints by including the token in the request header.

### Deployment

The project is deployed at https://vms.pythonanywhere.com/. If the site is not working, try reloading it once.
