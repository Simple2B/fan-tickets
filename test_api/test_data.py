from pydantic import BaseModel


class TestUser(BaseModel):
    __test__ = False

    username: str
    email: str
    password: str


class TestData(BaseModel):
    __test__ = False

    authorized_users: list[TestUser]
