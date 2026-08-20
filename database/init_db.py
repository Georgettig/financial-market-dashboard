from connection import engine
from models import Base


def init_database():

    Base.metadata.create_all(engine)

    print("Tabelas criadas com sucesso!")


if __name__ == "__main__":
    init_database()