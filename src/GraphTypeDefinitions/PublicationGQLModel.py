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


PublicationAuthorGQLModel = typing.Annotated["PublicationAuthorGQLModel", strawberry.lazy(".PublicationAuthorGQLModel")]
PublicationAuthorInputFilter = typing.Annotated["PublicationAuthorInputFilter", strawberry.lazy(".PublicationAuthorGQLModel")]
PublicationTypeGQLModel = typing.Annotated["PublicationTypeGQLModel", strawberry.lazy(".PublicationTypeGQLModel")]
PublicationTypeInputFilter = typing.Annotated["PublicationTypeInputFilter", strawberry.lazy(".PublicationTypeGQLModel")]

@createInputs2
class PublicationInputFilter:
    name: str
    published_date: datetime.datetime
    reference: str
    valid: bool
    place: str
    id: IDType
    publication_type_id: IDType


@strawberry.federation.type(
    keys=["id"],
    description="Entity representing a publication"
)
class PublicationGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).PublicationModel

    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path representing the group's hierarchical location.  
Materializovaná cesta reprezentující umístění skupiny v hierarchii.""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Publication name assigned by an administrator""",
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    publication_type_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""ID of the publication type""",
        permission_classes=[OnlyForAuthentized]
    )

    published_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Date of publication""",
        permission_classes=[OnlyForAuthentized]
    )

    reference: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Reference of the publication""",
        permission_classes=[OnlyForAuthentized]
    )

    valid: typing.Optional[bool] = strawberry.field(
        name="valid_raw",
        description="""If it intersects current date""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    @strawberry.field(
        name="valid",
        description="""Event duration, implicitly in minutes""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ],
    )
    def valid_(self) -> typing.Optional[bool]:
     if self.valid is not None:
        return self.valid

     now = datetime.datetime.now().date()  # dnešní datum bez času
     if self.published_date:
        # True pokud published_date je dnešní den
         return self.published_date.date() <= now

     return False
    
    place: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Place of publication""",
        permission_classes=[OnlyForAuthentized]
    )

    authors: typing.List["PublicationAuthorGQLModel"] = strawberry.field(
       description="""Authors of the publication""",
       permission_classes=[OnlyForAuthentized],
       resolver = VectorResolver[ "PublicationAuthorGQLModel" ](fkey_field_name="publication_id",whereType=PublicationAuthorInputFilter)
    )

    publicationtype: typing.Optional["PublicationTypeGQLModel"] = strawberry.field(
        description="""Type of the publication""",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver["PublicationTypeGQLModel"](fkey_field_name="publication_type_id")
    )




@strawberry.interface(
    description="""Publication queries"""
)
class PublicationQuery:
    publication_by_id: typing.Optional[PublicationGQLModel] = strawberry.field(
        description="""get a publication by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=PublicationGQLModel.load_with_loader
    )

    publication_page: typing.List[PublicationGQLModel] = strawberry.field(
        description="""get a page of publications""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[PublicationGQLModel](whereType=PublicationInputFilter)
    )
