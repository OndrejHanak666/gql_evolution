import pytest
import asyncio
import os
import sys
import uuid
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mark all tests in this file to run sequentially (they depend on shared test data)
pytestmark = pytest.mark.serial

os.environ['JWTPUBLICKEYURL'] = 'http://localhost:33001/oauth/publickey'
os.environ['JWTRESOLVEUSERPATHURL'] = 'http://localhost:33001/oauth/userinfo'
os.environ['GQLUG_ENDPOINT_URL'] = 'http://localhost:33001/api/gql'

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select
from src.DBDefinitions.PublicationAuthorModel import PublicationAuthorModel
from tests.client import createFederationClient
import aiohttp

# Fixed test ID - same one for all tests
TEST_AUTHOR_ID = uuid.UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")


async def get_session():
    """Helper to create database session"""
    engine = create_async_engine("postgresql+asyncpg://postgres:example@localhost:5432/data")
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return SessionLocal()


@pytest.mark.asyncio
async def test_publication_author_create():
    """CREATE - Test inserting a publication author"""
    session = await get_session()
    
    async with session:
        new_author = PublicationAuthorModel(
            id=TEST_AUTHOR_ID,
            user_id=uuid.UUID("dd5b4ad0-f8ee-4c72-b5d8-5ba1969bbc92"),
            order=1,
            share=0.5
        )
        session.add(new_author)
        await session.commit()
        logging.info(f"Created author: {TEST_AUTHOR_ID}")
        
        result = await session.execute(select(PublicationAuthorModel).filter_by(id=TEST_AUTHOR_ID))
        inserted = result.scalar_one()
        
        assert inserted is not None
        assert inserted.id == TEST_AUTHOR_ID
        assert inserted.share == 0.5
        logging.info("✓ Create operation successful")


@pytest.mark.asyncio
async def test_publication_author_update():
    """UPDATE - Test updating a publication author"""
    session = await get_session()
    
    async with session:
        # Get the author that was created in test_publication_author_create
        result = await session.execute(select(PublicationAuthorModel).filter_by(id=TEST_AUTHOR_ID))
        inserted = result.scalar_one()
        lastchange = inserted.lastchange
        logging.info(f"Updating author: {TEST_AUTHOR_ID}")
        
        # Now update via GraphQL mutation
        client = createFederationClient()
        
        update_mutation = f"""
        mutation {{
          publicationAuthorUpdate(
            publicationAuthor: {{id: "{TEST_AUTHOR_ID}", lastchange: "{lastchange}", share: 0.75}}
          ) {{
            ... on PublicationAuthorGQLModel {{
              share
            }}
          }}
        }}
        """
        
        try:
            response = await client(update_mutation, {})
        except aiohttp.client_exceptions.ClientConnectorError as e:
            pytest.skip(f"GraphQL server not available at localhost:8001: {e}")
        
        assert isinstance(response, dict)
        assert response.get("data", {}).get("publicationAuthorUpdate") is not None
        logging.info(f"Updated author - new share: 0.75")
        logging.info("✓ Update operation successful")


@pytest.mark.asyncio
async def test_publication_author_delete():
    """DELETE - Test deleting a publication author"""
    session = await get_session()
    
    async with session:
        # Get the author that was created in test_publication_author_create
        result = await session.execute(select(PublicationAuthorModel).filter_by(id=TEST_AUTHOR_ID))
        inserted = result.scalar_one()
        
        logging.info(f"Deleting author: {TEST_AUTHOR_ID}")
        
        # Delete
        await session.delete(inserted)
        await session.commit()
        
        # Verify delete
        result = await session.execute(select(PublicationAuthorModel).filter_by(id=TEST_AUTHOR_ID))
        deleted = result.scalar()
        
        assert deleted is None
        logging.info("✓ Delete operation successful")
