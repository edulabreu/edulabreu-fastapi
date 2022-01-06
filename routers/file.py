from fastapi import APIRouter, File, UploadFile
import shutil
from fastapi.responses import FileResponse

router = APIRouter(
    prefix='/file',
    tags=['file']
)

@router.post('/file')
def get_file(file: bytes = File(...)):  # importar : from fastapi import File
    content = file.decode('utf-8')
    lines = content.split('\n')
    return {'lines': lines}


@router.post('/uploadFile')
def get_uploadFile(upload_file: UploadFile = File(...)):  # importar : from fastapi import UploadFile
    path = f'files/{upload_file.filename}'  # Criando um caminho para armazenar o arquivo no projeto
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)  # Criando e armazenando o arquivo no projeto (pasta files)

    return {
        'filename': path,
        'type': upload_file.content_type
    }

@router.get('/download/{name}', response_class=FileResponse)  # Importar: from fastapi.responses import FileResponse
def get_file(name: str):
    path = f'files/{name}'

    return path