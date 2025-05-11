from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from routers import property_layer, brand, traffic
from database import get_db, engine
import logging
from sqlalchemy import text
from services.property_layer import PropertyLayerService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Use ORJSON for faster response serialization
app = FastAPI(
    title="Blackprint Backend API",
    description="FastAPI implementation of Blackprint Backend",
    version="1.0.0",
    default_response_class=ORJSONResponse
)

# Add GZip middleware to compress large responses
app.add_middleware(GZipMiddleware, minimum_size=9000)

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

property_layer_service = PropertyLayerService()

@app.on_event("startup")
def startup():
    logger.info("Attempting to connect to database...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database()")).scalar()
            logger.info(f"Connected to database: {result}")
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        logger.error("Application startup failed due to database connection error")
        raise

@app.on_event("shutdown")
def shutdown():
    logger.info("Closing database connection...")
    engine.dispose()
    logger.info("Database connection closed")

@app.on_event("startup")
def load_property_data():
    print("Loading property data at startup...")
    from database import SessionLocal
    db = SessionLocal()
    try:
        data = property_layer_service.get_properties_layer_data(db)
        app.state.property_data_cache = data
        print(f"Loaded {len(data)} properties into cache.")
    finally:
        db.close()
