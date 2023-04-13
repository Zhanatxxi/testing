import string
import random

import aiohttp
from pydantic import EmailStr
from fastapi import HTTPException, status

from src.project_name.apps.auth.schemas import UserCreateSchema, SignInSchema, UserSignInSchema
from src.project_name.apps.blog.schemas import BlogSchema, BlogInDBSchema
from src.project_name.bot.config.settings import settings


def generate_email(number_of_users: int) -> str:
    domain_ = ['example.com', "gmail.com", "yandex.ru", "mail.ru", "yahoo.com"]

    for index in range(1, number_of_users+1):
        username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))
        domain = random.choice(domain_)
        yield f"{username}@{domain}"


def generate_password(length=9) -> str:
    """
    Generate a random activation code consisting of uppercase letters and digits.
    """
    characters = string.ascii_lowercase + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


async def sign_up_users(number_of_users: int):

    responses = {
        "success": list(),
        "error": list()
    }

    URL = settings.URL + "/auth/sign-up"

    async with aiohttp.ClientSession() as session:

        for email in generate_email(number_of_users):
            password = generate_password(length=9)

            user = UserCreateSchema(
                email=email,
                password=password,
                password_confirm=password
            )

            async with session.post(
                    url=URL,
                    json=user.dict()
            ) as response:
                if response.status == 201:
                    responses["success"].append(user)
                else:
                    responses["error"].append(user)

    return responses


async def sign_in_users(users: list[UserCreateSchema]):
    responses = dict()

    URL = settings.URL + "/auth/sign-in"

    async with aiohttp.ClientSession() as session:

        for user in users:
            user_sign_in = SignInSchema(email=user.email, password=user.password)
            print(user_sign_in.dict())

            async with session.post(
                    url=URL,
                    json=user_sign_in.dict()
            ) as response:
                if response.status == 200:
                    res = await response.json()
                    responses[user_sign_in.email] = UserSignInSchema(
                        access_token=res["access_token"],
                        refresh_token=res["refresh_token"]
                    )

    return responses


async def create_blog_with_author(
    users: dict[EmailStr, UserSignInSchema],
    max_posts_per_user: int
) -> list[BlogInDBSchema]:
    responses = list()

    URL = settings.URL + "/blog/"
    blog = BlogSchema(title="Blog")

    async with aiohttp.ClientSession() as session:

        for email, tokens in users.items():
            """ get access_token for Authorization """
            headers = {"Authorization": "Bearer {}".format(tokens.access_token)}

            for _ in range(max_posts_per_user):
                """ count create blog for thi's user """

                async with session.post(
                    url=URL,
                    json=blog.dict(),
                    headers=headers
                ) as response:
                    if response.status == 201:
                        blog_res = await response.json()
                        responses.append(BlogInDBSchema(
                            id=blog_res["id"],
                            title=blog_res["title"],
                            author_id=blog_res["author_id"],
                            created_date=blog_res["created_date"],
                            updated_date=blog_res["updated_date"]
                            )
                        )

    return responses


def get_blogs_ids(blogs):
    return [blog["id"] for blog in blogs]


def random_choice_blog_id(blogs_ids: list[int]):
    return random.choice(blogs_ids)


async def click_likes_random(
    users: dict[EmailStr, UserSignInSchema],
    max_likes_per_user: int
):
    URL = settings.URL + "/blog/"

    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=URL,
        ) as blogs_response:
            if blogs_response.status == 200:
                blogs_ids = get_blogs_ids(await blogs_response.json())
            else:
                blogs_ids = []

        if not blogs_ids:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Not blogs")

        for email, tokens in users.items():
            """ get access_token for Authorization """
            headers = {"Authorization": "Bearer {}".format(tokens.access_token)}

            for _ in range(max_likes_per_user):
                blog_id = random_choice_blog_id(blogs_ids)
                LIKE_URL = settings.URL + f"/blog/{blog_id}"

                async with session.post(
                    url=LIKE_URL,
                    headers=headers
                ) as like_response:
                    pass
