# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# import json
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load app.json configuration
# try:
#     with open('app.json', 'r') as f:
#         config = json.load(f)
# except Exception as e:
#     logger.error(f"Error loading app.json: {e}")
#     config = {}

# # Get Redshift database credentials from app.json
# DB_USER = config.get("AWS_USERNAME", "admin_user")
# DB_PASSWORD = config.get("AWS_PASSWORD", "dee0jsdeERSpO5658sfiejde#asnf$?")
# DB_HOST = config.get("AWS_HOST", "blackprint-cluster-prd.czdk80krdpeg.us-west-1.redshift.amazonaws.com")
# DB_PORT = config.get("AWS_PORT", "5439")
# DB_NAME = config.get("AWS_REDSHIFT_DATABASE", "blackprint_db_prd")

# # Construct Redshift database URL
# DATABASE_URL = f"redshift+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# # Create SQLAlchemy Engine for Redshift
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"sslmode": "require"},  # Required for secure connection
#     pool_size=5,
#     max_overflow=10,
#     pool_timeout=30,
#     pool_recycle=1800
# )

# # Create session factory
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Create base class for declarative models
# Base = declarative_base()

# def get_db():
#     """
#     Dependency function to get a database session.
#     Yields a session and ensures it's closed after use.
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#         logger.info("Database session closed")


from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load app.json configuration
try:
    with open("app.json", "r") as f:
        config = json.load(f)
except Exception as e:
    logger.error(f"Error loading app.json: {e}")
    config = {}

# Get Redshift database credentials from app.json
DB_USER = config.get("AWS_USERNAME", "admin_user")
DB_PASSWORD = config.get("AWS_PASSWORD", "dee0jsdeERSpO5658sfiejde#asnf$?")
DB_HOST = config.get(
    "AWS_HOST", "blackprint-cluster-prd.czdk80krdpeg.us-west-1.redshift.amazonaws.com"
)
DB_PORT = config.get("AWS_PORT", "5439")
DB_NAME = config.get("AWS_REDSHIFT_DATABASE", "blackprint_db_prd")

# Construct Redshift database URL
DATABASE_URL = f"redshift+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy Engine for Redshift
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},  # Required for secure connection
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency function to get a database session.
    Yields a session and ensures it's closed after use.
    Also sets the correct schema for queries.
    """
    db = SessionLocal()
    try:
        # Set the correct schema (presentation)
        db.execute(text("SET search_path TO presentation"))
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()
        logger.info("Database session closed")
