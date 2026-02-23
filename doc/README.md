# Mergington High School API Documentation

A FastAPI application for managing extracurricular activities and products at Mergington High School.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup & Installation](#setup--installation)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Database](#database)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

## Overview

This is a web application built with **FastAPI** that allows students to view activities, sign up for extracurricular programs, and manage a product catalog. The application features:

- RESTful API endpoints
- SQLite database for persistent data storage
- Interactive web interface with HTML/CSS/JavaScript
- JSON request/response handling
- Pydantic data validation

## Features

✅ **Activities Management**
- View all available activities
- Sign up for activities with email validation
- Track activity participants

✅ **Products Catalog**
- View all products with detailed information
- Create new products via API
- Persistent product storage in SQLite database
- Browse products in a dedicated catalog page

✅ **Web Interface**
- Interactive HTML forms
- Real-time data updates
- Static file serving
- Responsive design with CSS styling

✅ **Database**
- SQLite database with automatic initialization
- Schema migration from JSON to SQLite
- Full CRUD operations support

## Setup & Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd md-getting-started-with-github-copilot
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   pip list
   ```

## Running the Server

### Start the FastAPI Server

```bash
python src/app.py
```

The server will start on `http://127.0.0.1:8001`

### Access the Application

- **Main Page:** http://127.0.0.1:8001/
- **Products Catalog:** http://127.0.0.1:8001/static/products.html
- **API Documentation (Swagger UI):** http://127.0.0.1:8001/docs
- **Alternative API Docs (ReDoc):** http://127.0.0.1:8001/redoc

## API Endpoints

### Activities Endpoints

**GET /activities**
- Retrieve all available activities
- Returns list of activities with details
- No parameters required

**POST /activities/{activity_name}/signup**
- Sign up a student for an activity
- Request body:
  ```json
  {
    "email": "student@example.com"
  }
  ```
- Response:
  ```json
  {
    "message": "Signed up student@example.com for Activity Name"
  }
  ```

### Products Endpoints

**GET /products**
- Retrieve all products from database
- Returns dictionary of products with IDs as keys
- No parameters required
- Cache-Control: no-cache (fresh data on each request)

**GET /products/{product_id}**
- Retrieve a specific product by ID
- Parameters:
  - `product_id` (string): Product ID
- Returns single product object
- Status 404 if product not found

**POST /products**
- Create a new product in database
- Request body:
  ```json
  {
    "name": "Product Name",
    "description": "Product description",
    "price": 29.99,
    "stock": 10
  }
  ```
- Response:
  ```json
  {
    "message": "Product created successfully",
    "product": {
      "id": "5",
      "name": "Product Name",
      "description": "Product description",
      "price": 29.99,
      "stock": 10
    }
  }
  ```

### Other Endpoints

**GET /**
- Redirects to main page (`/static/index.html`)

## Database

### SQLite Database

The application uses **SQLite** for persistent data storage.

**Database File:** `src/products.db`

### Products Table Schema

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);
```

### Database Operations

**Initialization**
- Database is automatically created on first run
- Table is created if it doesn't exist

**Data Migration**
- Initial JSON data (`products.json`) is migrated to SQLite on startup
- Migration only happens once (if table is empty)

**Viewing Database**

1. Install **SQLite Viewer** extension in VS Code
2. Right-click on `src/products.db`
3. Select "Open with SQLite Viewer"
4. Browse all products in table format

## Project Structure

```
md-getting-started-with-github-copilot/
├── src/
│   ├── app.py                 # Main FastAPI application
│   ├── database.py            # SQLite database functions
│   ├── products.json          # Initial product data (for migration)
│   ├── products.db            # SQLite database (auto-created)
│   ├── __pycache__/
│   └── static/
│       ├── index.html         # Main page with forms
│       ├── products.html      # Products catalog page
│       ├── app.js             # JavaScript for form handling
│       └── styles.css         # Application styling
├── doc/
│   └── README.md              # This documentation
├── .devcontainer/
│   └── devcontainer.json      # Codespaces configuration
├── requirements.txt           # Python dependencies
├── README.md                  # Main project README
└── pytest.ini                 # Python testing configuration
```

## Technologies Used

**Backend**
- **FastAPI** - Modern web framework for building APIs
- **Pydantic** - Data validation using Python type hints
- **Uvicorn** - ASGI server for running FastAPI
- **SQLite3** - Lightweight relational database

**Frontend**
- **HTML5** - Semantic markup
- **CSS3** - Styling and responsive design
- **JavaScript (ES6+)** - Client-side logic and API calls

**Development**
- **Python 3.10+** - Programming language
- **Pip** - Dependency management
- **GitHub Codespaces** - Cloud development environment

## API Testing

### Using cURL

```bash
# Get all products
curl http://127.0.0.1:8001/products

# Get specific product
curl http://127.0.0.1:8001/products/1

# Create a product
curl -X POST http://127.0.0.1:8001/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tablet",
    "description": "10-inch tablet for students",
    "price": 399.99,
    "stock": 20
  }'
```

### Using Postman

1. Import the API into Postman
2. Use the endpoints listed above
3. Set headers: `Content-Type: application/json`
4. For POST requests, use JSON request bodies

### Using FastAPI Interactive Docs

Visit `http://127.0.0.1:8001/docs` for interactive API documentation where you can test endpoints directly in the browser.

## Current Data

The database currently contains **5 products**:

| ID | Name | Price | Stock |
|----|------|-------|-------|
| 1 | Laptop | $899.99 | 15 |
| 2 | Notebook Set | $12.99 | 52 |
| 3 | Backpack | $49.99 | 25 |
| 4 | Calculator | $29.99 | 30 |
| 5 | Tech Books | $7.00 | 7 |

## Environment Variables

None required for basic setup. All configuration is hardcoded for development purposes.

## Troubleshooting

### Server won't start
- Ensure port 8001 is not in use
- Check Python version compatibility
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Products not saving
- Ensure `src/` directory has write permissions
- Check that `products.db` file exists
- Restart the server to ensure database is initialized

### Static files not loading
- Verify files exist in `src/static/` directory
- Check browser console for 404 errors
- Hard refresh the page (Ctrl+F5)

## Future Enhancements

- Add authentication/authorization
- Implement product search and filtering
- Add email notifications
- Create admin dashboard
- Add product images
- Implement pagination for large datasets
- Add API rate limiting
- Database backups and versioning

## Contact & Support

For issues or questions, please refer to the main README.md in the project root.
