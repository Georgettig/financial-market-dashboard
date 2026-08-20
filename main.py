from database.connection import engine
from database.models import Base
from database.ingestion import run_ingestion


def main():

    Base.metadata.create_all(engine)

    print("Banco de dados inicializado.")

    run_ingestion()


if __name__ == "__main__":
    main()