import strawberry

from .PublicationGQLModel import PublicationMutation
from .PublicationAuthorGQLModel import PublicationAuthorMutation
from .PublicationTypeGQLModel import PublicationTypeMutation

@strawberry.type(description="""Type for mutation root""")
class Mutation(
    PublicationMutation,
    PublicationAuthorMutation,
    PublicationTypeMutation,
    
):
    pass

