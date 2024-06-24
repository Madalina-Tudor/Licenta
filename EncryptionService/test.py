from sqlalchemy import create_engine, inspect

# Source database URL
SOURCE_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/allPatientData"

# Create engine
source_engine = create_engine(SOURCE_DATABASE_URL)

# Inspect database
inspector = inspect(source_engine)

# Get table names
tables = inspector.get_table_names()
print("Tables in source database:", tables)
