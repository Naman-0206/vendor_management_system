# Vendor Management System with Performance Metrics

## Overview

This project implements a Vendor Management System with performance metrics using Django and Django REST Framework. The system allows users to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Naman-0206/vendor_management_system.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Navigate to the project directory

   ```bash
   cd vendor_management_system
   ```

4. Apply database migrations
   ```bash
   python manage.py makemigrations
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
