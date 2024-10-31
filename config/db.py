from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker,joinedload

# Define the MySQL connection URL (replace with your actual credentials)
DATABASE_URL = "mysql+pymysql://root:Beibei202307!@localhost:3306/Veggie"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Base class for models
Base = declarative_base()

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
