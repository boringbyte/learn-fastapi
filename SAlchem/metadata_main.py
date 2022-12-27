from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column  # These are common foundational objects for db metadata in SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import registry, declarative_base, relationship


# Setting up MetaData with Table Objects.
# To start using the SQLAlchemy Expression Language, we will want to have Table objects constructed that represent all
# the database tables we are interested in working with. Each Table may be declared, meaning we explicitly spell out
# in source code what the table looks like, or may be reflected, which means we generate the object based on what's
# already present in a particular database. The two approaches can also be blended in many ways.

# When using the ORM, the MetaData collection remains present, however it itself is associated with an ORM-only
# construct commonly referred towards as the Declarative Base. The most expedient way to acquire a new acquire
# Declarative Base is to create a new class that subclasses the SQLAlchemy DeclarativeBase class.


metadata_obj = MetaData()  # We start out with a collection that will be where we place our tables.
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)


address_table = Table(
     "address",
     metadata_obj,
     Column("id", Integer, primary_key=True),
     Column("user_id", ForeignKey("user_account.id"), nullable=False),
     Column("email_address", String, nullable=False),
)

# Defining Table Metadata with the ORM.
# When using the ORM, the process by which we declare Table metadata is usually combined with the process of declaring
# mapped classes. Setting up the Registry.
mapper_registry = registry()
OldBase = mapper_registry.generate_base()
# The steps of creating the registry and “declarative base” classes can be combined into one step using the
# historically familiar declarative_base() function:
Base = declarative_base()
"""
    In version 2.0
    from sqlalchemy.orm import DeclarativeBase
    class Base(DeclarativeBase):
        pass
    Base.metadata
    Base.registry
    
    from typing import List, Optional
    from sqlalchemy.orm import Mapped, mapped_column, relationship
    
    class User(Base):
        __tablename__ = "user_account"
    
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(30))
        fullname: Mapped[Optional[str]]
        addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    
        def __repr__(self) -> str:
            return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
    
    class Address(Base):
        __tablename__ = "address"
    
        id: Mapped[int] = mapped_column(primary_key=True)
        email_address: Mapped[str]
        user_id = mapped_column(ForeignKey("user_account.id"))
        user: Mapped[User] = relationship(back_populates="addresses")
    
        def __repr__(self) -> str:
            return f"Address(id={self.id!r}, email_address={self.email_address!r})"
"""


class User(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(30))
    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"))
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# Table Reflection:
# Table reflection refers to the process of generating Table and related objects by reading the current state of a
# database. Whereas in the previous sections we’ve been declaring Table objects in Python and then emitting DDL to the
# database, the reflection process does it in reverse.


if __name__ == '__main__':
    SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:////home/siva/Desktop/Projects/learn-fastapi/SAlchem/sample.db'
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    print(user_table.c.name)  # To get details about column name 'name' from table
    print(user_table.c.keys())  # To get list of columns in the table
    print(user_table.primary_key)  # To get details about the primary key from the table.
    print('-------------------------------------------')
    metadata_obj.drop_all(engine)
    metadata_obj.create_all(engine)
    metadata_obj.drop_all(engine)
    print('-------------------------------------------')
    print(mapper_registry.metadata)
    # mapper_registry.metadata.create_all(engine)  # same as metadata_obj
    print(User.__table__)
    sandy = User(name="sandy", fullname="Sandy Cheeks")
    print(sandy)
    # Base.metadata.create_all(engine)  # same as metadata_obj
    print('-------------------------------------------')
    # Table Reflection
    address = Table("address", metadata_obj, autoload_with=engine)
    print(address)
