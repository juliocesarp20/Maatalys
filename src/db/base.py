from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import as_declarative, declared_attr

# Define a MetaData object with the schema
metadata = MetaData(schema="maatalys")


@as_declarative(metadata=metadata)
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
