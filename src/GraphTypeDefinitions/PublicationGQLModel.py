from typing import Optional
import typing
import datetime
import uuid
import strawberry

from uoishelpers.gqlpermissions import OnlyForAuthentized
from uoishelpers.resolvers import getLoadersFromInfo, createInputs2, PageResolver

from .BaseGQLModel import BaseGQLModel, IDType, Relation
from ._GraphResolvers import resolve_id, resolve_name, resolve_created, resolve_lastchange, resolve_createdby, resolve_changedby

PublicationTypeGQLModel = typing.Annotated["PublicationTypeGQLModel", strawberry.lazy(".PublicationTypeGQLModel")]

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

    id = resolve_id
    name = resolve_name

    @strawberry.field(description="publication type id")
    def publication_type_id(self) -> Optional[IDType]:
        return getattr(self, "publication_type_id", None)

    @strawberry.field(description="published date")
    def published_date(self) -> Optional[datetime.datetime]:
        return getattr(self, "published_date", None)

    @strawberry.field(description="reference")
    def reference(self) -> Optional[str]:
        return getattr(self, "reference", None)

    @strawberry.field(description="If a publication is valid")
    def valid(self) -> Optional[bool]:
        return getattr(self, "valid", None)

    @strawberry.field(description="place")
    def place(self) -> Optional[str]:
        return getattr(self, "place", None)

    # meta timestamps / authors (read-only)
    created: Optional[datetime.datetime] = strawberry.field(description="creation timestamp", default=None)
    lastchange: Optional[datetime.datetime] = strawberry.field(description="last change timestamp", default=None)
    createdby: Optional[IDType] = strawberry.field(description="who created this", default=None)
    changedby: Optional[IDType] = strawberry.field(description="who changed this", default=None)


@strawberry.interface(description="Publication queries")
class PublicationQuery:
    publication_by_id: Optional[PublicationGQLModel] = strawberry.field(
        description="get a publication by its id",
        permission_classes=[OnlyForAuthentized],
        resolver=PublicationGQLModel.load_with_loader
    )

    publication_page: typing.List[PublicationGQLModel] = strawberry.field(
        description="get a page of publications",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[PublicationGQLModel](whereType=PublicationInputFilter)
    )
# filepath: c:\Users\oh200\OneDrive - Univerzita obrany\škola\IT\5. semestr\gql_evolution\src\GraphTypeDefinitions\PublicationGQLModel.py
from typing import Optional
import typing
import datetime
import uuid
import strawberry

from uoishelpers.gqlpermissions import OnlyForAuthentized
from uoishelpers.resolvers import getLoadersFromInfo, createInputs2, PageResolver

from .BaseGQLModel import BaseGQLModel, IDType, Relation
from ._GraphResolvers import resolve_id, resolve_name, resolve_created, resolve_lastchange, resolve_createdby, resolve_changedby

PublicationTypeGQLModel = typing.Annotated["PublicationTypeGQLModel", strawberry.lazy(".PublicationTypeGQLModel")]

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

    id = resolve_id
    name = resolve_name

    @strawberry.field(description="publication type id")
    def publication_type_id(self) -> Optional[IDType]:
        return getattr(self, "publication_type_id", None)

    @strawberry.field(description="published date")
    def published_date(self) -> Optional[datetime.datetime]:
        return getattr(self, "published_date", None)

    @strawberry.field(description="reference")
    def reference(self) -> Optional[str]:
        return getattr(self, "reference", None)

    @strawberry.field(description="If a publication is valid")
    def valid(self) -> Optional[bool]:
        return getattr(self, "valid", None)

    @strawberry.field(description="place")
    def place(self) -> Optional[str]:
        return getattr(self, "place", None)

    # meta timestamps / authors (read-only)
    created: Optional[datetime.datetime] = strawberry.field(description="creation timestamp", default=None)
    lastchange: Optional[datetime.datetime] = strawberry.field(description="last change timestamp", default=None)
    createdby: Optional[IDType] = strawberry.field(description="who created this", default=None)
    changedby: Optional[IDType] = strawberry.field(description="who changed this", default=None)


@strawberry.interface(description="Publication queries")
class PublicationQuery:
    publication_by_id: Optional[PublicationGQLModel] = strawberry.field(
        description="get a publication by its id",
        permission_classes=[OnlyForAuthentized],
        resolver=PublicationGQLModel.load_with_loader
    )

    publication_page: typing.List[PublicationGQLModel] = strawberry.field(
        description="get a page of publications",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[PublicationGQLModel](whereType=PublicationInputFilter)
    )