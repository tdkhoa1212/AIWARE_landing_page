from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymongo

URL_DATABASE = 'mysql+pymysql://root:!AIWARE!@localhost:3306/AIWARE'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# def check_database_connection():
#     try:
#         # Attempt to create a session
#         session = SessionLocal()
        
#         # Execute a simple query to check the connection
#         result = session.execute(text('select * from contacts;'))
        
#         # Close the session
#         session.close()
        
#         # Print connection status
#         print("Connection to the database is successful.")
#     except Exception as e:
#         print("Error connecting to the database:", e)

# # Check the database connection
# check_database_connection()
