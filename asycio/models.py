import asyncio
import asyncpg
import os
import datetime
from sqlalchemy import String, func, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs


POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_USER = os.getenv("POSTGRES_USER", "swapi")
POSTGRES_DB = os.getenv("POSTGRES_DB", "swapi")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DNS = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(PG_DNS)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):

    __tablename__ = "swapi_people"

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.current_date, nullable=False)
    eye_color: Mapped[str] = mapped_column(String(15), nullable=False)
    films: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(60), nullable=False)
    height: Mapped[str] = mapped_column(String(50), nullable=False)
    home_world: Mapped[str] = mapped_column(String(70), nullable=False)
    mass: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=False)
    species: Mapped[str] = mapped_column(String(100), nullable=False)
    starships: Mapped[str] = mapped_column(String(100), nullable=False)
    vehicles: Mapped[str] = mapped_column(String(100), nullable=False)
    json: Mapped[dict] = mapped_column(JSON, nullable=False)


async def migrate_db():

    conn = await asyncpg.connect(user='swapi', password='secret', host='localhost', port='5432')

    await conn.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INT PRIMARY KEY,
            birth_year VARCHAR(50),
            eye_color VARCHAR(50),
            films TEXT,
            gender VARCHAR(50),
            hair_color VARCHAR(50),
            height VARCHAR(50),
            homeworld VARCHAR(255),
            mass VARCHAR(50),
            name VARCHAR(255),
            skin_color VARCHAR(50),
            species TEXT,
            starships TEXT,
            vehicles TEXT
        )
    ''')
    await conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(migrate_db())
