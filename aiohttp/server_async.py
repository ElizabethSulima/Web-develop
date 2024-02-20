from aiohttp import web
from datetime import datetime

app = web.Application()
advertisements = []


async def create_advertisement(request: web.Request):
    data = await request.json()
    title = data['title']
    description = data['description']
    owner = data['owner']
    advertisement = {
        'title': title,
        'description': description,
        'owner': owner,
        'creation_date': str(datetime.now())
    }
    advertisements.append(advertisement)
    return web.json_response({'message': 'Advertisement created successfully.'}, status=201)


async def get_advertisements(request: web.Request):
    return web.json_response(advertisements, status=200)


async def get_advertisement(request: web.Request):
    advertisement_id = int(request.match_info['advertisement_id'])
    advertisement = next((adv for adv in advertisements if adv['id'] == advertisement_id), None)
    if advertisement:
        return web.json_response(advertisement, status=200)
    else:
        return web.json_response({'message': 'Advertisement not found.'}, status=404)


async def delete_advertisement(request: web.Request):
    advertisement_id = int(request.match_info['advertisement_id'])
    advertisement = next((adv for adv in advertisements if adv['id'] == advertisement_id), None)
    if advertisement:
        advertisements.remove(advertisement)
        return web.json_response({'message': 'Advertisement deleted successfully.'}, status=204)
    else:
        return web.json_response({'message': 'Advertisement not found.'}, status=404)


app.router.add_post('/advertisement', create_advertisement)
app.router.add_get('/advertisements', get_advertisements)
app.router.add_get('/advertisement/{advertisement_id}', get_advertisement)
app.router.add_delete('/advertisement/{advertisement_id}', delete_advertisement)


if __name__ == '__main__':
    web.run_app(app)
