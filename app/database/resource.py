from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class StreamingResource(SQLModel, table=True):
    __tablename__: str = "streaming_resources_alter"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    url: str = Field(..., index=True, unique=True)
    title: str
    date_added: datetime = Field(default=datetime.now())
