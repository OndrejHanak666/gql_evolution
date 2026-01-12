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
    InputModelMixin, getUserFromInfo,
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
    ScalarResolver,
    TreeInputStructureMixin
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
PublicationCategoryGQLModel = typing.Annotated["PublicationCategoryGQLModel", strawberry.lazy(".PublicationCategoryGQLModel")]
PublicationCategoryInputFilter = typing.Annotated["PublicationCategoryInputFilter", strawberry.lazy(".PublicationCategoryGQLModel")]

@createInputs2
class PublicationTypeInputFilter:
    name: str
    name_en: str
    category_id: IDType
    mastertype_id: IDType

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

    publications: typing.List[PublicationGQLModel] = strawberry.field(
        description="Publications associated with this publication type",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver[PublicationGQLModel](fkey_field_name="publication_type_id", whereType=PublicationInputFilter)
    )


    category: typing.Optional[PublicationCategoryGQLModel] = strawberry.field(
        description="""Associated publication category""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[PublicationCategoryGQLModel](fkey_field_name="category_id")
    )

    # mastertype / subtypes (self-referential)
    mastertype_id: typing.Optional[IDType] = strawberry.field(
        description="ID of the parent publication type (master)",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    mastertype: typing.Optional["PublicationTypeGQLModel"] = strawberry.field(
        description="Parent (master) publication type",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver["PublicationTypeGQLModel"](fkey_field_name="mastertype_id")
    )

    subtypes: typing.List["PublicationTypeGQLModel"] = strawberry.field(
        description="Subtypes (children) of this publication type",
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver["PublicationTypeGQLModel"](fkey_field_name="mastertype_id", whereType=PublicationTypeInputFilter)
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

@strawberry.input(
    description="PublicationType insert mutation"
)
class PublicationTypeInsertGQLModel(TreeInputStructureMixin):
    getLoader = PublicationTypeGQLModel.getLoader
    name: typing.Optional[str] = strawberry.field(default=None)
    name_en: typing.Optional[str] = strawberry.field(default=None)
    id: typing.Optional[IDType] = strawberry.field(default=None)
    subtypes: typing.Optional[typing.List["PublicationTypeInsertGQLModel"]] = strawberry.field(description="Subtypes to be inserted along with this publication type", default_factory=list)
    mastertype_id: typing.Optional[IDType] = strawberry.field(default=None)

    path: strawberry.Private[str] = ""
    createdby_id: strawberry.Private["IDType"] = None
    rbacobject_id: strawberry.Private["IDType"] = None    #IDType("d75d64a4-bf5f-43c5-9c14-8fda7aff6c09")  # RBAC object for publication types"

@strawberry.input(
    description="PublicationType update mutation"
)
class PublicationTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="id")
    lastchange: datetime.datetime = strawberry.field(description="timestamp")
    name: typing.Optional[str] = strawberry.field(default=None)
    name_en: typing.Optional[str] = strawberry.field(default=None)
    

    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="PublicationType delete mutation"
)
class PublicationTypeDeleteGQLModel:
    id: IDType = strawberry.field(description="PublicationType id")
    lastchange: datetime.datetime = strawberry.field(description="PublicationType lastchange")


@strawberry.type(
    description="PublicationType mutation"
)
class PublicationTypeMutation:
    from .PublicationGQLModel import PublicationGQLModel
    @strawberry.field(
        description="Insert a PublicationType",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAbsoluteAccessControlExtension[InsertError, PublicationTypeGQLModel](roles=["administrátor"]),
        ],
    )
    async def publication_type_insert(
        self,
        info: strawberry.types.Info,
        publication_type: PublicationTypeInsertGQLModel,
        user_roles: typing.Optional[typing.List[typing.Dict]] = None,
    ) -> typing.Union[PublicationTypeGQLModel, InsertError[PublicationTypeGQLModel]]:
        return await Insert[PublicationTypeGQLModel].DoItSafeWay(info=info, entity=publication_type)


    @strawberry.field(
        description="Update a PublicationType",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAbsoluteAccessControlExtension[UpdateError, PublicationTypeUpdateGQLModel](roles=["administrátor"]),
        ],
    )
    async def publication_type_update(
        self,
        info: strawberry.types.Info,
        publication_type: PublicationTypeUpdateGQLModel,
        user_roles: typing.Optional[typing.List[typing.Dict]] = None,
    ) -> typing.Union[PublicationTypeGQLModel, UpdateError[PublicationTypeGQLModel]]:
        return await Update[PublicationTypeGQLModel].DoItSafeWay(info=info, entity=publication_type)


    @strawberry.field(
        description="Delete a PublicationType",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAbsoluteAccessControlExtension[DeleteError, PublicationTypeDeleteGQLModel](roles=["administrátor"]),
        ],
    )
    async def publication_type_delete(
        self,
        info: strawberry.types.Info,
        publication_type: PublicationTypeDeleteGQLModel,
        user_roles: typing.Optional[typing.List[typing.Dict]] = None,
    ) -> typing.Optional[DeleteError[PublicationTypeGQLModel]]:
        return await Delete[PublicationTypeGQLModel].DoItSafeWay(info=info, entity=publication_type)