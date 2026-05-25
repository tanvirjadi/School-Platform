import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert
from werkzeug.security import generate_password_hash

def main():
    # Load environment variables from the root .env file
    load_dotenv()

    # Database configuration
    try:
        db_user = os.environ['DB_USER']
        db_password = os.environ['DB_PASSWORD']
        db_host = os.environ['DB_HOST']
        db_port = os.environ['DB_PORT']
        db_name = os.environ['DB_NAME']
    except KeyError as e:
        print(f"Error: Missing environment variable {e}")
        sys.exit(1)

    DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    # Setup SQLAlchemy
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()

    users = Table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("username", String(30), nullable=False, unique=True),
        Column("email", String(320), nullable=False, unique=True),
        Column("password", String, nullable=False),
        Column("role", String(10), nullable=False),
    )

    # Get input from user
    print("--- Create New Admin Account ---")
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    if not username or not email or not password:
        print("Error: All fields are required.")
        sys.exit(1)

    # Hash password using werkzeug (to match backend)
    hashed_password = generate_password_hash(password)

    # Insert into database
    try:
        with engine.connect() as conn:
            stmt = insert(users).values(
                username=username,
                email=email,
                password=hashed_password,
                role='admin'
            )
            conn.execute(stmt)
            conn.commit()
            print(f"\nSuccess! Admin account '{username}' created successfully.")
    except Exception as e:
        print(f"\nError: Could not create account. {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
