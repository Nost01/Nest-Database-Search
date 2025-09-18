# Create a FastAPI instance
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
import mysql.connector
import bcrypt
import os
import uvicorn

frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/build")
app = FastAPI(title="Employee Search API", description="API for searching employee details in a database")
app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="static")

load_dotenv(dotenv_path="variables.env")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

class LoginRequest(BaseModel):
    password: str

@app.post("/login")
def login(data: LoginRequest):
    hashed_password = os.getenv("APP_PASSWORD_HASH").encode('utf-8')
    if bcrypt.checkpw(data.password.encode('utf-8'), hashed_password):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid password")
    
# Search Endpoint

@app.get("/search/1.0")
def smart_search(keyword: str = Query(..., description="Search keywords separated by spaces")):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    columns = [
        "FirstName", "LastName", "Department",
        "VehiclePlate", "VehicleDescription", "VehicleColour",
        "VehicleMake", "VehicleModel", "StallNumber", "PhoneNumber"
    ]

    field_map = {
        "firstname": "FirstName",
        "lastname": "LastName",
        "department": "Department",
        "vehicleplate": "VehiclePlate",
        "vehicledescription": "VehicleDescription",
        "vehiclecolour": "VehicleColour",
        "vehiclemake": "VehicleMake",
        "vehiclemodel": "VehicleModel",
        "stallnumber": "StallNumber",
        "phonenumber": "PhoneNumber"
    }

    keywords = keyword.strip().split()
    query = "SELECT * FROM Employees WHERE "
    query_parts = []
    params = []

    for kw in keywords:
        # Check for field=value pattern
        if "=" in kw:
            field, value = kw.split("=", 1)
            field = field.lower().replace(" ", "")
            value = value.strip()
            if field in field_map:
                col = field_map[field]
                if col in ["StallNumber"]:
                    query_parts.append(f"{col} = %s")
                    params.append(value)
                else:
                    query_parts.append(f"LOWER({col}) LIKE %s")
                    params.append(f"%{value.lower()}%")
                continue 

        sub_parts = [f"LOWER({col}) LIKE %s" for col in columns]
        query_parts.append("(" + " OR ".join(sub_parts) + ")")
        params.extend([f"%{kw.lower()}%"] * len(columns))

    query += " AND ".join(query_parts)

    cursor.execute(query, params)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"employees": results}
