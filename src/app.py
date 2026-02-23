"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
import os
import json
from pathlib import Path
from database import init_database, migrate_json_to_db, get_all_products, get_product, create_product, get_next_product_id

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Request models for JSON payloads
class SignupRequest(BaseModel):
    email: str

class ProductRequest(BaseModel):
    name: str
    description: str
    price: float
    stock: int

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}

# Load products from JSON file
# Load products from database
init_database()
migrate_json_to_db()

products = get_all_products()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, request: SignupRequest):
    """Sign up a student for an activity with JSON payload"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(request.email)
    return {"message": f"Signed up {request.email} for {activity_name}"}


@app.get("/products")
def get_products_endpoint():
    """Get all products"""
    all_products = get_all_products()
    return JSONResponse(content=all_products, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


@app.get("/products/{product_id}")
def get_product_endpoint(product_id: str):
    """Get a specific product by ID"""
    product = get_product(int(product_id))
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return JSONResponse(content=product, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})


@app.post("/products")
def create_product_endpoint(request: ProductRequest):
    """Create a new product with JSON payload"""
    print(f"DEBUG: Received POST request for /products")
    print(f"DEBUG: Request data: {request}")
    
    # Create product in database
    product_id = create_product(request.name, request.description, request.price, request.stock)
    
    # Get the created product
    new_product = get_product(product_id)
    
    print(f"DEBUG: Product created with ID {product_id}")
    
    return {"message": "Product created successfully", "product": new_product}


# Mount the static files directory AFTER all routes
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


if __name__ == "__main__":
    import uvicorn
    # When running this file directly (`python src/app.py`) we cannot
    # reliably use the import-string form required for `reload=True`.
    # Use `reload=False` here so the file can be run directly.
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=False)
