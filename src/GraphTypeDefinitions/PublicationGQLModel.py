import asyncio
import dataclasses
import datetime
import typing
from numpy import info
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
    description="Entity representing a publication"  ###TODO i u dalsich modelu
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
    def valid_(self) -> bool:
        # 1. Check explicit override from DB (self.valid maps to the column defined above)
        if self.valid is not None:
            return self.valid

        # 2. Check if published_date exists
        if self.published_date is None:
            return False

        # 3. Date comparison logic
        now = datetime.datetime.now().date()
        
        # Ensure we are comparing date to date (handle if self.published_date is datetime)
        pub_date = self.published_date
        if isinstance(pub_date, datetime.datetime):
            pub_date = pub_date.date()

        # True if published_date is today or earlier
        return pub_date <= now
    
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


from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin


@strawberry.input(
    description="""Input type for creating a Publication"""
)

class PublicationInsertGQLModel(InputModelMixin):
   getLoader = PublicationGQLModel.getLoader
   name: typing.Optional[str] = strawberry.field(
      description="Publication name assigned by an administrator",
      default = None
   )

   published_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Date of publication",
        default = None
     )
   
   reference: typing.Optional[str] = strawberry.field(
        description="Reference of the publication",
        default = None
     )
   
   place: typing.Optional[str] = strawberry.field(
        description="Place of publication",
        default = None
     )
   
   id: typing.Optional[IDType] = strawberry.field(
        description="Publication ID",
        default = None
     )
   
   rbacobject_id: IDType = strawberry.field(
        description="""Definitoin of access control"""
    )
   
   createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for updating a Publication"""
)

class PublicationUpdateGQLModel:
   id: IDType = strawberry.field(
        description="Publication ID"
     )
   
   lastchange: datetime.datetime = strawberry.field(
        description="Last change timestamp"
        )
   
   name: typing.Optional[str] = strawberry.field(
        description="Publication name assigned by an administrator",
        default = None
     )
   
   published_date: typing.Optional[datetime.datetime] = strawberry.field(
          description="Date of publication",
          default = None
      )
   
   reference: typing.Optional[str] = strawberry.field(
            description="Reference of the publication",
            default = None
        )
   
   place: typing.Optional[str] = strawberry.field(
            description="Place of publication",
            default = None
        )
   
   changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
   description= "Input type for deleting a Publication"
   )

class PublicationDeleteGQLModel:
   id: IDType = strawberry.field(
        description="Publication ID"
     )
   
   lastchange: datetime.datetime = strawberry.field(
        description="Last change timestamp"
        )
   
@strawberry.interface(
   description="Publication mutations"
)

class PublicationMutation:
   @strawberry.mutation(
      description="Insert a new publication",
      permission_classes=[OnlyForAuthentized],
      extensions=[UserAccessControlExtension[InsertError, PublicationGQLModel](
                roles=[
                    "administrátor",
                    "publication_manager",
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[InsertError, PublicationGQLModel](),
            # RbacProviderExtension[InsertError, PublicationGQLModel](),
            # LoadDataExtension[InsertError, PublicationGQLModel](
            #     getLoader=PublicationGQLModel.getLoader,
                
            # ),
            RbacInsertProviderExtension[InsertError, PublicationGQLModel](
                rbac_key_name="rbacobject_id"
            ),
        ],
   )

   async def publication_insert(
    self,
    info: strawberry.Info,
    publication: PublicationInsertGQLModel,
    rbacobject_id: IDType,
    user_roles: typing.List[dict],
) -> typing.Union[PublicationGQLModel, InsertError[PublicationGQLModel]]:
    return await Insert[PublicationGQLModel].DoItSafeWay(info=info, entity=publication)
     
   

   @strawberry.mutation(
        description="""Update a Publication""",
        permission_classes=[
            OnlyForAuthentized
            # SimpleUpdatePermission[EventGQLModel](roles=["administrátor"])
        ],
        extensions=[
            # UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
            UserAccessControlExtension[UpdateError, PublicationGQLModel](
                roles=[
                    "administrátor",
                    "publication_manager",
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[UpdateError, PublicationGQLModel](),
            RbacProviderExtension[UpdateError, PublicationGQLModel](),
            LoadDataExtension[UpdateError, PublicationGQLModel]()
        ],
    )
   
   async def publication_update(
      self,
      info: strawberry.Info,
      publication: PublicationUpdateGQLModel,
      db_row: typing.Any,
      rbacobject_id: IDType,
      user_roles: typing.List[dict],
    ) -> typing.Union[PublicationGQLModel, UpdateError[PublicationGQLModel]]:
        return await Update[PublicationGQLModel].DoItSafeWay(info=info, entity=publication)
   

   
   @strawberry.mutation(
        description="""Delete a Publication""",
        permission_classes=[
            OnlyForAuthentized,
            # SimpleDeletePermission[EventGQLModel](roles=["administrátor"])
        ],
        extensions=[
             #UpdatePermissionCheckRoleFieldExtension[GroupGQLModel](roles=["administrátor", "personalista"]),
           UserAccessControlExtension[DeleteError, PublicationGQLModel](
                roles=[
                    "administrátor",
                    "publication_manager",
                    # "personalista"
                ]
            ),
            UserRoleProviderExtension[DeleteError, PublicationGQLModel](),
            RbacProviderExtension[DeleteError, PublicationGQLModel](),
            LoadDataExtension[DeleteError, PublicationGQLModel]()
        ],
    )   
   async def publication_delete(
        self,
        info: strawberry.Info,
        publication: PublicationDeleteGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[PublicationGQLModel]]:
        return await Delete[PublicationGQLModel].DoItSafeWay(info=info, entity=publication)
    
   
    

   