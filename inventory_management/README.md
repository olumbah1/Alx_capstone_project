# Inventory Management Project
The Inventory Management System is designed to help businesses efficiently manage and monitor their product inventory. It automates the tracking of stock levels, alerts when products are out of stock or below a predefined minimum threshold, and eliminates the need for manual stock counting. The system also tracks product inflow and outflow, supports detailed reporting, and organizes products into categories for easy identification, search, and filtering. Each product is assigned a unique ID along with metadata like name, quantity, creator, and creation date to ensure clear and organized inventory records.

Product Management – Add, update, delete, and view products with unique identifiers.

Stock Tracking – Automatically monitor product quantities, including in-flow and out-flow tracking.

Get Notify – Receive notifications for out-of-stock or low-inventory items.

Categorization – Group products by categories for easier filtering and searching.

Reports & Summaries – View inventory summaries, low-stock reports, and stock movement history.

# 🛠️ Tech Stack

Backend: Django / Django Rest Framework

Database: PostgreSQL / SQLite

Authentication: Token-based (DRF Token Auth)

API Docs: DRF Docs

# 📑 API Documentation

The API provides endpoints to manage users, products, categories, inventory movements, and reports. Documentation is generated using Swagger or DRF Docs for clear and testable references.

Endpoints:

GET /api/products/ – List all products
POST /api/products/ – Create a new product

GET /api/categories/<int:pk>/ - List all categories
POST /api/categories - Create a new Categories

GET /api/movements - List all movements
GET /api/movements/<int:pk>/ - Get all movements

GET /api/reports/summary/ – Get inventory summaries

GET  /sales/customers/           - List all customers
POST /sales/customers/           - Create new customer
GET  /sales/customers/1/         - Get customer details
PUT  /sales/customers/1/         - Update customer

GET  /sales/sales/               - List all sales
POST /sales/sales/create/        - Create new sale
GET  /sales/sales/1/             - Get sale details

📊 DASHBOARD:
GET  /sales/dashboard/           - Get sales statistics


# ⚙️ CI/CD Pipeline

CI/CD (Continuous Integration and Continuous Deployment) pipelines automate testing, building, and deploying the application with every code change. This improves code quality, reduces manual errors, and speeds up development. Tools like GitHub Actions can be used to run tests and deploy the app automatically. Docker may also be used to ensure consistent environments across development and production.

Register [POST]
link: http://127.0.0.1:8001/accounts/register/
{
"username":"John",
"email":"john@gmail.com",
"password":"john1234",
"password_confirm":"john1234"
}


login: [POST]
 http://127.0.0.1:8001/accounts/login/
{
    "username":"Peter",
    "password":"peter1234"
}

Authorization
token

products: [GET]
link: http://127.0.0.1:8001/products/


category:
link: http://127.0.0.1:8001/products/categories/


sales LIST [GET]
link: http://127.0.0.1:8001/sales/

Customers list [GET]
link: http://127.0.0.1:8001/customers/

customer Details [GET]
http://127.0.0.1:8001/customers/1/

Inventory List [GET]
link: http://127.0.0.1:8001/inventory/movements/

Summary [GET]
link: http://127.0.0.1:8001/inventory/summary/

Dashboard [GET]
link: http://127.0.0.1:8001/dashboard/
