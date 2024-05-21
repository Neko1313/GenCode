import os
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import create_engine, inspect
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Путь к папке с шаблонами
template_dir = "templates"

# Создание окружения Jinja2
env = Environment(loader=FileSystemLoader(template_dir))


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


# Функция для генерации файлов
def generate_files(model_class, output_dir="generated"):
    model_name = model_class.__name__
    columns = [gen_dict(i) for i in model_class.__table__.columns]

    # DTO
    template = env.get_template("dto_template.jinja2")
    dto_content = template.render(model_name=model_name, columns=columns)
    dto_filename = os.path.join(output_dir, f"{model_name.lower()}.py")
    with open(dto_filename, "w") as f:
        f.write(dto_content)

    # Добавьте генерацию других файлов по аналогии


# Пример модели SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), default="sssss")
    list_name: Mapped[list[str]] = mapped_column(
        ARRAY(String, dimensions=5), nullable=True
    )


# Генерация файлов для модели User
generate_files(User)
