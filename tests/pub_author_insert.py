#!/usr/bin/env python3
"""
PublicationAuthor Insert Mutation Test
"""
import asyncio
import os
import sys
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['JWTPUBLICKEYURL'] = 'http://localhost:33001/oauth/publickey'
os.environ['JWTRESOLVEUSERPATHURL'] = 'http://localhost:33001/oauth/userinfo'
os.environ['GQLUG_ENDPOINT_URL'] = 'http://localhost:33001/api/gql'

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select
from src.DBDefinitions.PublicationAuthorModel import PublicationAuthorModel


async def main():
    engine = create_async_engine("postgresql+asyncpg://postgres:example@localhost:5432/data")
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with SessionLocal() as session:
        # Count before
        result = await session.execute(select(PublicationAuthorModel))
        before = len(result.scalars().all())
        print(f"Before: {before} authors")
        
        # Insert
        new_id = uuid.uuid4()
        session.add(PublicationAuthorModel(
            id=new_id,
            user_id=uuid.UUID("dd5b4ad0-f8ee-4c72-b5d8-5ba1969bbc92"),
            order=1,
            share=0.5
        ))
        await session.commit()
        print(f"Inserted: {new_id}")
        
        # Count after
        result = await session.execute(select(PublicationAuthorModel))
        after = len(result.scalars().all())
        print(f"After: {after} authors")
        
        if after == before + 1:
            print("SUCCESS: Insert worked")
            return 0
        else:
            print("FAILED: Count didn't increase")
            return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))


if __name__ == "__main__":
    exit(asyncio.run(main()))
