from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

db_folder_path = Path("C:/Add/your/db/path")
SQLALCHEMY_DATABASE_URL = f'sqlite:///{db_folder_path}/ecommerce.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
    "check_same_thread": False
})
sessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

#return db session
def get_db():
    db = sessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"ERROR:: get_db function failed Exception: {e}")
    finally:
        db.close()