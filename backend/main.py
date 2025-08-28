# Create a FastAPI instance
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import mysql.connector
import os
import uvicorn

load_dotenv("variables.env")
app = FastAPI(title="Employee Search API", description="API for searching employee details in a database")

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

@app.get("/health")
def health_check():
    try: 
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return {"status": "healthy", "db": "connected"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

        
    
# Search Endpoints

@app.get("/search/all")
def search_all(keyword: str = Query(..., description="Search keyword")):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT * FROM Employees
        WHERE LOWER(FirstName) LIKE %s
        OR LOWER(LastName) LIKE %s
        OR LOWER(Department) LIKE %s
        OR LOWER(VehiclePlate) LIKE %s
        OR LOWER(VehicleDescription) LIKE %s
        OR LOWER(VehicleColour) LIKE %s
        OR LOWER(VehicleMake) LIKE %s
        OR LOWER(VehicleModel) LIKE %s
        OR LOWER(StallNumber) LIKE %s
    """

    kw = f"%{keyword.lower()}%"
    params = [kw] * 9

    cursor.execute(query, params)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"employees": results}

@app.get("/search")

def search_employees(
    FirstName: str | None = Query(None, description="Search by First Name"),
    LastName: str | None = Query(None, description="Search by Last Name"),
    Department: str | None = Query(None, description="Search by Department"),
    VehiclePlate: str | None = Query(None, description="Search by Vehicle Plate"),
    VehicleDescription: str | None = Query(None, description="Search by Vehicle Description"),
    VehicleColour: str | None = Query(None, description="Search by Vehicle Colour"),
    VehicleMake: str | None = Query(None, description="Search by Vehicle Make"),
    VehicleModel: str | None = Query(None, description="Search by Vehicle Model"),
    StallNumber: str | None = Query(None, description="Search by Stall Number"),
    NumberOfVehicles: int | None = Query(None, description="Search by Number of Vehicles")
):
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Base Queries
    query = "SELECT * FROM Employees WHERE 1=1"
    params = []

    # Filters based on provided parameters
    if FirstName:
        query += " AND LOWER(FirstName) LIKE %s"
        params.append(f"%{FirstName.strip().lower()}%")
    if LastName:
        query += " AND LOWER(LastName) LIKE %s"
        params.append(f"%{LastName.strip().lower()}%")
    if Department:
        query += " AND LOWER(Department) LIKE %s"
        params.append(f"%{Department.strip().lower()}%")
    if VehiclePlate:
        query += " AND LOWER(VehiclePlate) LIKE %s"
        params.append(f"%{VehiclePlate.strip().lower()}%")
    if VehicleDescription:
        query += " AND LOWER(VehicleDescription) LIKE %s"
        params.append(f"%{VehicleDescription.strip().lower()}%")
    if VehicleColour:
        query += " AND LOWER(VehicleColour) LIKE %s"
        params.append(f"%{VehicleColour.strip().lower()}%")
    if VehicleMake:
        query += " AND LOWER(VehicleMake) LIKE %s"
        params.append(f"%{VehicleMake.strip().lower()}%")
    if VehicleModel:
        query += " AND LOWER(VehicleModel) LIKE %s"
        params.append(f"%{VehicleModel.strip().lower()}%")
    if StallNumber:
        query += " AND LOWER(StallNumber) LIKE %s"
        params.append(f"%{StallNumber.strip().lower()}%")
    if NumberOfVehicles is not None:
        query += " AND NumberOfVehicles = %s"
        params.append(NumberOfVehicles)

    cursor.execute(query, params)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"employees": results}