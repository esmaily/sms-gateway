import databases
import ormar
from typing import Optional
import sqlalchemy
from datetime import datetime
from .config import settings

database = databases.Database(settings.DB_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class GatewayModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "gateways"

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=150, unique=True, nullable=False)
    token: str = ormar.String(max_length=150,nullable=True)
    username: str = ormar.String(max_length=128,  nullable=True)
    password: str = ormar.String(max_length=128, nullable=True)
    url: str = ormar.String(max_length=128, nullable=True)
    active: bool = ormar.Boolean(default=True, nullable=False)
    priority: int = ormar.Integer(default=1)
    created_at: sqlalchemy.DateTime = ormar.DateTime(nullable=True, default=datetime.now)
    updated_at: sqlalchemy.DateTime = ormar.DateTime(nullable=True, default=datetime.now)


class SmsModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "smses"

    id: int = ormar.Integer(primary_key=True)
    mobile: str = ormar.String(max_length=255, nullable=False)
    text: str = ormar.Text(nullable=True)
    gateway: Optional[GatewayModel] = ormar.ForeignKey(GatewayModel)
    created_at: sqlalchemy.DateTime = ormar.DateTime(nullable=True, default=datetime.now)
    updated_at: sqlalchemy.DateTime = ormar.DateTime(nullable=True, default=datetime.now)



 

engine = sqlalchemy.create_engine(settings.DB_URL)
metadata.create_all(engine)
