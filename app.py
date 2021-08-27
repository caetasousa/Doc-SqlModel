from sqlmodel import Session

from models import Hero, Team
from db import engine, SQLModel



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def main():
    create_db_and_tables()


if __name__ == "__main__":
    main()

