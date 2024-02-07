import uvicorn
from fastapi import FastAPI

from api.router import router
from settings import settings_app

app = FastAPI(
    title='Сервис для извлечения юридической информации из дерева в форматах Json и Xml'
)

app.include_router(router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings_app.SERVER_HOST,
        port=settings_app.SERVER_PORT,
        debug=True,
        reload=True
    )
