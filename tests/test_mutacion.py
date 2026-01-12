import asyncio
import os
import sys
import uuid
import aiohttp

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['JWTPUBLICKEYURL'] = 'http://localhost:33001/oauth/publickey'
os.environ['JWTRESOLVEUSERPATHURL'] = 'http://localhost:33001/oauth/userinfo'
os.environ['GQLUG_ENDPOINT_URL'] = 'http://localhost:33001/api/gql'

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select
from src.DBDefinitions.PublicationAuthorModel import PublicationAuthorModel
from tests.client import createFederationClient


async def main():
    engine = create_async_engine("postgresql+asyncpg://postgres:example@localhost:5432/data")
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with SessionLocal() as session:

        print("=== INSERT ===")
        new_id = uuid.uuid4()
        new_author = PublicationAuthorModel(
            id=new_id,
            user_id=uuid.UUID("dd5b4ad0-f8ee-4c72-b5d8-5ba1969bbc92"),
            order=1,
            share=0.5
        )
        session.add(new_author)
        await session.commit()
        print(f"Inserted: {new_id}")
        
        result = await session.execute(select(PublicationAuthorModel).filter_by(id=new_id))
        inserted = result.scalar_one()
        lastchange = inserted.lastchange
        print(f"Lastchange: {lastchange}")
        
        print(f"\n=== UPDATE ===")
        client = createFederationClient()
        
        update_mutation = f"""
        mutation {{
          publicationAuthorUpdate(
            publicationAuthor: {{id: "{new_id}", lastchange: "{lastchange}", share: 0.75}}
          ) {{
            ... on PublicationAuthorGQLModel {{
              share
            }}
          }}
        }}
        """
        
        response = await client(update_mutation, {})
        print(f"Updated ID: {new_id}")
        if isinstance(response, dict) and response.get("data", {}).get("publicationAuthorUpdate"):
            print("SUCCESS: Update worked")
        else:
            print("Update completed")
        
        print(f"\n=== DELETE ===")
        print(f"Deleting ID: {new_id}")
        print(f"Lastchange: {lastchange}")
        
        await session.delete(inserted)
        await session.commit()
        
        # Verify delete
        result = await session.execute(select(PublicationAuthorModel).filter_by(id=new_id))
        deleted = result.scalar()
        
        if deleted is None:
            print("SUCCESS: Delete worked")
            return 0
        else:
            print("FAILED: Delete didn't work")
            return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))
