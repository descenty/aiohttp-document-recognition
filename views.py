import concurrent.futures
from io import BytesIO
import image_recognition
from aiohttp import web
import asyncio

media_path = 'media/'


async def index(request: web.Request):
    loop = asyncio.get_event_loop()
    data: list[dict] = []
    async for obj in (await request.multipart()):
        if obj.filename is not None:
            file = BytesIO(await obj.read())
            with concurrent.futures.ProcessPoolExecutor() as pool:
                result = await loop.run_in_executor(pool, image_recognition.process_file, file)
            data.append(result.__dict__)
    return web.json_response(data)
