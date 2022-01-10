from fastapi import FastAPI
from routers import blog_get, blog_post, article, product, user, file
from auth import authentication
from templates import templates
from db import models
from db.create_db import engine
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi import Request, HTTPException
from exceptions import StoryException
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket
from client import html
import time

app = FastAPI()

app.include_router(user.router)  # Aqui Importo(acesso) o arquivo python onde está a chamada para o CRUD do usuario no db

app.include_router(blog_get.router)  # Aqui importo(acesso) o arquivo python onde estarão os metodos get

app.include_router(blog_post.router)  # Aqui importo (acesso) o arquivo python onde estarão os metodos post

app.include_router(article.router)  # Aqui importo (acesso) o arquivo python onde estarão os metodos de criar/pegar os artigo

app.include_router(product.router)  # Aqui importo (acesso) o arquivo python onde estarão os metodos de criar/pegar os produtos

app.include_router(authentication.router)  # Aqui importo (acesso) o arquivo python onde ira autenticar os usuarios

app.include_router(file.router)  # Aqui importo (acesso) o arquivo python onde ira pegar/gravar os arquivos

app.include_router(templates.router)  # Aqui importo (acesso) o arquivo python onde ira pegar/gravar os arquivos de templates html/css

app.mount('/files', StaticFiles(directory='files'), name='files')  # Permito acessar arquivos ( imagens, docs, txt etc...)  no projeto

# @app.get('/')
# def index():
#     return {'message': 'Hello World'}


@app.exception_handler(StoryException)  # Importar : from exceptions import StoryException - from fastapi import Request - from fastapi.responses import JSONResponse, PlainTextResponse
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name}
    )


@app.get("/")  # WEBSOCKET
async def get():
    return HTMLResponse(html)  # from fastapi.response import HTMLResponse

clients= []

@app.websocket('/chat')
async def websocket_endpoint(websocket: WebSocket):  # from fastapi.websockets import WebSocket
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


# @app.exception_handler(HTTPException) # Importar : from exceptions import StoryException - from fastapi import HTTPException - from fastapi import Request - from fastapi.responses import JSONResponse
# def custon_handler(request: Request, exc: StoryException):
#     return PlainTextResponse(str(exc), status_code=400)


models.Base.metadata.create_all(engine)  # importar o modulo models.py acima e o modulo create_db / importa 'engine'


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response


app.mount('/files', StaticFiles(directory='files'), name='files')
app.mount('/templates/static', StaticFiles(directory="templates/static"), name="static")
