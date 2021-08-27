from sqlmodel import Session, select, or_

from models import Hero
from db import engine, SQLModel


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        session.commit()


def select_heroes_all():
    with Session(engine) as session:
        statement = select(Hero)
        heroes = session.exec(select(Hero)).all() # traz todos elementos
        #heroes = session.exec(select(Hero.name, Hero.id)).all() # traz apenas as colunas selecionadas
        #results = session.exec(statement)
        #heroes = results.all() 
        print(heroes)


def select_heroes_each():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond") # traz apenas os elementos de nome Deadpond
        #statement = select(Hero).where(Hero.age >= 35).where(Hero.age < 40) # pega os valores entre as condicoes
        #statement = select(Hero).where(or_(Hero.name == "Deadpond", Hero.name == "Rusty-Man")) # utiliza a condicao OR e traz os 2 elementos
        results = session.exec(statement)
        #hero = session.exec(select(Hero).where(Hero.name == "Deadpond")).one()
        #for hero in results:
        #    print(hero)
        #hero = results.first() # Le apenas a primeira linha, caso n encontre nada retorna None
        #hero = results.one() # existe apenas um "Deadpond"e não deve haver mais de um.
        hero = session.get(Hero, 1) # selecao por id
        print(hero)


def select_heroes_ofset_limit():
    with Session(engine) as session:
        statement = select(Hero).offset(6).limit(3) # offset -> a busca comeca a partir do 6 elemento
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)


def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Dr. Weird")
        results = session.exec(statement)
        hero = results.one()
        print("Hero:", hero)

        hero.age = 25
        hero.secret_name = "Eduardo Caetano"
        session.add(hero)
        session.commit()
        session.refresh(hero)

        print("Updated hero:", hero)


def delete_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "eduardo1")
        results = session.exec(statement)
        hero = results.all()
        #print("Hero: ", hero)
        for c in hero:
            session.delete(c) # deleta apenas uma linha por vez
            session.commit()

        print("Deleted hero:", hero) # imprime mesmo depois de deletado


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def main():
    create_db_and_tables()
    #create_heroes()
    #select_heroes_all()
    #select_heroes_each()
    #select_heroes_ofset_limit()
    #update_heroes()
    delete_heroes()

if __name__ == "__main__":
    main()

