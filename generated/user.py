from typing import Optional, List
from pydantic import BaseModel, Field
from typing_extensions import Annotated

class UserBaseScheme(BaseModel):
    name: Annotated[str, Field(max_length=50)] = 'sssss'
    list_name: Optional[Annotated[list[str], Field(max_length=5)]]


class UserAddScheme(UserBaseScheme):
    pass


class UserUpdateScheme(UserBaseScheme):
    name: Optional[Annotated[str, Field(max_length=50)]] = 'sssss'
    list_name: Optional[Annotated[list[str], Field(max_length=5)]]


class UserScheme(UserBaseScheme):
    id: Annotated[int, Field()]