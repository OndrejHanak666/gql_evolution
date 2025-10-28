import strawberry

from .EventGQLModel import EventQuery
from .EventInvitationGQLModel import EventInvitationQuery
from .PublicationGQLModel import PublicationQuery
from .PublicationAuthorGQLModel import PublicationAuthorQuery
from .PublicationTypeGQLModel import PublicationTypeQuery
from .PublicationCategoryGQLModel import PublicationCategoryQuery

@strawberry.type(description="""Type for query root""")
class Query(EventQuery, EventInvitationQuery, PublicationQuery, PublicationAuthorQuery, PublicationTypeQuery, PublicationCategoryQuery):
    @strawberry.field(
        description="""Returns hello world"""
        )
    async def hello(
        self,
        info: strawberry.types.Info,
    ) -> str:
        return "hello world"
