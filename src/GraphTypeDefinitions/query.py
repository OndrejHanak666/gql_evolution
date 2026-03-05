import strawberry

from .PublicationGQLModel import PublicationQuery
from .PublicationAuthorGQLModel import PublicationAuthorQuery
from .PublicationTypeGQLModel import PublicationTypeQuery
from .PublicationCategoryGQLModel import PublicationCategoryQuery

@strawberry.type(description="""Type for query root""")
class Query(PublicationQuery, PublicationAuthorQuery, PublicationTypeQuery, PublicationCategoryQuery):
    @strawberry.field(
        description="""Returns hello world"""
        )
    async def hello(
        self,
        info: strawberry.types.Info,
    ) -> str:
        return "hello world"
