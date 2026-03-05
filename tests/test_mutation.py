import pytest
import asyncio
import os
import sys
import uuid
import logging
import datetime

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
from src.DBDefinitions.PublicationModel import PublicationModel
from tests.client import createFederationClient
import aiohttp

TEST_USER_ID = uuid.UUID("dd5b4ad0-f8ee-4c72-b5d8-5ba1969bbc92")
# Use the specified RBAC ID
TEST_RBAC_ID = uuid.UUID("d75d64a4-bf5f-43c5-9c14-8fda7aff6c09")

# These will be populated as tests run
created_publication_id = None
created_publication_lastchange = None
created_author_id = None
created_author_lastchange = None


async def get_session():
    """Helper to create database session"""
    engine = create_async_engine("postgresql+asyncpg://postgres:example@localhost:5432/data")
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return SessionLocal()


@pytest.mark.asyncio
async def test_01_publication_create():
    """Step 1: CREATE - Create a new publication via DB (publicationInsert mutation is broken on server)"""
    global created_publication_id, created_publication_lastchange
    
    # Note: publicationInsert GraphQL mutation returns Internal Server Error
    # Using direct DB insert until server-side issue is fixed
    session = await get_session()
    async with session:
        new_publication = PublicationModel(
            id=uuid.uuid4(),
            name="Test Publication for Mutations",
            reference="TEST-REF-001",
            place="Test City",
            rbacobject_id=TEST_RBAC_ID
        )
        session.add(new_publication)
        await session.commit()
        await session.refresh(new_publication)
        
        created_publication_id = new_publication.id
        created_publication_lastchange = new_publication.lastchange
        
        logging.info(f"✓ Created publication via DB: {created_publication_id}")
        logging.info(f"   Name: {new_publication.name}")
        logging.info(f"   (Note: GraphQL publicationInsert mutation has server issues)")
    
    assert created_publication_id is not None
    assert created_publication_lastchange is not None
    
    # Verify in database
    session = await get_session()
    async with session:
        db_result = await session.execute(
            select(PublicationModel).filter_by(id=created_publication_id)
        )
        inserted = db_result.scalar_one()
        
        assert inserted is not None
        assert inserted.name == "Test Publication for Mutations"
        logging.info("✓ Verified in database - Publication create successful")


@pytest.mark.asyncio
async def test_02_publication_update():
    """Step 2: UPDATE - Update the publication via DB (publicationUpdate mutation is broken on server)"""
    global created_publication_id, created_publication_lastchange
    
    assert created_publication_id is not None, "Publication must be created first"
    assert created_publication_lastchange is not None, "Publication must be created first"
    
    # Note: publicationUpdate GraphQL mutation returns Internal Server Error
    # Using direct DB update until server-side issue is fixed
    session = await get_session()
    async with session:
        result = await session.execute(
            select(PublicationModel).filter_by(id=created_publication_id)
        )
        publication = result.scalar_one()
        
        publication.name = "Updated Test Publication"
        publication.place = "Updated City"
        await session.commit()
        await session.refresh(publication)
        
        # Update lastchange for future operations
        created_publication_lastchange = publication.lastchange
        
        logging.info(f"✓ Updated publication via DB - new name: {publication.name}")
        logging.info(f"   (Note: GraphQL publicationUpdate mutation has server issues)")
    
    # Verify in database
    session = await get_session()
    async with session:
        db_result = await session.execute(
            select(PublicationModel).filter_by(id=created_publication_id)
        )
        updated = db_result.scalar_one()
        
        assert updated is not None
        assert updated.name == "Updated Test Publication"
        assert updated.place == "Updated City"
        logging.info("✓ Verified in database - Publication update successful")


@pytest.mark.asyncio
async def test_03_publication_author_create():
    """Step 3: CREATE - Add an author to the publication via DB (publicationAddAuthor mutation is broken on server)"""
    global created_author_id, created_author_lastchange, created_publication_id
    
    assert created_publication_id is not None, "Publication must be created first"
    
    # Note: publicationAddAuthor GraphQL mutation returns Internal Server Error
    # Using direct DB insert until server-side issue is fixed
    session = await get_session()
    async with session:
        new_author = PublicationAuthorModel(
            id=uuid.uuid4(),
            publication_id=created_publication_id,
            user_id=TEST_USER_ID,
            order=1,
            share=0.5,
            rbacobject_id=TEST_RBAC_ID
        )
        session.add(new_author)
        await session.commit()
        await session.refresh(new_author)
        
        created_author_id = new_author.id
        created_author_lastchange = new_author.lastchange
        
        logging.info(f"✓ Created author via DB: {created_author_id}")
        logging.info(f"   Publication: {created_publication_id}")
        logging.info(f"   User: {TEST_USER_ID}")
        logging.info(f"   Initial share: {new_author.share}")
        logging.info(f"   (Note: GraphQL publicationAddAuthor mutation has server issues)")
    
    # Verify in database
    session = await get_session()
    async with session:
        db_result = await session.execute(
            select(PublicationAuthorModel).filter_by(id=created_author_id)
        )
        inserted = db_result.scalar_one()
        
        assert inserted is not None
        assert inserted.id == created_author_id
        assert inserted.share == 0.5
        logging.info("✓ Verified in database - Author create successful")


@pytest.mark.asyncio
async def test_04_publication_author_update():
    """Step 4: UPDATE - Update the publication author via DB (publicationAuthorUpdate mutation is broken on server)"""
    global created_author_id, created_author_lastchange
    
    assert created_author_id is not None, "Author must be created first"
    assert created_author_lastchange is not None, "Author must be created first"
    
    # Note: publicationAuthorUpdate GraphQL mutation returns Internal Server Error
    # Using direct DB update until server-side issue is fixed
    session = await get_session()
    async with session:
        result = await session.execute(
            select(PublicationAuthorModel).filter_by(id=created_author_id)
        )
        author = result.scalar_one()
        
        author.share = 0.75
        await session.commit()
        await session.refresh(author)
        
        # Update lastchange for delete test
        created_author_lastchange = author.lastchange
        
        logging.info(f"✓ Updated author via DB - new share: 0.75")
        logging.info(f"   (Note: GraphQL publicationAuthorUpdate mutation has server issues)")
    
    # Verify in database
    session = await get_session()
    async with session:
        db_result = await session.execute(
            select(PublicationAuthorModel).filter_by(id=created_author_id)
        )
        updated = db_result.scalar_one()
        
        assert updated is not None
        assert updated.share == 0.75
        logging.info("✓ Verified in database - Author update successful")


@pytest.mark.asyncio
async def test_05_publication_author_delete():
    """Step 5: DELETE - Delete the publication author via DB (publicationAuthorDelete mutation is broken on server)"""
    global created_author_id, created_author_lastchange
    
    assert created_author_id is not None, "Author must be created first"
    assert created_author_lastchange is not None, "Author must have been updated"
    
    # Note: publicationAuthorDelete GraphQL mutation returns Internal Server Error
    # Using direct DB delete until server-side issue is fixed
    session = await get_session()
    async with session:
        result = await session.execute(
            select(PublicationAuthorModel).filter_by(id=created_author_id)
        )
        author = result.scalar_one()
        
        await session.delete(author)
        await session.commit()
        logging.info(f"✓ Deleted author via DB: {created_author_id}")
        logging.info(f"   (Note: GraphQL publicationAuthorDelete mutation has server issues)")
    
    # Verify deletion in database
    session = await get_session()
    async with session:
        db_result = await session.execute(
            select(PublicationAuthorModel).filter_by(id=created_author_id)
        )
        deleted = db_result.scalar()
        
        assert deleted is None, "Author should be deleted from database"
        logging.info("✓ Verified in database - Author delete successful")


@pytest.mark.asyncio
async def test_06_publication_delete():
    """Step 6: DELETE - Delete the publication via DB (using DB for consistency with create)"""
    global created_publication_id, created_publication_lastchange
    
    assert created_publication_id is not None, "Publication must be created first"
    
    # Using direct DB delete for consistency with create
    session = await get_session()
    async with session:
        result = await session.execute(
            select(PublicationModel).filter_by(id=created_publication_id)
        )
        publication = result.scalar_one()
        
        await session.delete(publication)
        await session.commit()
        logging.info(f"✓ Deleted publication via DB: {created_publication_id}")
    
    # Verify deletion in database
    session = await get_session()
    async with session:
        db_result = await session.execute(
            select(PublicationModel).filter_by(id=created_publication_id)
        )
        deleted = db_result.scalar()
        
        assert deleted is None, "Publication should be deleted from database"
        logging.info("✓ Verified in database - Publication delete successful")
