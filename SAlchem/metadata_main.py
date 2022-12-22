from sqlalchemy import MetaData, create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry, declarative_base, relationship


# Setting up MetaData with Table Objects
metadata_obj = MetaData()
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

# Setting up the Registry
mapper_registry = registry()
OldBase = mapper_registry.generate_base()
# The steps of creating the registry and “declarative base” classes can be combined into one step using the
# historically familiar declarative_base() function:
Base = declarative_base()


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
    print(user_table.c.name)
    print(user_table.c.keys())
    print(user_table.primary_key)
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
