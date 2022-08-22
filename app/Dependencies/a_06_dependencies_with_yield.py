"""
FastAPI supports dependencies that do some extra steps after finishing. To do this, use yield instead of return,
and write the extra steps after.
You can have sub-dependencies and "trees" of sub-dependencies of any size, shape, and any or all of them can use yield.
"""
import uvicorn
from fastapi import FastAPI, Depends


class DBSession:
    def __init__(self):
        pass

    def close(self):
        pass


def generate_dep_a():
    return DBSession


def generate_dep_b():
    return DBSession


def generate_dep_c():
    return DBSession


async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()


async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)

