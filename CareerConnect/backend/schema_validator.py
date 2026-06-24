import logging
import sys
from sqlalchemy import inspect
import models
from database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_schema():
    logger.info("Validating database schema...")
    inspector = inspect(engine)
    
    missing_columns = []
    
    for table_name in models.Base.metadata.tables.keys():
        if not inspector.has_table(table_name):
            logger.warning(f"Table '{table_name}' does not exist in the database.")
            continue
            
        db_columns = {col['name'] for col in inspector.get_columns(table_name)}
        model_columns = {col.name for col in models.Base.metadata.tables[table_name].columns}
        
        diff = model_columns - db_columns
        if diff:
            for col in diff:
                missing_columns.append((table_name, col))
                logger.error(f"Missing column in DB: {table_name}.{col}")
    
    if missing_columns:
        logger.error("\n*** SCHEMA MISMATCH DETECTED ***")
        logger.error("The SQLAlchemy models do not match the PostgreSQL database.")
        logger.error("Please run the provided Alembic migrations or the raw SQL script.")
        logger.error("Suggested ALTER statements:")
        for table, col in missing_columns:
            logger.error(f"  ALTER TABLE {table} ADD COLUMN {col} <type>;")
        logger.error("Application startup aborted to prevent implicit crashing.")
        sys.exit(1)
        
    logger.info("Database schema validation passed successfully.")
