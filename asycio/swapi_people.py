import asyncio
import asyncpg
import aiohttp
import datetime
from models import SwapiPeople, Session, engine, migrate_db


async def load_data(url, conn):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

            films = ','.join([film.split('/')[-2] for film in data['films']])
            species = ','.join([specie.split('/')[-2] for specie in data['species']])
            starships = ','.join([starship.split('/')[-2] for starship in data['starships']])
            vehicles = ','.join([vehicle.split('/')[-2] for vehicle in data['vehicles']])

            await conn.execute('''
                INSERT INTO characters (id, birth_year, eye_color, films, gender, hair_color, height, homeworld, mass, name, skin_color, species, starships, vehicles)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
            ''', data['id'], data['birth_year'], data['eye_color'], films, data['gender'], data['hair_color'], data['height'], data['homeworld'], data['mass'], data['name'], data['skin_color'], species, starships, vehicles)


async def load_data_to_db():

    conn = await asyncpg.connect(user='swapi', password='secret', host='localhost', port='5432')

    async with aiohttp.ClientSession() as session:
        async with session.get('https://swapi.dev/api/people/1/') as response:
            data = await response.json()
            characters = data['results']
            await asyncio.gather(*(load_data(character['url'], conn) for character in characters))

    await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(load_data_to_db())
