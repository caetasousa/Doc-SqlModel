from sqlmodel import Session, select

from models import Hero, Team
from db import engine, SQLModel


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()

        hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id)
        hero_rusty_man = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, team_id=team_preventers.id)
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")

        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)


def select_heroes():
    with Session(engine) as session:
        #statement = select(Hero, Team).where(Hero.team_id == Team.id) # faz a mesma coisa que utilizando o join
        #statement = select(Hero, Team).join(Team, isouter=True) # isouter=True diz para trazer o que tiver team_id=Null
        statement = select(Hero, Team).join(Team).where(Team.name == "Preventers") # nao junta as 2 tabelas for com 2 items
        #statement = select(Hero).join(Team).where(Team.headquarters == "Sharp Tower") # depois de fazer o join, cria uma unica tabela e tbm e possivel colocar filtros o for e com 1 elemento
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)
        #for hero in results:
            #print("Preventer Hero:", hero)


def update_heroes():
    with Session(engine) as session:
        heroi = select(Hero).where(Hero.secret_name == 'Pedro Parqueador')
        time = select(Team).where(Team.name == "Preventers")
        resultsheroi = session.exec(heroi).one()
        resultstime = session.exec(time).one() # para descobri qual e o id do time
        
        resultsheroi.team_id = None # tirando a relacao com o time Preventers
        session.add(resultsheroi)
        session.commit()
        session.refresh(resultsheroi)

        print("Updated hero:", resultsheroi)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def main():
    create_db_and_tables()
    #create_heroes()
    select_heroes()
    #update_heroes()

if __name__ == "__main__":
    main()

