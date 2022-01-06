from sqlalchemy.orm import relationship
from db.create_db import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.sql.schema import ForeignKey


class DbUsers(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship('DbArticle', back_populates='user')  # Artigos que o usuario criou estao relacionados aqui


class DbArticle(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))  # Precisa importar a biblioteca ForeignKey ('from sqlalchemy.sql.schema import ForeignKey')
    user = relationship('DbUsers', back_populates='items')  # Precisa importar a biblioteca relationship ('from sqlalchemy.orm import relationship') -> Usuario que criou o artigo (relacionando com a tabela usuario)


