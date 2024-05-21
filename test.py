from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    list_name: Mapped[list[str]] = mapped_column(
        ARRAY(String, dimensions=5),
        nullable=True,
        default=[
            "1",
            "3",
            "2",
        ],
    )


def gen_dict(obj):
    data_json = {
        "nullable": obj.nullable,
        "name": obj.name,
    }
    if isinstance(obj.type, ARRAY):
        data_json["type"] = f"list[{obj.type.item_type.python_type.__name__}]"
    else:
        data_json["type"] = obj.type.python_type.__name__

    if obj.default:
        data_json["default"] = obj.default.arg
    else:
        data_json["default"] = None

    if isinstance(obj.type, String):
        data_json["length"] = obj.type.length
    elif isinstance(obj.type, ARRAY):
        data_json["length"] = obj.type.dimensions
    else:
        data_json["length"] = None

    return data_json


print(User.__tablename__)
print([gen_dict(i) for i in User.__table__.columns])
