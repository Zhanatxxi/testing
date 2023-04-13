from fastapi import APIRouter

from src.project_name.bot.apps.create_user.schemas import AutoCreateUser
from src.project_name.bot.apps.create_user.utils import sign_up_users, sign_in_users, create_blog_with_author, \
    click_likes_random

bot_router = APIRouter()


@bot_router.post("")
async def generate_user(
    config: AutoCreateUser
):
    sign_up_users_responses = await sign_up_users(number_of_users=config.number_of_users)
    sign_in_users_response = await sign_in_users(users=sign_up_users_responses["success"])
    create_blog_with_author_response = await create_blog_with_author(
        users=sign_in_users_response,
        max_posts_per_user=config.max_posts_per_user,
    )
    await click_likes_random(
        users=sign_in_users_response,
        max_likes_per_user=config.max_likes_per_user
    )

    return create_blog_with_author_response
