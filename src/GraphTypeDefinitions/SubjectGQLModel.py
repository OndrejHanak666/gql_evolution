import typing
import strawberry
from .BaseGQLModel import IDType


from uoishelpers.gqlpermissions import (
    OnlyForAuthentized
)
from uoishelpers.resolvers import (
    VectorResolver,
    ScalarResolver
)
from .PublicationGQLModel import PublicationGQLModel, PublicationInputFilter

@strawberry.federation.type(extend=False, keys=["id"])
class SubjectGQLModel:
    id: IDType = strawberry.federation.field(external=False)

    from .BaseGQLModel import resolve_reference

    publication: typing.Optional[typing.List["PublicationGQLModel"]] = strawberry.field(
        description="List of publications associated with this subject",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver["PublicationGQLModel"](fkey_field_name="subject_id")
    )

    # async def event_invitations(self, info:strawberry.types.Info)