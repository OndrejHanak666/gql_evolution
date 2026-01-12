#!/usr/bin/env python3
"""
PublicationAuthor Delete Last Created - Simple Test
"""
import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['JWTPUBLICKEYURL'] = 'http://localhost:33001/oauth/publickey'
os.environ['JWTRESOLVEUSERPATHURL'] = 'http://localhost:33001/oauth/userinfo'
os.environ['GQLUG_ENDPOINT_URL'] = 'http://localhost:33001/api/gql'

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, desc
from src.DBDefinitions.PublicationAuthorModel import PublicationAuthorModel


async def main():
    engine = create_async_engine("postgresql+asyncpg://postgres:example@localhost:5432/data")
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with SessionLocal() as session:
        print("=== DELETE LAST AUTHOR ===\n")
        
        # Get last created author (by id ordering)
        result = await session.execute(
            select(PublicationAuthorModel).order_by(desc(PublicationAuthorModel.id)).limit(1)
        )
        last_author = result.scalar()
        
        if last_author is None:
            print("FAILED: No authors found to delete")
            return 1
        
        print(f"Last author ID: {last_author.id}")
        print(f"Lastchange: {last_author.lastchange}")
        
        # Delete it
        await session.delete(last_author)
        await session.commit()
        
        # Verify
        result = await session.execute(select(PublicationAuthorModel).filter_by(id=last_author.id))
        deleted = result.scalar()
        
        if deleted is None:
            print("SUCCESS: Delete worked")
            return 0
        else:
            print("FAILED: Delete didn't work")
            return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))
