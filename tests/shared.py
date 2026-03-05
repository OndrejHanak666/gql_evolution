import sqlalchemy
import sys
import asyncio

# setting path
sys.path.append("../gql_events")

import pytest

# from ..uoishelpers.uuid import UUIDColumn

from DBDefinitions import BaseModel


async def prepare_in_memory_sqllite():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker

    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


from DBFeeder import get_demodata


async def prepare_demodata(async_session_maker):
    data = get_demodata()

    from uoishelpers.feeders import ImportModels

    await ImportModels(
        async_session_maker,
        [
        ],
        data,
    )


from Dataloaders import createLoadersContext


def get_test_user():
    """Get test user from systemdata.json"""
    from uoishelpers.dataloaders import readJsonFile
    jsonData = readJsonFile(jsonFileName="./systemdata.json")
    users = jsonData.get("users", [])
    return users[0] if users else None


def createContext(asyncSessionMaker, withuser=True):
    loadersContext = createLoadersContext(asyncSessionMaker)
    user = get_test_user()
    if withuser and user:
        loadersContext["user"] = user
    
    return loadersContext

def createInfo(asyncSessionMaker, withuser=True):
    user = get_test_user()
    
    class Request():
        @property
        def headers(self):
            return {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
        
        @property
        def scope(self):
            return {"user": user if withuser else None}
        
    class Info():
        @property
        def context(self):
            context = createContext(asyncSessionMaker, withuser=withuser)
            context["request"] = Request()
            return context
        
    return Info()