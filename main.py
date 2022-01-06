from fastapi import FastAPI
from routers import blog_get, blog_post, article, product, user, file
from auth import authentication
from db import models
from db.create_db import engine
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi import Request, HTTPException
from exceptions import StoryException
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(user.router)  # Aqui Importo(acesso) o arquivo python onde está a chamada para o CRUD do usuario no db

app.include_router(blog_get.router)  # Aqui importo(acesso) o arquivo python onde estarão os metodos get

app.include_router(blog_post.router)  # Aqui importo (acesso) o arquivo python onde estarão os metodos post

app.include_router(article.router)  # Aqui importo (acesso) o arquivo python onde estarão os metodos de criar/pegar os artigo

app.include_router(product.router)  # Aqui importo (acesso) o arquivo python onde estarão os metodos de criar/pegar os produtos

app.include_router(authentication.router)  # Aqui importo (acesso) o arquivo python onde ira autenticar os usuarios

app.include_router(file.router) # Aqui importo (acesso) o arquivo python onde ira pegar/gravar os arquivos


app.mount('/files', StaticFiles(directory='files'), name='files')  # Permito acessar arquivos ( imagens, docs, txt etc...)  no projeto

@app.get('/')
def index():
    return {'message': 'Hello World'}


@app.exception_handler(StoryException)  # Importar : from exceptions import StoryException - from fastapi import Request - from fastapi.responses import JSONResponse, PlainTextResponse
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name}
    )


# @app.exception_handler(HTTPException) # Importar : from exceptions import StoryException - from fastapi import HTTPException - from fastapi import Request - from fastapi.responses import JSONResponse
# def custon_handler(request: Request, exc: StoryException):
#     return PlainTextResponse(str(exc), status_code=400)


models.Base.metadata.create_all(engine)  # importar o modulo models.py acima e o modulo create_db importar 'engine'
