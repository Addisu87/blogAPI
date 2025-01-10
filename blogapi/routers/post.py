from fastapi import APIRouter, HTTPException, status

from blogapi.core.database import comment_table, database, post_table
from blogapi.schemas.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

router = APIRouter(tags=["Posts"])


async def find_post(post_id: int):
    query = post_table.select().where(post_table.c.id == post_id)
    return await database.fetch_one(query)


@router.post(
    "/post",
    response_model=UserPost,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    query = post_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {"id": last_record_id, **data}


@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    query = post_table.select()
    return await database.fetch_all(query)


@router.post(
    "/comment",
    response_model=Comment,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(comment: CommentIn):
    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    data = comment.model_dump()
    query = comment_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {"id": last_record_id, **data}


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = await find_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }
