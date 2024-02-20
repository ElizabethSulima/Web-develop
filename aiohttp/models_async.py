import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String
from aiohttp import web

Base = declarative_base()
app = web.Application()


class Advertisement(Base):
    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    owner = Column(String(50), nullable=False)

    async def delete_advertisement(request: web.Request):
        user_id = int(request.match_info['id'])
        async with request.app['db'].acquire() as conn:
            try:
                query = sqlalchemy.delete(Advertisement).where(Advertisement.id == user_id)
                await conn.execute(query)
            except sqlalchemy.exc.NoResultFound:
                return web.json_response({'error': 'Объявление не найдено'}, status=404)
            return web.json_response({'message': 'Объявление успешно удалено'}, status=200)

    async def create_advertisement(request: web.Request):
        data = await request.json()
        if 'title' not in data or 'description' not in data or 'owner' not in data:
            return web.json_response({'error': 'Не указаны обязательные поля'}, status=400)
        advertisement = Advertisement(
            title=data['title'],
            description=data['description'],
            owner=data['owner']
        )
        async with request.app['db'].begin() as conn:
            async with AsyncSession(conn) as session:
                session.add(advertisement)
                await session.commit()

        return web.json_response({'message': 'Объявление успешно создано'}, status=201)

    async def get_advertisement(request: web.Request):
        user_id = int(request.match_info['id'])
        async with request.app['db'].begin() as conn:
            async with AsyncSession(conn) as session:
                query = select(Advertisement).where(Advertisement.id == user_id)
                result = await session.execute(query)
                advertisement = result.scalar()

                if not advertisement:
                    return web.json_response({'error': 'Объявление не найдено'}, status=404)

                return web.json_response(advertisement.to_dict(), status=200)

    app.router.add_post('/api/advertisements', create_advertisement)
    app.router.add_get('/api/advertisements/{id}', get_advertisement)


