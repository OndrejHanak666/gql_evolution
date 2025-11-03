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


PublicationGQLModel = typing.Annotated["PublicationGQLModel", strawberry.lazy(".PublicationGQLModel")]
PublicationInputFilter = typing.Annotated["PublicationInputFilter", strawberry.lazy(".PublicationGQLModel")]

@createInputs2
class PublicationTypeInputFilter:
    name: str
    name_en: str
    category_id: IDType

@strawberry.federation.type(
    keys=["id"],
    description="Entity representing a publication type"
)


class PublicationTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).PublicationTypeModel

    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path representing the group's hierarchical location.  
Materializovaná cesta reprezentující umístění skupiny v hierarchii.""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    name: typing.Optional[str] = strawberry.field(
        description="""Name of the publication type""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    name_en: typing.Optional[str] = strawberry.field(
        description="""English name of the publication type""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )   

    category_id: typing.Optional[IDType] = strawberry.field(
        description="""ID of the associated category""",
        default=None,
        permission_classes=[OnlyForAuthentized],
        directives=[Relation(to="CategoryGQLModel")]
    )

    publicattions: typing.List[PublicationGQLModel] = strawberry.field(
        description="Publications associated with this publication type",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver[PublicationGQLModel](fkey_field_name="publication_type_id", whereType=PublicationInputFilter)
    )


@strawberry.interface(
    description="""Publication_type queries"""
)
class PublicationTypeQuery:
    publication_type_by_id: typing.Optional[PublicationTypeGQLModel] = strawberry.field(
        description="""get a publication type by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=PublicationTypeGQLModel.load_with_loader
    )

    publication_type_page: typing.List[PublicationTypeGQLModel] = strawberry.field(
        description="""get a page of publication types""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[PublicationTypeGQLModel](whereType=PublicationTypeInputFilter)
    )