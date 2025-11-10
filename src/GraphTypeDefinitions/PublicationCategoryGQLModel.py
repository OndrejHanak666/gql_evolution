import asyncio
import dataclasses
import datetime
import typing
import strawberry

import strawberry.types
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,
    createInputs2,

    InsertError, 
    Insert, 
    UpdateError, 
    Update, 
    DeleteError, 
    Delete,

    PageResolver,
    VectorResolver,
    ScalarResolver
)
from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.RbacInsertProviderExtension import RbacInsertProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

from .BaseGQLModel import BaseGQLModel, IDType, Relation
from .TimeUnit import TimeUnit

PublicationTypeGQLModel = typing.Annotated["PublicationTypeGQLModel", strawberry.lazy(".PublicationTypeGQLModel")]
PublicationTypeInputFilter = typing.Annotated["PublicationTypeInputFilter", strawberry.lazy(".PublicationTypeGQLModel")]


@createInputs2
class PublicationCategoryInputFilter:
    id: IDType
    name: str
    name_en: str
    
@strawberry.federation.type(
    keys=["id"],
    description="Entity representing a publication author")

class PublicationCategoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).PublicationCategoryModel

    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path representing the group's hierarchical location.  
Materializovaná cesta reprezentující umístění skupiny v hierarchii.""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    name: typing.Optional[str] = strawberry.field(
        description="Name of the publication category",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    name_en: typing.Optional[str] = strawberry.field(
        description="English name of the publication category",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )


    publicationtypes: typing.List[PublicationTypeGQLModel] = strawberry.field(
        description="Publication types associated with this publication category",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver[PublicationTypeGQLModel](fkey_field_name="id", whereType=PublicationTypeInputFilter)
    )

   
    



@strawberry.interface(
    description="""Publication_category queries"""
)
class PublicationCategoryQuery:
    publication_category_by_id: typing.Optional[PublicationCategoryGQLModel] = strawberry.field(
        description="""get a publication_category by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=PublicationCategoryGQLModel.load_with_loader
    )

    publication_category_page: typing.List[PublicationCategoryGQLModel] = strawberry.field(
        description="""get a page of publication_categories""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[PublicationCategoryGQLModel](whereType=PublicationCategoryInputFilter)
    )


   
