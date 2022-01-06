from fastapi import APIRouter, Depends
from schemas import ArticleBase, ArticleDisplay, UserBase
from sqlalchemy.orm import Session
from db.create_db import get_db
from db import db_article
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/article',
    tags=['article']
)


# Create article
@router.post('/', response_model=ArticleDisplay)
def create_article(request: ArticleBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):  # o codigo até antes de current_user é base para Create_Article, current_user implementado para 'trancar' o metodo
    return db_article.create_article(db, request)


# Get specific article by user
@router.get('/{id}')  #response_model=ArticleDisplay)
def get_article(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):  # Importar from auth.oauth2 import oauth2_schema (trabalhando com autenticação
    return {
        'data': db_article.get_article(db, id),
        'current_user': current_user
    }