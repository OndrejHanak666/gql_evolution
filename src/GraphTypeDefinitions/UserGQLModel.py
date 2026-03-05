import typing
import strawberry
from .BaseGQLModel import IDType


from uoishelpers.gqlpermissions import (
    OnlyForAuthentized
)
from uoishelpers.resolvers import (
    VectorResolver
)

from .PublicationAuthorGQLModel import PublicationAuthorGQLModel, PublicationAuthorInputFilter

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: IDType = strawberry.federation.field(external=True)

    from .BaseGQLModel import resolve_reference


    publication_authors: typing.List[PublicationAuthorGQLModel] = strawberry.field(
        description="Publication authors associated with the user",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver[PublicationAuthorGQLModel](fkey_field_name="user_id", whereType=PublicationAuthorInputFilter)
    )

    # async def event_invitations(self, info:strawberry.types.Info)