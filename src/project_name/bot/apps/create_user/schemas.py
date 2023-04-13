from pydantic import BaseModel, Field


class AutoCreateUser(BaseModel):
    number_of_users: int = Field(gte=1, description="when count create users")
    max_posts_per_user: int = Field(gte=1, description="when count create blog for every user")
    max_likes_per_user: int = Field(gte=1, description="when count create like for every user")
