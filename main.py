from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routers import property_layer, brand, traffic
from database import get_db, engine
import logging
from sqlalchemy import text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Blackprint Backend API",
    description="FastAPI implementation of Blackprint Backend",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(property_layer.router, prefix="/api/v1", tags=["Property Layer"])
app.include_router(brand.router, prefix="/api/v1", tags=["Brand"])
app.include_router(traffic.router, prefix="/api/v1", tags=["Traffic"])

@app.on_event("startup")
def startup():
    # Log database connection attempt
    logger.info("Attempting to connect to database...")
    try:
        # Test database connection with a simple query that works on Redshift
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database()")).scalar()
            logger.info(f"Connected to database: {result}")
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        # Don't raise HTTPException here as it's not a request context
        logger.error("Application startup failed due to database connection error")
        raise

@app.on_event("shutdown")
def shutdown():
    # Close the engine
    logger.info("Closing database connection...")
    engine.dispose()
    logger.info("Database connection closed") 