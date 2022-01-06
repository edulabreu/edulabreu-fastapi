from fastapi import APIRouter, status, Response, Depends
from enum import Enum
from typing import Optional
from routers.blog_post import required_functionality


router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


# @app.get('/blog/all')
# def get_all_blogs():
#     return {'message': 'All blogs provided'}


@router.get(
    '/all',
    summary='Retrive all blogs',
    description='This api call simulates fetching all blogs'
)
def get_all_blogs(page = 1, page_size: Optional[int] = None, req_param: dict = Depends(required_functionality)):
    return {'message': f'All {page_size} blogs on page {page}', 'req': req_param }


@router.get('/{id}/comments/{comment_id}', tags=['comments'])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    """
    Simulate retrieving a comment of a blog
    - **id** Mandatory path parameter
    - **comment_id** mandatory path parameter
    - **valid** opitional query parameter
    - **username** opitional query parameter

    """
    return {'message': f'blog_id: {id}, comment_id: {comment_id}, valid: {valid}, username: {username}'}


class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'


@router.get('/type/{type}', response_description='The type of available blogs')
def get_blog_type(type: BlogType):
    return {'message': f'Blog type {type}'}


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_blog(id: int, response: Response):
    if id > 5:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': f'Blog id {id} not found'}
    else:
        response.status_code = status.HTTP_200_OK
        return {'message': f'Blog with id {id}'}