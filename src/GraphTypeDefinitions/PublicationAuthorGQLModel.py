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
from sqlalchemy import select, func, update    
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
from src.DBDefinitions import PublicationAuthorModel

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]
PublicationGQLModel = typing.Annotated["PublicationGQLModel", strawberry.lazy(".PublicationGQLModel")]
PublicationInputFilter = typing.Annotated["PublicationInputFilter", strawberry.lazy(".PublicationGQLModel")]

@createInputs2
class PublicationAuthorInputFilter:
    id: IDType
    user_id: IDType
    publication_id: IDType
    order: int
    share: float
    


@strawberry.federation.type(
    keys=["id"],
    description="Entity representing a publication author")
class PublicationAuthorGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).PublicationAuthorModel

    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path representing the group's hierarchical location.  
Materializovaná cesta reprezentující umístění skupiny v hierarchii.""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )


    publication_id: typing.Optional[IDType] = strawberry.field(
        description="""ID of the associated publication""",
        default=None,
        permission_classes=[OnlyForAuthentized],
        directives=[Relation(to="PublicationGQLModel")]
    )

    order: typing.Optional[int] = strawberry.field(
        default=None,
        description="""Order of the author in the publication""",
        permission_classes=[OnlyForAuthentized]
    )

    share: typing.Optional[float] = strawberry.field(
        default=None,
        description="""Share of the author in the publication""",
        permission_classes=[OnlyForAuthentized]
    )


    user_id: typing.Optional[IDType] = strawberry.field(
        description="""ID of the associated user""",
        default=None,
        permission_classes=[OnlyForAuthentized],
        directives=[Relation(to="UserGQLModel")]
    )

    user: typing.Optional[UserGQLModel] = strawberry.field(
        description="""User assigned to the author role""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[UserGQLModel](fkey_field_name="user_id")
    )

    publication: typing.Optional[PublicationGQLModel] = strawberry.field(
        description="""Associated publication""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[PublicationGQLModel](fkey_field_name="publication_id")
    )   



@strawberry.interface(
    description="""Publication_author queries"""
)
class PublicationAuthorQuery:
    publication_author_by_id: typing.Optional[PublicationAuthorGQLModel] = strawberry.field(
        description="""get a publication_author by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=PublicationAuthorGQLModel.load_with_loader
    )

    publication_authors_page: typing.List[PublicationAuthorGQLModel] = strawberry.field(
        description="""get a page of publication_authors""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[PublicationAuthorGQLModel](whereType=PublicationAuthorInputFilter)
    )


from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin


@strawberry.input(
    description="""Input type for updating a PublicationAuthor"""
)
class PublicationAuthorUpdateGQLModel:
    id: IDType = strawberry.field(
        description="PublicationAuthor ID"
    )

    lastchange: datetime.datetime = strawberry.field(
        description="Last change timestamp"
    )

    user_id: typing.Optional[IDType] = strawberry.field(
        description="ID of the associated user",
        default=None
    )

    """ publication_id: typing.Optional[IDType] = strawberry.field(
        description="ID of the associated publication",
        default=None
    ) """

    order: typing.Optional[int] = strawberry.field(
        description="Order of the author in the publication",
        default=None
    )

    share: typing.Optional[float] = strawberry.field(
        description="Share of the author in the publication",
        default=None
    )

    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="Input type for deleting a PublicationAuthor"
)
class PublicationAuthorDeleteGQLModel:
    id: IDType = strawberry.field(
        description="PublicationAuthor ID"
    )

    lastchange: datetime.datetime = strawberry.field(
        description="Last change timestamp"
    )


@strawberry.input(
    description="Input type for adding an author to a publication"
)
class PublicationAddAuthorGQLModel:
    publication_id: IDType = strawberry.field(
        description="ID of the associated publication"
    )

    user_id: IDType = strawberry.field(
        description="ID of the associated user"
    )

    order: typing.Optional[int] = strawberry.field(
        description="Order of the author in the publication",
        default=1
    )

    share: typing.Optional[float] = strawberry.field(
        description="Share of the author in the publication",
        default=0.1
    )

    rbacobject_id: IDType = strawberry.field(
        description="""Definitoin of access control"""
    )
    
    createdby_id: strawberry.Private[IDType] = None


@strawberry.interface(
    description="PublicationAuthor mutations"
)
class PublicationAuthorMutation:

    @strawberry.mutation(
        description="""Update a PublicationAuthor""",
        permission_classes=[
            OnlyForAuthentized,
            #SimpleUpdatePermission[PublicationAuthorGQLModel](roles=["administrátor"])
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, PublicationAuthorGQLModel](
                roles=[
                    "administrátor",
                    "author_manager",
                    "publication_manager",
                ]
            ),
            UserRoleProviderExtension[UpdateError, PublicationAuthorGQLModel](),
            RbacProviderExtension[UpdateError, PublicationAuthorGQLModel](),
            LoadDataExtension[UpdateError, PublicationAuthorGQLModel]()
        ],
    )
    async def publication_author_update(
        self,
        info: strawberry.Info,
        publication_author: PublicationAuthorUpdateGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[PublicationAuthorGQLModel, UpdateError[PublicationAuthorGQLModel]]:
        return await Update[PublicationAuthorGQLModel].DoItSafeWay(info=info, entity=publication_author)

    @strawberry.mutation(
        description="""Delete a PublicationAuthor""",
        permission_classes=[
            OnlyForAuthentized,
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, PublicationAuthorGQLModel](
                roles=[
                    "administrátor",
                    "author_manager",
                    "publication_manager",
                ]
            ),
            UserRoleProviderExtension[DeleteError, PublicationAuthorGQLModel](),
            RbacProviderExtension[DeleteError, PublicationAuthorGQLModel](),
            LoadDataExtension[DeleteError, PublicationAuthorGQLModel]()
        ],
    )
    async def publication_author_delete(
        self,
        info: strawberry.Info,
        publication_author: PublicationAuthorDeleteGQLModel,
        db_row: typing.Any,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Optional[DeleteError[PublicationAuthorGQLModel]]:
        return await Delete[PublicationAuthorGQLModel].DoItSafeWay(info=info, entity=publication_author)
    

    @strawberry.mutation(
        description="Add an author to a publication",
        permission_classes=[OnlyForAuthentized],
        extensions=[UserAccessControlExtension[InsertError, PublicationAuthorGQLModel](
                    roles=[
                        "administrátor",
                        "author_manager",
                        "publication_manager",
                    ]
                ),
                UserRoleProviderExtension[InsertError, PublicationAuthorGQLModel](),
                RbacInsertProviderExtension[InsertError, PublicationAuthorGQLModel](
                    rbac_key_name="rbacobject_id"
                ),
            ],
    )
    async def publication_add_author(
        self,
        info: strawberry.Info,
        publication_author: PublicationAddAuthorGQLModel,
        rbacobject_id: IDType,
        user_roles: typing.List[dict],
    ) -> typing.Union[PublicationAuthorGQLModel, InsertError[PublicationAuthorGQLModel]]:
        
        # Session se bere z kontextu, kam ji vložila ta Extension
        session = info.context["session"]

        # 1. Zjistíme aktuální stav (max order a počet lidí)
        stmt = select(
            func.max(PublicationAuthorModel.order),
            func.count(PublicationAuthorModel.id)
        ).where(PublicationAuthorModel.publication_id == publication_author.publication_id)

        result = await session.execute(stmt)
        row = result.one()
        max_order = row[0] if row[0] is not None else 0
        count = row[1] if row[1] is not None else 0

        # 2. Vypočítáme nový férový podíl
        new_total_authors = count + 1
        new_fair_share = round(1.0 / new_total_authors, 4)

        # 3. Nastavíme hodnoty pro TOHOTO nového autora
        if publication_author.order is None or publication_author.order == 1:
            publication_author.order = max_order + 1
        
        # Nastavíme mu rovnou ten nový podíl
        publication_author.share = new_fair_share

        # 4. Provedeme VLOŽENÍ nového autora
        # Předpokládáme, že DoItSafeWay používá session z info.context a NEDĚLÁ vlastní commit
        result_gql = await Insert[PublicationAuthorGQLModel].DoItSafeWay(info=info, entity=publication_author)

        # Pokud se vložení nepovedlo (vrátila se chyba), skončíme
        # Extension uvidí, že jsme skončili bez vyhození výjimky, a pokusí se o commit.
        # Protože ale Insert selhal, v DB se nic nezměnilo, takže commit prázdné transakce nevadí.
        if isinstance(result_gql, InsertError):
            return result_gql

        # 5. AKTUALIZACE VŠECH: Teď musíme opravit podíl i těm ostatním (starým) autorům
        stmt_update = update(PublicationAuthorModel).where(
            PublicationAuthorModel.publication_id == publication_author.publication_id
        ).values(share=new_fair_share)

        # Pouze přidáme operaci do session. NECOMMITUJEME.
        await session.execute(stmt_update)
        
        # ZDE BYLA ZMĚNA: Odstraněno await session.commit()
        # O commit se postará SessionCommitExtension v bloku "else: await session.commit()"

        # 6. Vrátíme nově vytvořeného autora
        return result_gql