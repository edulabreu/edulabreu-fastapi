from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUsers
from db.hash import Hash
from fastapi import HTTPException, status


def create_user(db: Session, request: UserBase):  # Importar biblioteca: (from sqlalchemy.orm.session import Session) e UserBase importar do arquivo schemas.py
    new_user = DbUsers(  #DbUsers esta em models.py
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)  # importar o método Hash.bcrypt do arquivo hash
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session):
    return db.query(DbUsers).all()


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUsers).filter(DbUsers.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with name {username} not found')  # Importar da biblioteca fastapi os modulos HTTPException e status para tratar erros
    return user


def get_one_user(db: Session, id: int):
    user = db.query(DbUsers).filter(DbUsers.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')  # Importar da biblioteca fastapi os modulos HTTPException e status para tratar erros
    return user

def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DbUsers).filter(DbUsers.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')  # Importar da biblioteca fastapi os modulos HTTPException e status para tratar erros
    user.update({
        DbUsers.username: request.username,
        DbUsers.email: request.email,
        DbUsers.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return 'ok'

def delete_user(db: Session, id: int):
    user = db.query(DbUsers).filter(DbUsers.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} not found')  # Importar da biblioteca fastapi os modulos HTTPException e status para tratar erros
    db.delete(user)
    db.commit()
    return 'ok'