from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from typing import Optional, List
import time

router = APIRouter(
    prefix='/product',
    tags=['product']
)


products = ['Watch', 'Camera', 'Phone']

async def time_consuming_funcionality():  # Funcionalidade que precisa estar resolvida antes ou precisa de alguma resolução antes de ser rodada (async / await)
    time.sleep(5)
    return 'ok'

@router.post('/new')
def create_product(name: str = Form(...)):  #Importar: from fastapi import Form
    products.append(name)
    return products


@router.get('/all')
async def get_all_products():
    await time_consuming_funcionality()  # Funcionalidade que precisa estar resolvida antes ou precisa de alguma resolução antes de ser rodada (async / await)
    # return products
    data = " ".join(products)
    response = Response(content=data, media_type='text/plain')  # Importar: from fastapi.responses import Response
    response.set_cookie(key='test_cookie', value='test_cookie_value')
    return response


# usando custom headers
@router.get('/withheader')  # Importar: from fastapi.responses import Response - Importar: from fastapi import Header
def get_products(
        response: Response,
        custom_header: Optional[List[str]] = Header(None),
        test_cookie: Optional[str] = Cookie(None)
    ):
    if custom_header:
        response.headers['custom_response_header'] = ' and '.join(custom_header)
    return {
        'data': products,
        'custom_header': custom_header,
        'my_cookie': test_cookie
    }

@router.get('/{id}', responses={
    200: {
        "content": {
            'text/html': {
                "example": '<div>Product</div>'
            }
        },
        "description": "Returns the HTML for an object"
    },
    404: {
        "content": {
            'text/plain': {
                "exemple": 'Product not available'
            }
        },
        "description": "A clear text erro message"
    }
})
def get_one_product(id: int):
    if id > len(products):
        out = "Product not Available"
        return PlainTextResponse(status_code=404, content=out, media_type='text/plain')  ## Importar from fastapi.responses import PlainTextResponse
    else:
        product = products[id]
        out = f"""
        <head>
            <style>
            .product {{
                width: 500px;
                height: 30px;
                border: 2px inset green;
                background-color: lightblue;
                text-align: center;
            }}
            </style>
        </head>
        <div class="product">{product}</div>
        """
        return HTMLResponse(content=out, media_type='text/html')  # Importar from fastapi.responses import HTMLResponse